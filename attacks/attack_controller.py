import random

from attacks.replay_attack import inject as replay
from attacks.fdi_attack import inject as fdi
from attacks.byzantine_attack import inject as byzantine
from attacks.load_suppression_attack import inject as load_suppression
from attacks.pulse_attack import inject as pulse
from attacks.inconsistency_attack import inject as inconsistency
from attacks.sensor_freeze_attack import inject as sensor_freeze
from attacks.oscillation_attack import inject as oscillation
from attacks.ramp_attack import inject as ramp
from attacks.peak_clipping_attack import inject as peak_clipping
from attacks.data_substitution_attack import inject as data_substitution

# ✅ FIXED: Enriched attack catalog now includes ALL implemented vectors
ATTACKS = [
    replay,
    fdi,
    byzantine,
    load_suppression,
    pulse,
    inconsistency,
    sensor_freeze,
    oscillation,
    ramp,
    peak_clipping,
    data_substitution
]

def inject_attack(row, row_number):
    payload = row.copy()

    # ✅ FIXED: Force 0% attacks for the first 60 rows so the consumer 
    # can calculate a completely clean, unpolluted baseline threshold.
    if row_number < 60:
        attack_rate = 0.0
    else:
        attack_rate = 0.30

    if random.random() > attack_rate:
        payload["_attack"] = "NORMAL"
        return payload

    attack = random.choice(ATTACKS)
    attacked = attack(payload)
    
    attacked["_attack"] = (
        attack.__module__
        .split(".")[-1]
        .upper()
    )

    return attacked
