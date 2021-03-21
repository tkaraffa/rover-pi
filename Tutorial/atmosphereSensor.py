"""atmosphere data measured with DHT11 sensor using Raspberry Pi.

To better recreate a functional space rover, we have incorporated a DHT11 sensor
 onto the Raspberry Pi rover. This sensor will monitor the humidity and
 temperature at a given internal and write the time and measurements to a
 JSONL file to be passed to a semi-structured database.
"""

import Adafruit_DHT
from datetime import datetime
from time import sleep
import os
import json
import subprocess

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# change as needed
seconds_between_records = 1
directory_string = 'atmosphere-sensor-data'
file_string = 'atmosphere-sensor-data'
temp_units = "*C"
humidity_units = "%"

def get_output_dir(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return dir

def get_device_id():
    bash_command = "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output

def get_file_name(file):
    file_time = datetime.now().strftime("%Y-%m-%d--%H-%M-%S-%f")
    file_name = f"{file}--{file_time}.jsonl"
    return file_name

device_id = get_device_id()
output_dir = get_output_dir(data_string)
output_file = get_file_name(file_string)
output = os.path.join(output_dir, output_file)

while True:
    # record sensor data
    # humidity, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    humidity, temp = 15, 15 # stand-in data until sensor is set up

    time_record = datetime.now()
    date_string = time_record.strftime("%Y-%m-%d")
    time_string = time_record.strftime("%H-%M-%S-%f")
    record = {
        "device_id": device_id,
        "date": date_string,
        "time": time_string,
        "data": {
            "humidity": {
                "measurement": humidity,
                "units": humidity_units},
            "temperature": {
                "measurement": temp,
                "units": temp_units
            }
        }
    }
    with open(output, 'a+') as f:
        f.write(json.dumps(data)+"\n")
    sleep(seconds_between_records)
