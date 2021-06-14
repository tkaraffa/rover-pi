from rover import Rover
from time import sleep

rover = Rover()

while True:
    try:
        print(rover.get_humidity())
        print(rover.get_temperature())

    except:
        pass
    sleep(1)