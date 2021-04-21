#make a class with all my functions within it

from rover import Rover
from time import sleep
def main():

    rover = Rover()            
    print("forward")
    rover.goForward()
    sleep(1.5)
    print(rover.travel)
    print('right')
    rover.spinRight()
    sleep(1.5)
    print(rover.travel)
    print('forward')
    rover.goForward()
    sleep(1.5)
    print(rover.travel)
    rover.stop()
    print(rover.travel)
    print(f"Rover traveled {round(rover.travel/20*rover.wheel_diameter, 2)}m")

if __name__=="__main__":
    main()
