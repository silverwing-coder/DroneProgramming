import RPi.GPIO as GPIO
import time

# Pull-Up Switch: (In Pin + Switch-A) (+) Switch-B --> Ground  
# 3.3 v --> Register connection is internally established by code

delay = 0.1
inPin = 29
outPin = 31

GPIO.setmode(GPIO.BOARD)
GPIO.setup(inPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(outPin, GPIO.OUT)

try:
    while True:
        if GPIO.input(inPin):
            print(GPIO.input(inPin))
            GPIO.output(outPin, 1)
        else:
            print(GPIO.input(inPin))
            GPIO.output(outPin, 0)
        time.sleep(delay)

except KeyboardInterrupt:
    GPIO.cleanup()
    print('LED flip with switch finished!')
