

### Schematic
'''
Pin 2(SDA1) --> button-in
button-out --> GND
'''

import gpiozero as io
from gpiozero import LED
import time
from signal import pause

btn = io.Button(17)
led = LED(26)

### option-1: check if button is pressed
while True:
    if(btn.is_pressed):
        print('Button is pressed')
        led.on()
        time.sleep(.5)
    else:
        print('Button is NOT pressed')
        led.off()
        time.sleep(.5)

### option-2: wait for a button to be pressed before continuing
# btn.wait_for_active()
# print("Button was pressed")
# pause() // not work

### option-3: run a function every time butten is pressed
# def say_hello():
#     print("Hello, button activated.")

# btn.when_activated = say_hello
# pause()