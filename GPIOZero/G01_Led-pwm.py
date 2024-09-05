from gpiozero import PWMLED
import time

led = PWMLED(26)
while True:
    led.value = 0
    time.sleep(1)
    led.value = 0.5
    time.sleep(1)
    led.value = 1
    time.sleep(1)