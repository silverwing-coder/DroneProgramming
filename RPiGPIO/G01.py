###
# Install the python RPi.GPIO library if necessary. (Don't have to)
# $ sudo apt-get install python-rpi.gpio

### 
# Recent Raspberry PI OS include python RPi.GPIO library

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
# BCM: Use Broadcom Channel Mode pinout
# BOARD: Use board pinout
GPIO.setup(17, GPIO.OUT)

GPIO.output(17, GPIO.HIGH)
time.sleep(5)
GPIO.output(17, GPIO.LOW)

GPIO.cleanup()