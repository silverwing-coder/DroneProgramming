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

ledState = 0
switchNow = 1
switchPrev = 1

try:
    while True:
        switchNow = GPIO.input(inPin)
        # print(switchNow)
        # print(switchPrev)

        if switchNow == 1 and switchPrev == 0:
            ledState = not ledState
            GPIO.output(outPin, ledState)   # output does not change until the condition meets
        switchPrev = switchNow

        time.sleep(delay)

except KeyboardInterrupt:
    GPIO.cleanup()
    print('LED flip with switch finished!')
