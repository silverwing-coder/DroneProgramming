###
# VCC: 5 volt
# OUT: GPIO
# GND: GND

import RPi.GPIO as GPIO
import time
# from time import sleep

GPIO.setmode(GPIO.BOARD)
motionPin = 8

GPIO.setup(motionPin, GPIO.IN)
time.sleep(10)

try:
    while True:
        # pass
        motion = GPIO.input(motionPin)
        print(motion)
        time.sleep(.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print('GPIO cleaned up.')
