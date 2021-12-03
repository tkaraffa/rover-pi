import sys

sys.path.append("/home/pi/rover-pi")

from config.rover_enums import Pins


class Sensor:
    """Class for reading environmental sensor data.

    Attributes
    ----------
    LightSensor: gpiozero.LightSensor
        Light Sensor class for measuring light
        from a photoreceptor.

    DHTSensor: adafruit_dht.DHT11
        DHT Sensor class for meaasuring humidity
        and temperature from a DHT sensor.
    """

    def __init__(self) -> None:
        super(Sensor, self).__init__()

        # pins
        self.LightSensor = Pins.LIGHTSENSOR.value
        self.DHTSensor = Pins.ATMOSPHERESENSOR.value

    def sense_light(self) -> float:
        """Obtains current light reading
        from the light sensor.

        Returns
        -------
        light: float
            The current light reading
        """
        return self.LightSensor.value

    def sense_humidity(self) -> float:
        """Obtains current humidity reading
        from the DHT sensor.

        Returns
        -------
        humidity: float
            The current humidity reading

        Raises
        ------
        RuntimeError
            in the case of a checksum failure, or if
            the reading returns insufficient data
        """
        try:
            return self.DHTSensor.humidity
        except RuntimeError:
            return None

    def sense_temperature(self) -> float:
        """Obtains current temperature reading
        from the DHT sensor.

        Returns
        -------
        temperature: float
            The current temperature reading

        Raises
        ------
        RuntimeError
            in the case of a checksum failure, or if
            the reading returns insufficient data
        """
        try:
            return self.DHTSensor.temperature
        except RuntimeError:
            return None
