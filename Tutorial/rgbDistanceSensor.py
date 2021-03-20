# python3
# raspberry pi uses distance sensor to change RGB LED color
# based on if object is moving towards or away from the sensor.
# Button used to toggle color template.

from gpiozero import DistanceSensor, RGBLED, Button
from time import sleep
from signal import pause

sensor = DistanceSensor(23, 24)
led = RGBLED(red=16, green=20, blue=21)
button = Button(2)

# 0: red, 1: green, 2: blue
colors1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

# 0: yellow, 1: magenta, 2: cyan
colors2 = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]

class ButtonState(): # real dumb workaround for the buttom press to toggle
    state = True
button_state = ButtonState()

# tweak these for performance
sleep_time = .25
threshold = .025

def change_button_state(button_state):
    button_state.state = not button_state.state

# measure, at intervals, how far away an object is from the sensor
def get_distance(sensor, sleep_time):
    d0 =  sensor.distance
    sleep(sleep_time)
    d1 = sensor.distance
    return d1-d0

def main():
    while True:
        # use button to toggle colors
        button.when_pressed = lambda: change_button_state(button_state)
        if button_state.state == True:
            colors = colors1
        else:
            colors = colors2

        # get change in distance
        delta = get_distance(sensor, sleep_time)
        if delta < -threshold: # towards sensor
            led.color = colors[0]
        elif delta > threshold: # away from sensor
            led.color = colors[1]
        else: # not moving
            led.color = colors[2]

if __name__ == "__main__":
    main()
