import RPi.GPIO as GPIO
import time

delay = 0.1

rPin = 29
gPin = 37
bPin = 23

rSwitch = 40
gSwitch = 38
bSwitch = 36

GPIO.setmode(GPIO.BOARD)
GPIO.setup(rPin, GPIO.OUT)
GPIO.setup(gPin, GPIO.OUT)
GPIO.setup(bPin, GPIO.OUT)

GPIO.setup(rSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(bSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

rState = 0
rBtn = 1
rBtnOld = 1

gState = 0
gBtn = 1
gBtnOld = 1

bState = 0
bBtun = 1
bBtnOld = 1

### output test ###
# GPIO.output(rPin, 1)
# time.sleep(3)
# GPIO.output(rPin, 0)
# GPIO.output(gPin, 1)
# time.sleep(3)
# GPIO.output(gPin, 0)
# GPIO.output(bPin, 1)
# time.sleep(3)
# GPIO.output(bPin, 0)
# GPIO.cleanup()

try:
    while True:
        rBtn = GPIO.input(rSwitch)
        # print('r:', rBtn)
        if rBtn == 1 and rBtnOld == 0:
            rState = not rState
            GPIO.output(rPin, rState)
            print('red btn push')
        # print('r:', rState)
        rBtnOld = rBtn

        gBtn = GPIO.input(gSwitch)
        # print('g:', gBtn)
        if gBtn == 1 and gBtnOld == 0:
            gState = not gState
            GPIO.output(gPin, gState)
            print('green btn push')
        # print('g:', gState)
        gBtnOld = gBtn


        bBtn = GPIO.input(bSwitch)
        # print('b:', bBtn)
        if bBtun == 1 and bBtnOld == 0:
            bState = not bState
            GPIO.output(bPin, bState)
            print('blue btn push')
        # print('b:', bState)
        bBtnOld = bBtn

        time.sleep(delay)

except KeyboardInterrupt:
    GPIO.cleanup()
    print('EXIT: GPIO cleaned!')
