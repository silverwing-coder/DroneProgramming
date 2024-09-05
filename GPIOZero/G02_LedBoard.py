from gpiozero import LEDBoard
from time import sleep
from signal import pause

leds = LEDBoard(5, 6, 13, 19, 26)
leds.on()
sleep(3)
leds.off()
sleep(3)
leds.value = (1, 0, 1, 0, 1)
sleep(3)
leds.blink()

pause()