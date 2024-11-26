from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
import os

load_dotenv()

INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")

print(f"URL: {INFLUXDB_URL}, Bucket: {INFLUXDB_BUCKET}")



client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG,
)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api(query_options=SYNCHRONOUS)

def write_to_influx(data):
    """
    JSONPlaceholder API'sinden gelen todo verilerini InfluxDB'ye yazar.
    """
    for todo in data:
        point = Point("todos") \
            .tag("userId", todo["userId"]) \
            .field("id", todo["id"]) \
            .field("title", todo["title"]) \
            .field("completed", todo["completed"])
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)



def read_from_influx(id):
    query = 'from(bucket: "deneme") \
    |> range(start: v.timeRangeStart, stop: v.timeRangeStop) \
    |> filter(fn: (r) => r["_measurement"] == "todos") \
    |> filter(fn: (r) => r["_field"] == "id") \
    |> filter(fn: (r) => r["userId"] == "1" or r["userId"] == "9") \
    |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false) \
    |> yield(name: "mean")'
    print("OK.")
    return query_api.query(org=client.org, query=query)
