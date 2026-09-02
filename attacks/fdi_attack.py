
import random


def inject(row):

    r = row.copy()

    r["voltage_v"] *= 1.4

    r["current_a"] *= 1.5

    r["power_consumption_kw"] *= 1.8

    r["predicted_load_kw"] *= 1.6

    r["voltage_fluctuation_pct"] += random.uniform(
        10,
        20
    )

    return r

