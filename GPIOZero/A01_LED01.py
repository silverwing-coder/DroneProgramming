from gpiozero import LED
from time import sleep

pin = 17
led = LED(pin)

count = 10
while count > 0:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
    count = count - 1
