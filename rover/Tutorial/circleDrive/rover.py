import os
import subprocess
from dotenv import load_dotenv
from datetime import datetime

# import warnings
# warnings.filterwarnings("ignore")

from vehicle import Vehicle # make this import less ridiculous
from sensor import Sensor
from uploader import Uploader

class Rover(Vehicle, Sensor, Uploader):

    def __init__(self):
        load_dotenv()
        super(Rover, self).__init__()

        # this should all get moved to a setup.py or something eventually
        # -------------------------------------------------

        self.directory_string = os.getenv("DIRECTORY")
        self.file_string = os.getenv("FILE")
        self.data_functions = {
            'temperature': self.sense_temperature,
            'humidity': self.sense_humidity,
            'light': self.sense_light,
            'distance': self.sense_distance
        }

        self.setup_functions = {
            'timestamp': self.timestamp,
        }

        self.device_id = self.read_device_id()

    def read_device_id(self):
        bash_command = "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2"
        byte = subprocess.run(bash_command, shell=True, capture_output=True).stdout
        output = byte.decode("utf-8").strip()
        return output

    @staticmethod
    def timestamp():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    
    def create_data(self):
        data = {'device_id': self.device_id}
        
        for name, func in self.data_functions.items():
            value = func()
            data[name] = value

        for name, func in self.setup_functions.items():
            value = func()
            data[name] = value

        return data