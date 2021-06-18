import os
from gpiozero import LightSensor
import subprocess
from dotenv import load_dotenv
import adafruit_dht
import board

import warnings
warnings.filterwarnings("ignore")

from vehicle import Vehicle # make this import less ridiculous


class Rover(Vehicle):

    load_dotenv()


    def __init__(self):
        super().__init__()

        load_dotenv()
        # this should all get moved to a setup.py or something eventually
        # -------------------------------------------------

        self.temp = float(os.getenv("TEMP"))
        self.humidity = float(os.getenv("HUMIDITY"))
        self.directory_string = os.getenv("DIRECTORY")
        self.file_string = os.getenv("FILE")
        self.temp_units = os.getenv("TEMPUNITS")
        self.humidity_units = os.getenv("HUMIDITY")

        self.LightSensor = LightSensor(os.getenv("LIGHTSENSOR"))
        self.DHTSensor = self.create_dht_sensor(os.getenv("ATMOSPHERESENSOR"))
        self.device_id = self.read_device_id()

    # Setup functions --------------------------------------------------- #

    def create_dht_sensor(self, pin):
        exec(f'sensor = adafruit_dht.DHT11(board.{pin}, use_pulseio=False)', None, globals()) 
        return sensor


    def read_device_id(self):
        bash_command = "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2"
        byte = subprocess.run(bash_command, shell=True, capture_output=True).stdout
        output = byte.decode("utf-8").strip()
        return output

    def sense_light(self):
        try:
            return self.LightSensor.value
        except:
            None

    def sense_humidity(self):
        try:
            return self.DHTSensor.humidity
        except:
            return None

    def sense_temperature(self):
        try:
            return self.DHTSensor.temperature
        except:
            return None

    # End sensor functions ---------------------------------------------- #

    # Driving functions ------------------------------------------------- #

    # End driving functions --------------------------------------------- #
