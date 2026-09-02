def inject(row):
    """
    Simulates a Load Suppression Attack by artificially reducing reporting 
    metrics to obscure true power grid consumption levels.
    """
    r = row.copy()
    
    # Scale down active power and forecast demand characteristics
    r["power_consumption_kw"] *= 0.45
    r["predicted_load_kw"] *= 0.50
    
    # Coherently reduce current to preserve basic physical properties (P = V * I)
    r["current_a"] *= 0.50
    
    return r
