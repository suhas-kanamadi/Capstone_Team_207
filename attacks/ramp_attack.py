# Tracks the cumulative linear drift steps per client substation
ramp_steps = {}

def inject(row):
    """
    Simulates a Stealthy Ramp-Up Attack by slowly walking the voltage 
    upward by small, incremental fractions over consecutive rows.
    """
    global ramp_steps
    client = row.get("client_id", "default")
    
    if client not in ramp_steps:
        ramp_steps[client] = 0
        
    ramp_steps[client] += 1
    r = row.copy()
    
    # Gradually scale the voltage bias based on consecutive iterations (max 40 steps)
    drift_factor = 1.0 + (0.003 * min(ramp_steps[client], 40))
    r["voltage_v"] *= drift_factor
    
    return r
