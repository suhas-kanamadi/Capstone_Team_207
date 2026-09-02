from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *
import os

# ----------------------------------
# Create Spark Session
# ----------------------------------
spark = SparkSession.builder \
    .appName("SmartGridSocketStream") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# ----------------------------------
# Define JSON Schema
# ----------------------------------
schema = StructType([
    StructField("client_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("voltage_v", DoubleType(), True),
    StructField("current_a", DoubleType(), True),
    StructField("power_consumption_kw", DoubleType(), True),
    StructField("reactive_power_kvar", DoubleType(), True),
    StructField("power_factor", DoubleType(), True),
    StructField("solar_power_kw", DoubleType(), True),
    StructField("wind_power_kw", DoubleType(), True),
    StructField("grid_supply_kw", DoubleType(), True),
    StructField("voltage_fluctuation_pct", DoubleType(), True),
    StructField("overload_condition", DoubleType(), True),
    StructField("transformer_fault", DoubleType(), True),
    StructField("temperature_c", DoubleType(), True),
    StructField("humidity_pct", DoubleType(), True),
    StructField("electricity_price_usd_per_kwh", DoubleType(), True),
    StructField("predicted_load_kw", DoubleType(), True)
])

# ----------------------------------
# Read From Socket (IMPORTANT CHANGE)
# ----------------------------------
FASTAPI_IP = "10.133.19.95"   # \F0\9F\94\A5 CHANGE THIS TO YOUR FASTAPI MACHINE IP

lines = spark.readStream \
    .format("socket") \
    .option("host", FASTAPI_IP) \
    .option("port", 9999) \
    .load()

# ----------------------------------
# Parse JSON
# ----------------------------------
json_df = lines.select(from_json(col("value"), schema).alias("data"))
final_df = json_df.select("data.*")

# ----------------------------------
# Custom Output Directory
# ----------------------------------
output_dir = "custom_output"
os.makedirs(output_dir, exist_ok=True)

# ----------------------------------
# Function To Append Per Client
# ----------------------------------
def write_batch_to_files(batch_df, batch_id):

    if batch_df.count() == 0:
        return

    pdf = batch_df.toPandas()

    for client_id in pdf["client_id"].unique():
        client_data = pdf[pdf["client_id"] == client_id]

        file_path = os.path.join(output_dir, f"{client_id}.csv")

        if not os.path.exists(file_path):
            client_data.to_csv(file_path, index=False)
        else:
            client_data.to_csv(file_path, mode='a', header=False, index=False)

# ----------------------------------
# Start Streaming
# ----------------------------------
query = final_df.writeStream \
    .outputMode("append") \
    .foreachBatch(write_batch_to_files) \
    .start()

print("\F0\9F\94\A5 Spark Streaming Started...")

query.awaitTermination()
