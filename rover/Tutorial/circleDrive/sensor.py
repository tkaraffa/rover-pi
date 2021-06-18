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
        self.DHTSensor = self.create_dht_sensor(os.getenv("ATMOSPHERESENSOR"))

        self.temp = 0
        self.humidity = 0

    def create_dht_sensor(self, pin):
        exec(f'sensor = adafruit_dht.DHT11(board.{pin}, use_pulseio=False)', None, globals())
        return sensor

    def sense_light(self):
        try:
            return self.LightSensor.value
        except:
            None

    def sense_humidity(self):
        print(self.DHTSensor.humidity)
        try:
            return self.DHTSensor.humidity
        except:
            print("coundnt get humidity")
            return None

    def sense_temperature(self):
        try:
            return self.DHTSensor.temperature
        except:
            print('couldnt get temp')
            return None