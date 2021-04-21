from configparser import ConfigParser
import os
from gpiozero import PWMOutputDevice, DigitalOutputDevice, Button, DistanceSensor
import Adafruit_DHT
import subprocess
from time import sleep

def get_config_path(ini_file="rover.ini"):
    return os.path.join(os.path.dirname(__file__), ini_file)

def do_record_travel(function):
    def wrapper(self):
        self.record_travel = True
        function(self)
    return wrapper
    
def do_not_record_travel(function):
    def wrapper(self):
        self.record_travel = False
        function(self)
    return wrapper


class Rover:
    def __init__(self):
        # this should all get moved to a setup.py or something eventually
        # -------------------------------------------------
        self.config_path = get_config_path()

        config = ConfigParser()
        config.read(self.config_path)
        rover_config = config["Rover"]
        self.record_travel = True
        self.low_speed = float(rover_config["LOWSPEED"])
        self.high_speed = float(rover_config["HIGHSPEED"])
        self.turn_time = float(rover_config["TURNTIME"])
        self.wheel_diameter = float(rover_config["WHEELDIAMETER"])
        self.travel = 0
        self.temp = float(rover_config["TEMP"])
        self.humidity = float(rover_config["HUMIDITY"])
        self.directory_string = rover_config["DIRECTORY"]
        self.file_string = rover_config["FILE"]
        self.temp_units = rover_config["TEMPUNITS"]
        self.humidity_units = rover_config["HUMIDITY"]
        self.RightForward = DigitalOutputDevice(rover_config["RIGHTFORWARD"])
        self.RightBackward = DigitalOutputDevice(rover_config["RIGHTBACKWARD"])
        self.RightSpeedPWM = PWMOutputDevice(rover_config["RIGHTSPEEDPWM"])
        self.LeftForward = DigitalOutputDevice(rover_config["LEFTFORWARD"])
        self.LeftBackward = DigitalOutputDevice(rover_config["LEFTBACKWARD"])
        self.LeftSpeedPWM = PWMOutputDevice(rover_config["LEFTSPEEDPWM"])
        self.RotaryEncoder = Button(rover_config["ROTARYENCODER"]) 
        self.DistanceSensor = DistanceSensor(rover_config["ECHO"], rover_config["TRIG"])
        self.DHT_SENSOR = Adafruit_DHT.DHT11
        self.DHT_PIN = rover_config["ATMOSPHERESENSOR"]
        # ------------------------------------------

        self.device_id = self.get_device_id()
        self.RotaryEncoder.when_pressed = self.add_travel
        #self.humidity, self.temp = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)




    def add_travel(self):
        if self.record_travel == True:
            self.travel += 1
        if self.travel % 100 == 0:
            print(self.travel)


    def stop(self):
        self.RightForward.off()
        self.LeftForward.off()
        self.RightBackward.off()
        self.LeftBackward.off()
        self.RightSpeedPWM.value = 0
        self.LeftSpeedPWM.value = 0

    @do_record_travel
    def goForward(self):
        self.stop()
        self.RightForward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_record_travel
    def goBackward(self):
        self.stop()
        self.RightBackward.on()
        self.LeftBackward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_not_record_travel
    def spinRight(self):
        self.stop()
        self.RightBackward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_not_record_travel
    def spinLeft(self):
        self.stop()
        self.RightForward.on()
        self.LeftBackward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_record_travel
    def turnForwardRight(self):
        self.stop()
        self.RightForward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.low_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_record_travel
    def turnForwardLeft(self):
        self.stop()
        self.RightForward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.low_speed

    @do_record_travel
    def turnBackwardRight(self):
        self.stop()
        self.RightBackward.on()
        self.LeftBackward.on()
        self.RightSpeedPWM.value = self.low_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_record_travel
    def turnBackwardLeft(self):
        self.stop()
        self.RightBackward.on()
        self.LeftBackward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.low_speed

    @do_not_record_travel
    def turnRight(self):
        for _ in range(2):
            self.turnForwardRight()
            sleep(self.turn_time)
            self.turnBackwardLeft()
            sleep(self.turn_time)

    @do_not_record_travel
    def turnLeft(self):
        for _ in range(2):
            self.turnForwardLeft()
            sleep(self.turn_time)
            self.turnBackwardRight()
            sleep(self.turn_time)

    def get_device_id(self):
        bash_command = "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2"
        byte = subprocess.run(bash_command, shell=True, capture_output=True).stdout
        output = byte.decode("utf-8").strip()
        return output

    def setup(self):
        self.device_id = self.get_device_id()
        self.RotaryEncoder.when_pressed = self.add_travel
        #self.humidity, self.temp = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
