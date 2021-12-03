"""minute_demo.py

Runs all usable features of the Rover at once.
Drives and collects data in a timeframe, then stops.
"""

from rover import Rover
from time import sleep
from multiprocessing import Process


def minute_loop():
    t = 50
    print(f"Timer Loop: {t} seconds")
    sleep(t)


def minute_drive(rover):
    while True:
        print('Driving Loop: driving "autonomously"')
        rover.goForward()
        sleep(0.5)
        rover.spinRight()
        sleep(1.5)


def minute_sense(rover):
    while True:
        print("Environmental Sensor Loop: reading environmental conditions")
        data = rover.create_data()
        rover.upload_data(data)
        rover.download_data()
        sleep(rover.upload_frequency)


if __name__ == "__main__":
    rover = Rover()
    loop = Process(target=minute_loop)
    drive = Process(target=minute_drive, args=(rover,))
    sense = Process(target=minute_sense, args=(rover,))
    loop.start()
    drive.start()
    sense.start()

    while True:
        if not loop.is_alive():
            drive.terminate()
            sense.terminate()
            break
