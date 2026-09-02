
import os
import sys

ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(ROOT)

import pandas as pd
import time
import json

from kafka import KafkaProducer
from attacks.attack_controller import inject_attack


KAFKA_BROKER = "10.133.19.103:9092"
TOPIC = "grid-data"


csv_file = sys.argv[1]

client_id = os.path.splitext(
    os.path.basename(csv_file)
)[0]


df = pd.read_csv(
    csv_file,
    encoding="latin1"
)

df.columns = [

"timestamp",
"voltage_v",
"current_a",
"power_consumption_kw",
"reactive_power_kvar",
"power_factor",
"solar_power_kw",
"wind_power_kw",
"grid_supply_kw",
"voltage_fluctuation_pct",
"overload_condition",
"transformer_fault",
"temperature_c",
"humidity_pct",
"electricity_price_usd_per_kwh",
"predicted_load_kw"

]

df = df.fillna(0)


producer = KafkaProducer(

bootstrap_servers=KAFKA_BROKER,

value_serializer=lambda v:
json.dumps(v).encode(
"utf-8"
)

)


print(f"\n🚀 Streaming {client_id}\n")


for idx, row in df.iterrows():

    payload = row.to_dict()

    payload["client_id"] = client_id


    payload = inject_attack(
        payload,
        idx
    )


    attack = payload.pop(
        "_attack",
        "NORMAL"
    )


    producer.send(
        TOPIC,
        payload
    )


    print(
f"{client_id} → sent | Attack={attack}"
    )


    time.sleep(1)


producer.flush()

producer.close()


