from gpiozero import LED, Button
from signal import pause

led = LED(17)
button = Button(2)

button.when_pressed = switch

def switch():
    ~led.is_active

pause()
