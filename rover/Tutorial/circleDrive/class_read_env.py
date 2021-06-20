from rover import Rover
from time import sleep

freq = 5

while True:
    data = rover.create_data()
    rover.upload_data(data)
    sleep(freq)