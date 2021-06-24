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
    RIGHTBACKWARD=DigitalOutputDevice(5)
    RIGHTFORWARD=DigitalOutputDevice(6)
    RIGHTSPEEDPWM=PWMOutputDevice(13)
    LEFTBACKWARD=DigitalOutputDevice(16)
    LEFTFORWARD=DigitalOutputDevice(20)
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

class Directories(Enum):

    DATA_DIRECTORY='atmosphere-sensor-data'
    OUTPUT_FILE='atmosphere-sensor-data.json'

class Sheets_Enums(Enum):
    AUTH_FILE='credentials.json'
    # SPREADSHEET_NAME='env_data'
    SPREADSHEET_NAME='community_env_data'
    DEFAULT_SCOPE=[
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
            ]
    DEFAULT_COLUMNS=[
                "ID",
                "Timestamp",
                "Temperature",
                "Humidity",
                "Light",
                "Distance",
            ]
    NULL_VALUES = ['', None, 'NA', 'N/A', 'na', 'n/a', '\n', 'None', 'none', 'NULL', 'Null', 'null', False]