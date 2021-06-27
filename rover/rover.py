import sys
sys.path.append("/home/pi/rover-pi")

import subprocess
from config.uploader_enums import Directories
from datetime import datetime

# import warnings
# warnings.filterwarnings("ignore")

from rover.vehicle import Vehicle  # make this import less ridiculous
from rover.sensor import Sensor
from rover.uploader import Uploader


class Rover(Vehicle, Sensor, Uploader):
    def __init__(self):
        super(Rover, self).__init__()

        self.directory_string = Directories.DATA_DIRECTORY.value
        self.file_string = Directories.OUTPUT_FILE.value

        self.device_id = self.read_device_id()

        self.sensor_functions = {
            "Temperature": self.sense_temperature,
            "Humidity": self.sense_humidity,
            "Light": self.sense_light,
            "Distance": self.sense_distance,
        }

        self.setup_functions = {"Timestamp": self.timestamp}

        self.function_list = [self.sensor_functions, self.setup_functions]

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
