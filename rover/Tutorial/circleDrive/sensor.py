import os
import adafruit_dht
import board
from gpiozero import LightSensor

class Sensor:
        
    def __init__(self):
        super(Sensor, self).__init__()
        self.temp_units = os.getenv("TEMPUNITS")
        self.humidity_units = os.getenv("HUMIDITY")

        self.LightSensor = LightSensor(os.getenv("LIGHTSENSOR"))
        self.DHTSensor = self.create_dht_sensor(pin=os.getenv("ATMOSPHERESENSOR"))


    def create_dht_sensor(self, pin):
        exec(f'sensor = adafruit_dht.DHT11(board.{pin}, use_pulseio=False)', None, globals())
        return sensor

    def sense_light(self):
        print(LightSensor)
        print(dir(LightSensor))
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