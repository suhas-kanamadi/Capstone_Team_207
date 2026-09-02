def inject(row):
    """
    Simulates a Data Substitution Attack by replacing one sensor's 
    telemetry input directly with another sensor's data.
    """
    r = row.copy()
    
    # Clone the current reading directly into the voltage variable slot
    r["voltage_v"] = r["current_a"]
    
    return r
