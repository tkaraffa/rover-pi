from rover import Rover
from time import sleep
from dotenv import load_dotenv
import os
load_dotenv()
print(load_dotenv())
print(os.environ)
rover = Rover()

while True:
    print(rover.get_humidity())
    print(rover.get_temperature())
    sleep(1)