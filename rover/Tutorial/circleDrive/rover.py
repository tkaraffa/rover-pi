import os
import subprocess
from dotenv import load_dotenv

# import warnings
# warnings.filterwarnings("ignore")

from vehicle import Vehicle # make this import less ridiculous
from sensor import Sensor

class Rover(Vehicle, Sensor):

    load_dotenv()

    def __init__(self):
        super(Rover, self).__init__()

        load_dotenv()
        # this should all get moved to a setup.py or something eventually
        # -------------------------------------------------

        self.directory_string = os.getenv("DIRECTORY")
        self.file_string = os.getenv("FILE")

        self.device_id = self.read_device_id()

    def read_device_id(self):
        bash_command = "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2"
        byte = subprocess.run(bash_command, shell=True, capture_output=True).stdout
        output = byte.decode("utf-8").strip()
        return output
    