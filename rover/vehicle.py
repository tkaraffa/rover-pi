import sys

sys.path.append("/home/pi/rover-pi")

from config.rover_enums import Pins, Constants
from time import sleep
import random


class Vehicle:
    """Class for driving around and having fun.

    Attributes
    ----------
    Constant values:
        Constants for turning and driving
    Pins:
        GPIO pins corresponding to gpiozero classes for input/output
    default_values:
        values associated with recording movement, distance traveled, and
        sensing distance
    functions:
        gpiozero functions associated with changing direction and recording
        traveled distance
    """

    def __init__(self):
        super(Vehicle, self).__init__()
        # Constant Values
        self.low_speed = Constants.LOWSPEED.value
        self.high_speed = Constants.HIGHSPEED.value
        self.turn_time = Constants.TURNTIME.value
        self.wheel_diameter = Constants.WHEELDIAMETER.value

        # Pins
        self.RightForward = Pins.RIGHTFORWARD.value
        self.RightBackward = Pins.RIGHTBACKWARD.value
        self.RightSpeedPWM = Pins.RIGHTSPEEDPWM.value
        self.LeftForward = Pins.LEFTFORWARD.value
        self.LeftBackward = Pins.LEFTBACKWARD.value
        self.LeftSpeedPWM = Pins.LEFTSPEEDPWM.value
        self.RotaryEncoder = Pins.ROTARYENCODER.value
        self.DistanceSensor = Pins.DISTANCESENSOR.value

        # default values
        self.record_travel = True
        self.travel = 0
        self.clockwise_rotation = 0
        self.counterclockwise_rotation = 0
        self.accel_increment = 100
        self.decel_increment = 100
        self.accel_time = 5
        self.decel_time = 5
        self.DistanceSensor.threshold = 0.5

        # assign functions to sensors
        self.RotaryEncoder.when_pressed = self.add_travel
        self.DistanceSensor.when_in_range = self.change_direction

    def __del__(self):
        self.stop()

    def sense_distance(self):
        """Get value from Distance Sensor"""
        try:
            return self.DistanceSensor.distance
        except:
            return None

    def add_travel(self):
        """Depending on boolean, either record distance travelled,
        record clockwise rotation, or record counterclockwise roatation"""
        if self.record_travel == True:
            self.travel += 1
        if self.record_clockwise_rotation == True:
            self.clockwise_rotation += 1
        if self.record_counterclockwise_rotation == True:
            self.counterclockwise_rotation += 1

    def change_direction(self):
        """Randomly choose a function to avoid an obstacle
        used for 'when_in_range' method of the distance sensor
        """
        choice = random.choice(
            [self.spinLeft, self.spinRight, self.turnLeft, self.turnRight]
        )
        choice()

    def stop(self):
        "Stop all movement"
        self.RightForward.off()
        self.LeftForward.off()
        self.RightBackward.off()
        self.LeftBackward.off()
        self.RightSpeedPWM.value = 0
        self.LeftSpeedPWM.value = 0

    def do_record_travel(function):
        "Start recording travel"

        def wrapper(self):
            self.record_travel = True
            self.stop()
            function(self)

        return wrapper

    def do_not_record_travel(function):
        "Stop recording travel"

        def wrapper(self):
            self.record_travel = False
            self.stop()
            function(self)

        return wrapper

    def accel(self, time=None):
        if not time:
            time = self.accel_time
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
        max_speed = int(self.high_speed * self.decel_increment)  # 90
        min_speed = int(self.low_speed * self.decel_increment)  # 20
        speed_delta = max_speed - min_speed
        for speed in reversed(range(min_speed, max_speed)):
            self.RightSpeedPWM.value = speed / self.decel_increment
            self.LeftSpeedPWM.value = speed / self.decel_increment
            sleep(time / speed_delta)

    def accel_decel_decorator(function):
        """Decorator to accelerate, then decelerate while moving."""

        def wrapper(self):
            function(self)
            self.accel()
            self.decel()

        return wrapper

    def accel_decorator(function):
        """Decorator to accelerate over time."""

        def wrapper(self):
            function(self)
            self.accel()

        return wrapper

    def decel_decorator(function):
        """Decorator to decelerate over time."""

        def wrapper(self):
            function(self)
            self.decel()

        return wrapper

    @do_record_travel
    @accel_decel_decorator
    def goForward(self):
        "Move the Rover forward."
        self.RightForward.on()
        self.LeftForward.on()

    @do_record_travel
    @accel_decel_decorator
    def goBackward(self):
        "Move the Rover backward."
        self.RightBackward.on()
        self.LeftBackward.on()

    @do_not_record_travel
    def spinRight(self):
        "Spin the Rover to the right in place."
        self.RightBackward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_not_record_travel
    def spinLeft(self):
        "Spin the jrover to the left in place."
        self.RightForward.on()
        self.LeftBackward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_record_travel
    def turnForwardRight(self):
        "Moves the Rover forward and to the right in an arc."
        self.RightForward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.low_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_record_travel
    def turnForwardLeft(self):
        "Moves the Rover forward and to the left in an arc."
        self.RightForward.on()
        self.LeftForward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.low_speed

    @do_record_travel
    def turnBackwardRight(self):
        "Moves the Rover backward and to the right in an arc."
        self.RightBackward.on()
        self.LeftBackward.on()
        self.RightSpeedPWM.value = self.low_speed
        self.LeftSpeedPWM.value = self.high_speed

    @do_record_travel
    def turnBackwardLeft(self):
        "Moves the Rover backward and to the left in an arc."
        self.RightBackward.on()
        self.LeftBackward.on()
        self.RightSpeedPWM.value = self.high_speed
        self.LeftSpeedPWM.value = self.low_speed

    @do_not_record_travel
    def turnRight(self):
        "Performs a 5-point turn to face to the right."
        for _ in range(2):
            self.turnForwardRight()
            sleep(self.turn_time)
            self.turnBackwardLeft()
            sleep(self.turn_time)

    @do_not_record_travel
    def turnLeft(self):
        "Performs a 5-point turn to face to the left."
        for _ in range(2):
            self.turnForwardLeft()
            sleep(self.turn_time)
            self.turnBackwardRight()
            sleep(self.turn_time)
