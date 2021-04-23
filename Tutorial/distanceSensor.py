from gpiozero import DistanceSensor, LED, RGBLED
from time import sleep
from signal import pause

sensor = DistanceSensor(23, 24)
led = RGBLED(red=16, green=20, blue=21)

# to do
# add rgbled and have it change color depending on moving towards/away/not


threshold = 0.05


def get_distance(sensor):
    d0 = sensor.distance
    sleep(0.5)
    d1 = sensor.distance
    return d1 - d0


# the funtions in each if statement aren't
# working right...
def main():
    while True:
        delta = get_distance(sensor)
        if delta < -threshold:
            led.color = (0, 0, 1)
        elif delta > threshold:
            led.color = (0, 1, 0)
        else:
            led.color = (1, 0, 0)


if __name__ == "__main__":
    main()
