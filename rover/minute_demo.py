import sys
from rover import Rover
from time import sleep
from multiprocessing import Process


def minute_loop():
    sleep(60)


def minute_drive(rover):
    while True:
        rover.goForward()
        sleep(1.5)
        rover.spinRight()
        sleep(1.5)


def minute_sense(rover):
    while True:
        data = rover.create_data()
        rover.upload_data(data)
        rover.download_data()
        sleep(rover.upload_frequency)


if __name__ == "__main__":
    loop = Process(target=minute_loop)
    drive = Process(target=minute_drive)
    sense = Process(target=minute_sense)
    loop.start()
    drive.start()
    sense.start()

    while True:
        if not loop.is_alive():
            drive.terminate()
            sense.terminate()
            break
