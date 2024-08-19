import RPi.GPIO as GPIO
import time

###
# Pull-Up Switch: 3.3 v --> Register --> (In Pin + Switch-A) (+) Switch-B --> Ground  
# Pull-Down Switch: 3.3 v -->Switch-B (+) Ground --> Register --> (In Pin + Switch-A)


GPIO.setmode(GPIO.BOARD)

GPIO.setup(29, GPIO.IN)
GPIO.setup(31, GPIO.OUT)

try:
    while True:
        if GPIO.input(29):
            # GPIO.output(31, GPIO.HIGH)
            GPIO.output(31, 1)
        else: 
            # GPIO.output(31, GPIO.LOW)
            GPIO.output(31, 0)

except KeyboardInterrupt:
    GPIO.cleanup()
    print('LED controm with switch finished!')
