def inject(row):
    """
    Simulates an Intermittent Pulse Attack by injecting a sharp, transient 
    telemetry spike into a single isolated data block.
    """
    r = row.copy()
    
    # Apply high-intensity surge multipliers
    r["voltage_v"] *= 1.8
    r["current_a"] *= 2.0
    r["power_consumption_kw"] *= 2.2
    
    return r
