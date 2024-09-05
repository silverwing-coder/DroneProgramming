from gpiozero import LEDCharDisplay
from time import sleep

display = LEDCharDisplay(12, 16, 20, 21, 5, 6, 13, dp = 19)
for char in '12345':
    display.value = char
    sleep(3)

display.off()