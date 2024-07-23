import os
import pandas as pd
import influxdb_client
from influxdb_client.client.write_api import ASYNCHRONOUS
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Retrieve the token and other details from the environment variables
token = os.getenv("INFLUXDB_TOKEN", "your_default_token")
org = os.getenv("INFLUXDB_ORG", "your_organization")
bucket = os.getenv("INFLUXDB_BUCKET", "your_bucket")
url = os.getenv("INFLUXDB_URL", "http://localhost:8086")


# Initialize InfluxDB client
client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Write API instance
write_api = client.write_api(write_options=ASYNCHRONOUS)

# Define the current time and the cutoff time (three weeks ago)
now = datetime.now()
cutoff_time = now - timedelta(weeks=3)

# Define a function to convert rows to InfluxDB points
def row_to_point(row):
    try:
        ts = datetime.fromtimestamp(float(row["ts"]))
        if ts < cutoff_time:
            return None  # Skip rows older than three weeks

        ts_epoch = int(ts.timestamp())  # Convert to epoch timestamp
    except ValueError as e:
        print(f"Timestamp conversion error: {e}")
        return None

    light = str(row["light"]).lower() == 'true'
    motion = str(row["motion"]).lower() == 'true'
    smoke = str(row["smoke"]).lower() == 'true'

    return (
        influxdb_client.Point("sensor_reading")  # Measurement name
        .tag("device", row["device"])
        .field("co", row["co"])
        .field("humidity", row["humidity"])
        .field("light", light)
        .field("lpg", row["lpg"])
        .field("motion", motion)
        .field("smoke", smoke)
        .field("temp", row["temp"])
        .time(ts_epoch, influxdb_client.WritePrecision.S)  # Use WritePrecision.S for seconds
    )

# Load data from CSV file
df = pd.read_csv("sensor_data.csv", delimiter=";")  # Ensure delimiter matches your CSV file


points = []
# Convert each row to a Point object and write to InfluxDB
for index, row in df.iterrows():
    point = row_to_point(row)
    if point:
        points.append(point)
        # Batch write every 1000 points or after some interval
    if len(points) >= 1000:
        try:
            write_api.write(bucket=bucket, org=org, record=points)
            points = []
        except Exception as e:
            print(f"Error writing points: {e}")

# Write remaining points
if points:
    try:
        write_api.write(bucket=bucket, org=org, record=points)
    except Exception as e:
        print(f"Error writing remaining points: {e}")

print("Complete. Return to the InfluxDB UI.")

# Query example
query = f"""
from(bucket: "{bucket}")
    |> range(start: -1h)
"""

# Execute the query
try:
    query_api = client.query_api()
    tables = query_api.query(query, org=org)
    for table in tables:
        for record in table.records:
            print(f'Time: {record["_time"]}, Value: {record["_value"]}')
except Exception as e:
    print(f"Error executing query: {e}")
finally:
    client.close()