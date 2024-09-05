from gpiozero import RGBLED
from time import sleep

led = RGBLED(red=5, green=6, blue=13)

# led.red = 1
# sleep(3)
# led.red = 0.5
# sleep(3)

led.color = (1, 0, 0)  # full green
sleep(3)
led.color = (0, 1, 0)  # magenta
sleep(3)
led.color = (0, 0, 1)  # yellow
sleep(3)
led.color = (1, 1, 0)  # cyan
sleep(3)
led.color = (1, 0, 1)  # white
sleep(3)
led.color = (1, 1, 1)  # off
sleep(3)
led.color = (0, 1,1)  # off
sleep(3)

# for n in range(100):
#     led.blue = n/100
#     sleep(0.1)

