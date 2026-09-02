from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import io
import csv
import asyncio
from contextlib import asynccontextmanager

async def decay_chart_histories():
    while True:
        await asyncio.sleep(1.0)
        for cid in chart_histories:
            chart_histories[cid].pop(0)
            if client_statuses.get(cid, "NORMAL") == "ANOMALY":
                chart_histories[cid].append(client_errors.get(cid, 0.0))
            else:
                chart_histories[cid].append(0.0)

@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    task = loop.create_task(decay_chart_histories())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

client_thresholds = {"client_a": 24.5, "client_b": 24.5, "client_c": 24.5, "client_d": 24.5}
client_statuses = {"client_a": "NORMAL", "client_b": "NORMAL", "client_c": "NORMAL", "client_d": "NORMAL"}
client_errors = {"client_a": 0.0, "client_b": 0.0, "client_c": 0.0, "client_d": 0.0}
client_voltages = {"client_a": 230.0, "client_b": 230.0, "client_c": 230.0, "client_d": 230.0}

latest_alert = {
    "status": "NORMAL", "client_id": "client_a", "attack_type": "NORMAL",
    "voltage_v": 230.0, "reconstruction_error": 0.0, "threshold": 24.5
}

chart_histories = {
    "client_a": [0.0] * 60, "client_b": [0.0] * 60, 
    "client_c": [0.0] * 60, "client_d": [0.0] * 60,
}

event_logs = [{"time": "LIVE", "desc": "Grid Shield security link online on localhost"}]

attack_counts = {
    "FDI_ATTACK": 0, "BYZANTINE_ATTACK": 0, "REPLAY_ATTACK": 0, "PULSE_ATTACK": 0,
    "LOAD_SUPPRESSION_ATTACK": 0, "OSCILLATION_ATTACK": 0, "SENSOR_FREEZE_ATTACK": 0,
    "PHYSICAL_INCONSISTENCY_ATTACK": 0, "STEALTHY_RAMP_ATTACK": 0, "PEAK_CLIPPING_ATTACK": 0, "DATA_SUBSTITUTION_ATTACK": 0
}

@app.get("/", response_class=HTMLResponse)
def serve_dashboard_ui():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/update")
async def receive_detection(request: Request):
    global latest_alert, event_logs, attack_counts, client_thresholds, client_statuses, client_errors, client_voltages
    try:
        payload = await request.json()
        print(f"✅ DASHBOARD UPDATED: {payload.get('client_id')} -> {payload.get('attack_type')} | Err: {payload.get('error_magnitude')} | Thresh: {payload.get('threshold')}")
    except Exception as e:
        print(f"❌ JSON ERROR REJECTED: {e}")
        return {"status": "error"}
    
    raw_client = str(payload.get("client_id", "client_a")).strip().lower()
    client_id = os.path.splitext(raw_client)[0]

    status = payload.get("status", "NORMAL")
    
    # ✅ FIX: Removed all round() limits to capture high-precision terminal floats
    error_mag = payload.get("error_magnitude", 0.0)
    thresh = payload.get("threshold", 24.5)
    volt = payload.get("voltage", 230.0)

    client_thresholds[client_id] = thresh
    client_statuses[client_id] = status
    client_errors[client_id] = error_mag
    client_voltages[client_id] = volt

    latest_alert = {
        "status": status,
        "client_id": client_id,
        "attack_type": payload.get("attack_type", "NORMAL"),
        "voltage_v": volt,
        "reconstruction_error": error_mag,
        "threshold": thresh
    }

    if client_id in chart_histories:
        chart_histories[client_id][-1] = error_mag

    if status == "ANOMALY":
        atk = latest_alert["attack_type"]
        attack_counts[atk] = attack_counts.get(atk, 0) + 1
        time_slug = str(payload.get("timestamp", "LIVE"))[-8:] if len(str(payload.get("timestamp", ""))) > 8 else "LIVE"
        event_logs.insert(0, {"time": time_slug, "desc": f"{atk.replace('_', ' ')} on {client_id}"})
        if len(event_logs) > 30: event_logs.pop()

    return {"status": "success"}

@app.get("/api/data")
def stream_to_browser(response: Response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    alarms_count = sum(attack_counts.values())
    avg_volt = sum(client_voltages.values()) / len(client_voltages)
    
    return {
        "metrics": {
            "voltage_avg": avg_volt,
            "active_alarms": alarms_count,
            "anomaly_rate": round((alarms_count / max(alarms_count + 100, 1)) * 100, 1)
        },
        "histories": chart_histories,
        "thresholds": client_thresholds,
        "alerts": [latest_alert] if latest_alert["status"] == "ANOMALY" else [],
        "logs": event_logs,
        "distributions": attack_counts
    }

@app.get("/api/export")
def export_logs():
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["time", "desc"])
    writer.writeheader()
    for log in event_logs:
        writer.writerow(log)
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=gridshield_incident_logs.csv"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
