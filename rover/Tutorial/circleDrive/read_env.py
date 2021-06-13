from rover import Rover
from time import sleep
from dotenv import load_dotenv
load_dotenv()
print(load_dotenv())
rover = Rover()

while True:
    print(rover.get_humidity())
    print(rover.get_temperature())
    sleep(1)