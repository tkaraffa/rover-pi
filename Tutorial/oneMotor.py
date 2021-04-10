#onemotor.py
#mod from https://core-electronics.com.au/tutorials/how-to-control-a-motor-with-the-raspberry-pi.html

from gpiozero import PWMOutputDevice, Button
from gpiozero import DigitalOutputDevice
from time import sleep

#setup pins
RightBackward = DigitalOutputDevice(5) # On/Off output
RightForward = DigitalOutputDevice(6) #On/Off output
RightSpeedPWM = PWMOutputDevice(13) # set up PWM pin
LeftBackward = DigitalOutputDevice(16)
LeftForward = DigitalOutputDevice(20)
LeftSpeedPWM = PWMOutputDevice(21)
Encoder = Button(26)

class Distance():
    distance = 0
rover_distance = Distance()

def add_distance(Distance):
    Distance.distance += 1
    if Distance.distance % 10 == 0:
        print(Distance.distance)

while True:
    directionFlag = input("set motor direction: ")
    if directionFlag == "back": # if user types "back" go backward
        RightBackward.on() # Sets Backward Direction pin on
        LeftBackward.on()
        RightForward.off() # Sets Forward Direction pin off
        LeftForward.off()
    elif directionFlag == "forward":
        RightBackward.off() # Sets Backward Direction off
        LeftBackward.off()
        RightForward.on()   # Sets Forward Direction pin on
        LeftForward.on()
    else:
        RightBackward.off()
        Lef
    speedFlag = float(input("set speed (between 0-1000): ")) # Gets a number from the from the user
    Encoder.when_pressed = lambda: add_distance(rover_distance)
    RightSpeedPWM.value = speedFlag/1000 # Sets the duty cycle of the PWM between 0-1
    LeftSpeedPWM.value = speedFlag/1000
