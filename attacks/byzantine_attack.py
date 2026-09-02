
import random


def inject(row):

    r = row.copy()

    r["power_factor"] = random.uniform(
        0.05,
        0.25
    )

    r["temperature_c"] = random.uniform(
        95,
        130
    )

    r["grid_supply_kw"] *= 2.5

    r["solar_power_kw"] *= 0.1

    r["transformer_fault"] = 1

    return r

