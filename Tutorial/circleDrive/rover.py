from configparser import ConfigParser
import os
from gpiozero import PWMOutputDevice, DigitalOutputDevice, Button, DistanceSensor
import adafruit_dht
import subprocess
import board
from datetime import datetime
from time import sleep
import random


class Rover:
    def __init__(self):
        # this should all get moved to a setup.py or something eventually
        # -------------------------------------------------
        self.config_path = self.get_config_path()

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
        self.DistanceSensor = DistanceSensor(echo=rover_config["ECHO"], trigger=rover_config["TRIG"])
        # self.DHT_PIN = board(rover_config["ATMOSPHERESENSOR"])
        # self.DHT_SENSOR = adafruit_dht.DHT11()
        self.DistanceSensor.threshold = 0.5
        # ------------------------------------------
        self.accel_increment = 100
        self.decel_increment = 100
        self.accel_time = 5
        self.decel_time = 5
        self.device_id = self.get_device_id()
        self.RotaryEncoder.when_pressed = self.add_travel
        self.DistanceSensor.when_in_range = self.change_direction

        # self.humidity, self.temp = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)

    # Setup functions --------------------------------------------------- #
    def get_config_path(self, ini_file="rover.ini"):
        return os.path.join(os.path.dirname(__file__), ini_file)

    def get_device_id(self):
        bash_command = "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2"
        byte = subprocess.run(bash_command, shell=True, capture_output=True).stdout
        output = byte.decode("utf-8").strip()
        return output

    # ------------------------------------------------------------------- #

    # Sensor fucntions -------------------------------------------------- #
    def add_travel(self):
        if self.record_travel == True:
            self.travel += 1

    def change_direction(self):
        choice = random.choice([self.spinLeft, self.spinRight, self.turnLeft, self.turnRight])
        choice()

    # End sensor functions ---------------------------------------------- #

    # Driving functions ------------------------------------------------- #
    def stop(self):
        self.RightForward.off()
        self.LeftForward.off()
        self.RightBackward.off()
        self.LeftBackward.off()
        self.RightSpeedPWM.value = 0
        self.LeftSpeedPWM.value = 0

    def do_record_travel(function):
        def wrapper(self):
            self.record_travel = True
            self.stop()
            function(self)

        return wrapper

    def do_not_record_travel(function):
        def wrapper(self):
            self.record_travel = False
            self.stop()
            function(self)

        return wrapper

    def accel(self):
        a = int(self.high_speed * self.accel_increment)
        for speed in range(a):
            self.RightSpeedPWM.value = speed / self.accel_increment
            self.LeftSpeedPWM.value = speed / self.accel_increment
            sleep(self.accel_time / a)
            print(self.RightSpeedPWM.value)

    def decel(self):
        d = int(self.high_speed * self.decel_increment)
        for speed in reversed(range(d)):
            self.RightSpeedPWM.value = speed / self.decel_increment
            self.LeftSpeedPWM.value = speed / self.decel_increment
            sleep(self.decel_time / d)
            print(self.RightSpeedPWM.value)

    def accel_decel_decorator(function):
        def wrapper(self):
            self.accel()
            self.decel()

        return wrapper

    def accel_decorator(function):
        def wrapper(self):
            self.accel()

        return wrapper

    def decel_decorator(function):
        def wrapper(self):
            self.decel()

        return wrapper

    @do_record_travel
    @accel_decel_decorator
    def goForward(self, **kwargs):
        self.RightForward.on()
        self.LeftForward.on()

    @do_record_travel
    @accel_decel_decorator
    def goBackward(self):
        self.RightBackward.on()
        self.LeftBackward.on()

    @do_not_record_travel
    def spinRight(self):
        self.RightBackward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_not_record_travel
    def spinLeft(self):
        self.RightForward.on()
        self.LeftBackward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_record_travel
    def turnForwardRight(self):
        self.RightForward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.low_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_record_travel
    def turnForwardLeft(self):
        self.RightForward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.low_speed

    @do_record_travel
    def turnBackwardRight(self):
        self.RightBackward.on()
        self.LeftBackward.on()
        self.RightSpeedPWM.value = self.low_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_record_travel
    def turnBackwardLeft(self):
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

    # End driving functions --------------------------------------------- #
