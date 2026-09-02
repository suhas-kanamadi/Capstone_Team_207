from pydantic import BaseModel

class GridData(BaseModel):
    client_id: str
    timestamp: str
    voltage_v: float
    current_a: float
    power_consumption_kw: float
    reactive_power_kvar: float
    power_factor: float
    solar_power_kw: float
    wind_power_kw: float
    grid_supply_kw: float
    voltage_fluctuation_pct: float
    overload_condition: float
    transformer_fault: float
    temperature_c: float
    humidity_pct: float
    electricity_price_usd_per_kwh: float
    predicted_load_kw: float

