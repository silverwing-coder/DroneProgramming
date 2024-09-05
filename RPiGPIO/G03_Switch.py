import RPi.GPIO as GPIO
import time

###
# Pull-Up Switch: 3.3 v --> Register --> (In Pin + Switch-A) (+) Switch-B --> Ground  
# Pull-Down Switch: 3.3 v -->Switch-B (+) Ground --> Register --> (In Pin + Switch-A)


GPIO.setmode(GPIO.BOARD)

GPIO.setup(29, GPIO.IN)

try:
    while True:

        print(GPIO.input(29))
        time.sleep(0.5)   
except KeyboardInterrupt:
    GPIO.cleanup()
