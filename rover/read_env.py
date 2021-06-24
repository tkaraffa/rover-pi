from rover import Rover
from time import sleep

def main():
    rover = Rover()
    while True:
        data = rover.create_data()
        rover.upload_data(data)
        sleep(rover.upload_frequency)

if __name__=="__main__":
    main()