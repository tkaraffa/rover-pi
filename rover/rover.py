import sys

sys.path.append("/home/pi/rover-pi")

import subprocess
from config.uploader_enums import Directories
from datetime import datetime

from vehicle import Vehicle
from sensor import Sensor
from uploader import Uploader


class Rover(Vehicle, Sensor, Uploader):
    """The amalgamated class of
    driving, sensing, and recording data.

    Attributes
    ----------
    directory_string: str, default="atmosphere-sensor-data"
        The directory in which to save atmospheric outputs

    file_string: str, default="atmosphere-sensor-data.json"
        The filename with which to save atmospheric outputs

    device_id: str
        The serial number of the Raspberry Pi

    sensor_functions: dict
        Mapping of names of environmental measurements to respective functions

    self.setup_functions: dict
        Mapping of names of general-purpose measurements to respective functions

    self.functions: dict
        Mapping of names of all measurements to respective functions
    """

    directory_string = Directories.DATA_DIRECTORY.value
    file_string = Directories.OUTPUT_FILE.value

    def __init__(self) -> None:
        super(Rover, self).__init__()

        self.device_id = self.read_device_id()

        self.sensor_functions = {
            "Temperature": self.sense_temperature,
            "Humidity": self.sense_humidity,
            "Light": self.sense_light,
            "Distance": self.sense_distance,
        }
        self.setup_functions = {"Timestamp": self.timestamp}

        self.functions = {**self.sensor_functions, **self.setup_functions}

    def read_device_id(self) -> str:
        """Uses a command to obtain the device's serial number"""
        bash_command = "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2"
        byte = subprocess.run(bash_command, shell=True, capture_output=True).stdout
        output = byte.decode("utf-8").strip()
        return output

    @staticmethod
    def timestamp() -> str:
        """Outputs a formatted date and time."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def create_data(self) -> dict:
        """Creates dictionary-formatted data to save."""
        data = {"ID": self.device_id}
        for name, function in self.functions:
            data[name] = function()
        return data
