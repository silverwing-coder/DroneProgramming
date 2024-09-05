from gpiozero import LED, Button
from signal import pause
# import time

led = LED(17)
button = Button(2)

# while True:
#     button.when_pressed = led.on
#     button.when_released = led.off

button.when_pressed = led.on
button.when_released = led.off
    
# led.source = button

pause()


