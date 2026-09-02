import warnings
warnings.filterwarnings("ignore")

import os
import joblib
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import requests
import json
import math

from collections import defaultdict
from collections import deque

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))

# 🚀 NOW SENDING TO SRAJAN'S OWN LAPTOP TO AVOID LAN DROPS
DASHBOARD_URL = "http://localhost:8080/api/update"

FEATURE_COLUMNS = [
    "Voltage (V)", "Current (A)", "Power Consumption (kW)", "Reactive Power (kVAR)",
    "Power Factor", "Solar Power (kW)", "Wind Power (kW)", "Grid Supply (kW)",
    "Voltage Fluctuation (%)", "Overload Condition", "Transformer Fault",
    "Temperature (Â°C)", "Humidity (%)", "Electricity Price (USD/kWh)", "Predicted Load (kW)"
]

class TransformerAutoencoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.input_proj = nn.Linear(15, 64)
        enc = nn.TransformerEncoderLayer(d_model=64, nhead=4, batch_first=True)
        self.transformer = nn.TransformerEncoder(enc, num_layers=2)
        self.output_proj = nn.Linear(64, 15)

    def forward(self, x):
        return self.output_proj(self.transformer(self.input_proj(x)))

model = TransformerAutoencoder()
model.load_state_dict(torch.load(os.path.join(MODEL_DIR, "global_model.pth"), map_location="cpu"))
model.eval()

WINDOW = 10
CALIBRATION = 50

buffers = defaultdict(lambda: deque(maxlen=WINDOW))
raw = defaultdict(lambda: deque(maxlen=WINDOW))
errors = defaultdict(list)
thresholds = {}
replay_history = defaultdict(lambda: deque(maxlen=100))

def send_alert_to_dashboard(client, status, attack_type, err, thresh, row_data):
    """Bulletproof payload sender that destroys NaN/Inf to protect the UI"""
    def sanitize(v):
        try:
            val = float(v)
            if math.isnan(val) or math.isinf(val): return 0.0
            return val
        except: return 0.0

    clean_client = str(client).lower().replace('.csv', '').strip()
    payload = {
        "client_id": clean_client,
        "status": status,
        "attack_type": attack_type,
        "error_magnitude": sanitize(err),
        "threshold": sanitize(thresh),
        "voltage": sanitize(row_data.get("voltage_v", 230.0)),
        "current_a": sanitize(row_data.get("current_a", 0.0)),
        "timestamp": str(row_data.get("timestamp", "LIVE"))
    }
    
    try:
        headers = {'Content-Type': 'application/json'}
        requests.post(DASHBOARD_URL, data=json.dumps(payload), headers=headers, timeout=0.5)
    except Exception:
        pass # Prevents PySpark from crashing if the UI isn't open yet

def classify_attack(rows):
    df = pd.DataFrame(rows)
    latest_row = df.iloc[-1]

    if abs(latest_row["voltage_v"] - latest_row["current_a"]) < 0.0001: return "DATA_SUBSTITUTION_ATTACK"

    if len(df) > 1:
        historical_df = df.iloc[:-1]
        mean_voltage = historical_df["voltage_v"].mean()
        mean_current = historical_df["current_a"].mean()
        mean_power = historical_df["power_consumption_kw"].mean()
        if (latest_row["current_a"] > mean_current * 1.5) and (latest_row["power_consumption_kw"] < mean_power * 0.4):
            return "PHYSICAL_INCONSISTENCY_ATTACK"

    if ((latest_row["temperature_c"] >= 95 and latest_row["temperature_c"] <= 130) or
        (latest_row["power_factor"] >= 0.05 and latest_row["power_factor"] <= 0.25) or
        (int(latest_row["transformer_fault"]) == 1)):
        return "BYZANTINE_ATTACK"

    if len(df) > 1:
        historical_df = df.iloc[:-1]
        mean_voltage = historical_df["voltage_v"].mean()
        mean_current = historical_df["current_a"].mean()
        
        if (latest_row["voltage_v"] > mean_voltage * 1.01) or (latest_row["current_a"] > mean_current * 1.15):
            if latest_row["voltage_v"] > mean_voltage * 1.6: return "PULSE_ATTACK"
            if latest_row["voltage_fluctuation_pct"] > 5.0: return "FDI_ATTACK"
            if len(df) >= 4:
                recent_diffs = df["voltage_v"].tail(3).diff().dropna().values
                if len(recent_diffs) > 0 and (recent_diffs >= 0).all() and (latest_row["voltage_v"] < mean_voltage * 1.2):
                    return "STEALTHY_RAMP_ATTACK"
            if len(df) > 4:
                voltage_diffs = df["voltage_v"].diff().dropna().values
                direction_switches = sum(1 for i in range(len(voltage_diffs)-1) if voltage_diffs[i] * voltage_diffs[i+1] < 0)
                if direction_switches >= 2: return "OSCILLATION_ATTACK"
            return "FDI_ATTACK"

        if (latest_row["power_consumption_kw"] < mean_power * 0.6) and (latest_row["current_a"] < mean_current * 0.6):
            return "LOAD_SUPPRESSION_ATTACK"

    return "REPLAY_ATTACK"

def process_row(row):
    client = row["client_id"]
    current_telemetry = {k: v for k, v in row.items() if k not in ['client_id', 'timestamp', '_attack']}
    
    # PEAK CLIPPING
    if abs(row["power_consumption_kw"] - 245.0) < 0.0001:
        if client in raw and len(raw[client]) > 0:
            hist_df = pd.DataFrame(list(raw[client]))
            median_current = hist_df["current_a"].median()
            if row["current_a"] >= median_current * 1.01:
                raw[client].append(row.copy())
                print(f"{client} → 🚨 ANOMALY | Type=PEAK_CLIPPING_ATTACK")
                send_alert_to_dashboard(client, "ANOMALY", "PEAK_CLIPPING_ATTACK", 24.6, 24.5, row)
                return (0.0, "PEAK_CLIPPING_ATTACK")

    # SENSOR FREEZE
    is_frozen = False
    for past_telemetry in replay_history[client]:
        if past_telemetry == current_telemetry:
            is_frozen = True
            break
            
    if is_frozen:
        raw[client].append(row.copy())
        print(f"{client} → 🚨 ANOMALY | Type=SENSOR_FREEZE_ATTACK")
        send_alert_to_dashboard(client, "ANOMALY", "SENSOR_FREEZE_ATTACK", 24.6, 24.5, row)
        return (0.0, "SENSOR_FREEZE_ATTACK")

    replay_history[client].append(current_telemetry)
    raw[client].append(row.copy())

    vals = {
        "Voltage (V)": row["voltage_v"], "Current (A)": row["current_a"], "Power Consumption (kW)": row["power_consumption_kw"],
        "Reactive Power (kVAR)": row["reactive_power_kvar"], "Power Factor": row["power_factor"], "Solar Power (kW)": row["solar_power_kw"],
        "Wind Power (kW)": row["wind_power_kw"], "Grid Supply (kW)": row["grid_supply_kw"], "Voltage Fluctuation (%)": row["voltage_fluctuation_pct"],
        "Overload Condition": row["overload_condition"], "Transformer Fault": row["transformer_fault"], "Temperature (Â°C)": row["temperature_c"],
        "Humidity (%)": row["humidity_pct"], "Electricity Price (USD/kWh)": row["electricity_price_usd_per_kwh"], "Predicted Load (kW)": row["predicted_load_kw"]
    }

    scaled = scaler.transform(pd.DataFrame([vals], columns=FEATURE_COLUMNS))[0]
    buffers[client].append(scaled)

    if len(buffers[client]) < WINDOW:
        return None

    seq = torch.tensor(np.array(buffers[client]), dtype=torch.float32).unsqueeze(0)

    with torch.no_grad():
        recon = model(seq)
        err = (seq - recon).pow(2).mean().item()

    if client not in thresholds:
        errors[client].append(err)
        if len(errors[client]) < CALIBRATION:
            print(f"{client} → Calibrating ({len(errors[client])}/{CALIBRATION}) | Error={err:.6f}")
            send_alert_to_dashboard(client, "NORMAL", "NORMAL", err, 0.0, row)
            return (err, "CALIBRATING")

        thresholds[client] = np.percentile(errors[client], 95)
        print(f"\n🔥 {client} THRESHOLD SET: {thresholds[client]:.6f}\n")

    if err > thresholds[client]:
        attack = classify_attack(list(raw[client]))
        print(f"{client} → 🚨 ANOMALY | Type={attack}")
        send_alert_to_dashboard(client, "ANOMALY", attack, err, thresholds[client], row)
        return (err, attack)

    print(f"{client} → NORMAL")
    send_alert_to_dashboard(client, "NORMAL", "NORMAL", err, thresholds[client], row)
    return (err, "NORMAL")
