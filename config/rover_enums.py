from enum import Enum

from adafruit_dht import DHT11
import board
from gpiozero import (
    LightSensor,
    PWMOutputDevice,
    DigitalOutputDevice,
    Button,
    DistanceSensor,
)

# Update the pins for your own rover
# Note that the atmosphere sensor uses the board & adafruit_dht libraries; the rest use gpiozero

class Pins(Enum):
    RIGHTBACKWARD=DigitalOutputDevice(6)
    RIGHTFORWARD=DigitalOutputDevice(5)
    RIGHTSPEEDPWM=PWMOutputDevice(13)
    LEFTBACKWARD=DigitalOutputDevice(20)
    LEFTFORWARD=DigitalOutputDevice(16)
    LEFTSPEEDPWM=PWMOutputDevice(21)
    ROTARYENCODER=Button(26)
    DISTANCESENSOR=DistanceSensor(echo=23, trigger=24)
    ATMOSPHERESENSOR=DHT11(board.D4, use_pulseio=False)
    LIGHTSENSOR=LightSensor(18)

class Constants(Enum):
    LOWSPEED=.5
    MIDSPEED=.7
    HIGHSPEED=.9
    TURNTIME=.7
    WHEELDIAMETER=.203
