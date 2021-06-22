import os
import subprocess
from dotenv import load_dotenv
from datetime import datetime

# import warnings
# warnings.filterwarnings("ignore")

from vehicle import Vehicle  # make this import less ridiculous
from sensor import Sensor
from uploader import Uploader


class Rover(Vehicle, Sensor, Uploader):
    def __init__(self):
        load_dotenv()
        super(Rover, self).__init__()

        self.directory_string = os.getenv("DIRECTORY")
        self.file_string = os.getenv("FILE")

        self.device_id = self.read_device_id()

        self.data_functions = {
            "Temperature": self.sense_temperature,
            "Humidity": self.sense_humidity,
            "Light": self.sense_light,
            "Distance": self.sense_distance,
        }

        self.setup_functions = {"Timestamp": self.timestamp}

        self.function_list = [self.data_functions, self.setup_functions]

    def read_device_id(self):
        bash_command = "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2"
        byte = subprocess.run(
            bash_command, shell=True, capture_output=True
        ).stdout
        output = byte.decode("utf-8").strip()
        return output

    @staticmethod
    def timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def create_data(self):
        data = {"ID": self.device_id}
        for func_dict in self.function_list:
            for name, func in func_dict.items():
                data[name] = func()
        return data
