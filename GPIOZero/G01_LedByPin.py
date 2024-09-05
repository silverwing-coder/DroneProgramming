from gpiozero import OutputDevice
from time import sleep

led = OutputDevice(17)
led.on()
sleep(3)
led.off()

