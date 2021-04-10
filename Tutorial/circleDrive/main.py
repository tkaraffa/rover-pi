#make a class with all my functions within it

from rover import Rover
from time import sleep
def main():


    rover = Rover()
    rover.setup()
    t = rover.turn_time

    for i in range(4):
        rover.goForward()
        sleep(t/2)
        rover.spinRight()
        sleep(t)
    rover.stop()
    print(f"Rover traveled {round(rover.distance/20*rover.wheel_diameter, 2)}m")

if __name__=="__main__":
    main()
