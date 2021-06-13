# from rover import Rover
from time import sleep

rover = Rover()

while True:
    print(rover.get_humidity())
    print(rover.get_temperature())
    sleep(1)