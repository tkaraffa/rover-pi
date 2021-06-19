import os
from gpiozero import PWMOutputDevice, DigitalOutputDevice, Button, DistanceSensor
from time import sleep
import random
from dotenv import load_dotenv

load_dotenv()

import warnings
warnings.filterwarnings("ignore")

class Vehicle:

    def __init__(self):
        super(Vehicle, self).__init__()
        # Values
        self.low_speed = float(os.getenv("LOWSPEED"))
        self.high_speed = float(os.getenv("HIGHSPEED"))
        self.turn_time = float(os.getenv("TURNTIME"))
        self.wheel_diameter = float(os.getenv("WHEELDIAMETER"))

        # Pins
        self.RightForward = DigitalOutputDevice(os.getenv("RIGHTFORWARD"))
        self.RightBackward = DigitalOutputDevice(os.getenv("RIGHTBACKWARD"))
        self.RightSpeedPWM = PWMOutputDevice(os.getenv("RIGHTSPEEDPWM"))
        self.LeftForward = DigitalOutputDevice(os.getenv("LEFTFORWARD"))
        self.LeftBackward = DigitalOutputDevice(os.getenv("LEFTBACKWARD"))
        self.LeftSpeedPWM = PWMOutputDevice(os.getenv("LEFTSPEEDPWM"))
        self.RotaryEncoder = Button(os.getenv("ROTARYENCODER"))
        self.DistanceSensor = DistanceSensor(echo=os.getenv("ECHO"), trigger=os.getenv("TRIG"))

        # default values
        self.record_travel = True
        self.travel = 0
        self.accel_increment = 100
        self.decel_increment = 100
        self.accel_time = 5
        self.decel_time = 5
        self.DistanceSensor.threshold = 0.5

        # assign functions to sensors
        self.RotaryEncoder.when_pressed = self.add_travel
        self.DistanceSensor.when_in_range = self.change_direction

    def sense_distance(self):
        print(self.DistanceSensor.distance)
        print(self.DistanceSensor.value)
        return self.DistanceSensor.distance

    def add_travel(self):
        if self.record_travel == True:
            self.travel += 1

    def change_direction(self):
        choice = random.choice([self.spinLeft, self.spinRight, self.turnLeft, self.turnRight])
        choice()

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

    def accel(self, time=None):
        if not time:
            time = self.accel
        max_speed = int(self.high_speed * self.accel_increment)
        min_speed = int(self.low_speed * self.accel_increment)
        speed_delta = max_speed - min_speed
        for speed in range(min_speed, max_speed):
            self.RightSpeedPWM.value = speed / self.accel_increment
            self.LeftSpeedPWM.value = speed / self.accel_increment
            sleep(time / speed_delta)

    def decel(self, time=None):
        if not time:
            time = self.decel_time
        max_speed = int(self.high_speed * self.decel_increment) # 90
        min_speed = int(self.low_speed * self.decel_increment) # 20 
        speed_delta = max_speed - min_speed
        for speed in reversed(range(min_speed, max_speed)):
            self.RightSpeedPWM.value = speed / self.decel_increment
            self.LeftSpeedPWM.value = speed / self.decel_increment
            sleep(time / speed_delta)

    def accel_decel_decorator(function):
        def wrapper(self):
            function(self)
            self.accel()
            self.decel()

        return wrapper

    def accel_decorator(function):
        def wrapper(self):
            function(self)
            self.accel()

        return wrapper

    def decel_decorator(function):
        def wrapper(self):
            function(self)
            self.decel()

        return wrapper

    @do_record_travel
    @accel_decel_decorator
    def goForward(self):
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
