import Adafruit_DHT
from datetime import datetime
from time import sleep
import os
import json

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# change as needed
seconds_between_records = 1

output_dir = 'atmosphere-sensor-data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

file_time = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
outfile = f"atmosphere-sensor--{file_time}.json"

output = os.path.join(output_dir, outfile)

while True:
    # record sensor data
    # humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    # stand-in data until sensor arrives
    humidity, temperature = 15, 15

    time_record = datetime.now()
    t = time_record.strftime("%Y-%m-%d--%H-%M-%S")
    data = {"time": t, "temperature": temperature, "humidity": humidity}
    with open(output, 'a+') as f:
        f.write(json.dumps(data)+"\n")
    sleep(seconds_between_records)
