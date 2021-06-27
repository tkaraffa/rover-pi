import sys
sys.path.append("/home/pi/rover-pi")

from config.rover_enums import Pins


class Sensor:
    def __init__(self):
        super(Sensor, self).__init__()

        # pins
        self.LightSensor = Pins.LIGHTSENSOR.value
        self.DHTSensor = Pins.ATMOSPHERESENSOR.value

    def sense_light(self):
        try:
            return self.LightSensor.value
        except:
            return None

    def sense_humidity(self):
        try:
            return self.DHTSensor.humidity
        except:
            return None

    def sense_temperature(self):
        try:
            return self.DHTSensor.temperature
        except:
            return None
