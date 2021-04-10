from configparser import ConfigParser
import os
from gpiozero import PWMOutputDevice, DigitalOutputDevice, Button, DistanceSensor
import Adafruit_DHT
import subprocess
from time import sleep

def get_device_id():
    bash_command = "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2"
    byte = subprocess.run(bash_command, shell=True, capture_output=True).stdout
    output = byte.decode("utf-8").strip()
    return output

def get_config_path(ini_file="rover.ini"):
    return os.path.join(os.path.dirname(__file__), ini_file)

class Rover:
    def __init__(self):
        self.config_path = get_config_path()
        self.device_id = get_device_id()

        self.low_speed = .4
        self.high_speed = .9
        self.turn_time = .7

        self.wheel_diameter = .203

        self.distance = 0
        self.temp = 0
        self.humidity = 0
        self.directory_string = 'atmosphere-sensor-data'
        self.file_string = 'atmosphere-sensor-data'
        self.temp_units = "*C"
        self.humidity_units = "%"

        config = ConfigParser()
        config.read(self.config_path)
        pinout = config["Rover"]

        self.RightForward = DigitalOutputDevice(pinout["RIGHTFORWARD"])
        self.RightBackward = DigitalOutputDevice(pinout["RIGHTBACKWARD"])
        self.RightSpeedPWM = PWMOutputDevice(pinout["RIGHTSPEEDPWM"])
        self.LeftForward = DigitalOutputDevice(pinout["LEFTFORWARD"])
        self.LeftBackward = DigitalOutputDevice(pinout["LEFTBACKWARD"])
        self.LeftSpeedPWM = PWMOutputDevice(pinout["LEFTSPEEDPWM"])
        self.RotaryEncoder = Button(pinout["ROTARYENCODER"])
        #self.DistanceSensor = DistanceSensor(pinout["DISTANCESENSOR"])

        self.DHT_SENSOR = Adafruit_DHT.DHT11
        self.DHT_PIN = pinout["ATMOSPHERESENSOR"]


    def add_distance(self, distance):
        self.distance += 1
        if self.distance % 10 == 0:
            print(self.distance)

    def stop(self):
        self.RightForward.off()
        self.LeftForward.off()
        self.RightBackward.off()
        self.LeftBackward.off()
        self.RightSpeedPWM.value = 0
        self.LeftSpeedPWM.value = 0

    def goForward(self):
        self.stop()
        self.RightForward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.high_speed

    def goBackward(self):
        self.stop()
        self.RightBackward.on()
        self.LeftBackward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.high_speed

    def spinRight(self):
        self.stop()
        self.RightBackward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.high_speed

    def spinLeft(self):
        self.stop()
        self.RightForward.on()
        self.LeftBackward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.high_speed

    def turnForwardRight(self):
        self.stop()
        self.RightForward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.low_speed
        self.LeftSpeedPWM.value = self.high_speed

    def turnForwardLeft(self):
        self.stop()
        self.RightForward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.low_speed

    def turnBackwardRight(self):
        self.stop()
        self.RightBackward.on()
        self.LeftBackward.on()
        self.RightSpeedPWM.value = self.low_speed
        self.LeftSpeedPWM.value = self.high_speed

    def turnBackwardLeft(self):
        self.stop()
        self.RightBackward.on()
        self.LeftBackward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.low_speed

    def turnRight(self):
        for i in range(2):
            self.turnForwardRight()
            sleep(self.turn_time)
            self.turnBackwardLeft()
            sleep(self.turn_time)

    def turnLeft(self):
        for i in range(2):
            self.turnForwardLeft()
            sleep(self.turn_time)
            self.turnBackwardRight()
            sleep(self.turn_time)

    def setup(self):
        self.RotaryEncoder.when_pressed = self.add_distance
        #self.humidity, self.temp = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
