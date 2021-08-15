import sys
from rover import Rover
from time import sleep
from multiprocessing import Process


def minute_loop():
    print("time loop")
    sleep(50)


def minute_drive(rover):
    while True:
        print("drive loop")
        rover.goBackward()
        sleep(.5)
        rover.spinRight()
        sleep(1.5)


def minute_sense(rover):
    while True:
        print("sense loop")
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
