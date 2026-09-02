from fastapi import FastAPI
from master.schema import GridData
from master.socket_server import send_to_spark, start_socket_server
from anomaly_detector import process_row
from threading import Thread
from kafka import KafkaConsumer
import json

app = FastAPI()

# 🔥 Kafka config
KAFKA_BROKER = "10.133.19.103:9092"
TOPIC = "grid-data"

# ---------------------------
# Start socket server (Spark)
# ---------------------------
@app.on_event("startup")
def startup_event():
    Thread(target=start_socket_server, daemon=True).start()
    Thread(target=consume_kafka, daemon=True).start()

# ---------------------------
# Kafka Consumer Logic
# ---------------------------
def consume_kafka():

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='grid-group'
    )

    print("🔥 Kafka Consumer Started...")

    for message in consumer:

        row = message.value

        # 🔥 STEP 1: ANOMALY DETECTION
        result = process_row(row)

        if result:
            error, status = result
            print(f"{row['client_id']} → Error: {error:.6f} → {status}")

        # 🔥 STEP 2: SEND TO SPARK
        send_to_spark(json.dumps(row))

# ---------------------------
# Optional health check
# ---------------------------
@app.get("/")
def root():
    return {"status": "Kafka consumer running"}
