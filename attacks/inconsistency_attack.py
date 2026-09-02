def inject(row):
    """
    Simulates a Physical Inconsistency Attack (Correlation Breaker)
    by shifting coupled electrical telemetry metrics in completely
    contradictory, physically impossible directions.
    """
    r = row.copy()
    
    # Spoof an extreme physical line load drawing current
    r["current_a"] *= 2.5
    
    # Simultaneously spoof a completely low-utilization or idle power state
    r["power_consumption_kw"] *= 0.1
    
    return r
