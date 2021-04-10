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

low_speed = .25
high_speed = .9
t = .5


class Distance():
    distance = 0
rover_distance = Distance()

def add_distance(Distance):
    Distance.distance += 1
    if Distance.distance % 10 == 0:
        print(Distance.distance)
def turnForwardRight():
    RightForward.on()
    LeftForward.on()

    RightBackward.off()
    LeftBackward.off()

    RightSpeedPWM.value = high_speed
    LeftSpeedPWM.value = low_speed

def turnForwardLeft():
    RightForward.on()
    LeftForward.on()

    RightBackward.off()
    LeftBackward.off()

    RightSpeedPWM.value = low_speed
    LeftSpeedPWM.value = high_speed

def turnBackwardRight():
    RightForward.off()
    LeftForward.off()

    RightBackward.on()
    LeftBackward.on()

    RightSpeedPWM.value = high_speed
    LeftSpeedPWM.value = low_speed

def turnBackwardLeft():
    RightForward.off()
    LeftForward.off()

    RightBackward.on()
    LeftBackward.on()

    RightSpeedPWM.value = low_speed
    LeftSpeedPWM.value = high_speed

def stop():
    RightForward.off()
    LeftForward.off()

    RightBackward.off()
    LeftBackward.off()

    RightSpeedPWM.value = 0
    LeftSpeedPWM.value = 0
while True:
    turnForwardLeft()
    sleep(t)
    turnBackwardRight()
    sleep(t)
    turnForwardLeft()
    sleep(t)
    turnBackwardRight()
    sleep(t)
    stop()
    sleep(t)
    Encoder.when_pressed = lambda: add_distance(rover_distance)
