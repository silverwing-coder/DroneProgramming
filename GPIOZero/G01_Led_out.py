from gpiozero import LED, OutputDevice
# import gpiozero as io
from signal import pause
import time

pin = 17
# led = LED(pin)
led = OutputDevice(pin)

## blink option-1
# led.blink()
# pause()

# blink option-2
while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)


# birghtness control
