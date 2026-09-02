# Global dictionary to track state toggles independently for each client substation
oscillation_state = {}

def inject(row):
    """
    Simulates a Sensor Oscillation Attack.
    Alternates values predictably row-by-row to create an artificial 
    high-frequency square wave across core electrical metrics.
    """
    global oscillation_state
    client = row.get("client_id", "default")
    
    # Initialize toggle state if it's the first time seeing this client
    if client not in oscillation_state:
        oscillation_state[client] = True
        
    r = row.copy()
    
    # Check current state for this client
    if oscillation_state[client]:
        # High State: Inject an aggressive mathematical surge
        r["voltage_v"] *= 1.35
        r["current_a"] *= 1.40
        r["power_consumption_kw"] *= 1.50
    else:
        # Low State: Keep it at the clean baseline operation value
        pass

    # Flip the switch for the next row coming through this client's stream
    oscillation_state[client] = not oscillation_state[client]
    
    return r
