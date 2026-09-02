import copy

# Global state to persist the captured normal reading across streaming records
frozen_memory = {}

def inject(row):
    """
    Simulates a Sensor Freeze / Stuck-at Attack.
    The module locks onto an initial real telemetry state and repeatedly 
    broadcasts it, blinding operators to subsequent changes.
    """
    global frozen_memory
    client = row.get("client_id", "default")
    
    # If this client is targeted for the first time, store its current valid telemetry row
    if client not in frozen_memory:
        frozen_memory[client] = copy.deepcopy(row)
        return row

    # Grab the frozen reference baseline
    stuck_row = copy.deepcopy(frozen_memory[client])
    
    # Overwrite the stale timestamp with the current live real-time timestamp 
    # so that it passes basic ingestion validation layers
    stuck_row["timestamp"] = row["timestamp"]
    
    return stuck_row
