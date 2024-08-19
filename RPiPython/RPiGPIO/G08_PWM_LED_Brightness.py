import RPi.GPIO as GPIO
import time

holdTime = 0.1
upBtnPin = 29
dnBtnPin = 31
outPin = 33

GPIO.setmode(GPIO.BOARD)
GPIO.setup(upBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dnBtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(outPin, GPIO.OUT)

# Output test
# GPIO.output(outPin, 1)
# time.sleep(1)

frequency = 1000
duty_cycle = 99
myPWM = GPIO.PWM(outPin, frequency)
myPWM.start(duty_cycle)

upBtn = 1
upBtnOld = 1
dnBtn = 1
dnBtnOld = 1


##### full bright: 10 times button push 
# 100 = x ^ 10 --> log x = log 100 / 10 --> x = 10 ^ 0.2 = 1.5849
push_count = 10

try:
    while True:
        upBtn = GPIO.input(upBtnPin)
        if upBtn == 1 and upBtnOld == 0:
            # duty_cycle += 10      # linear scale
            # duty_cycle *= 2         # exponential scale
            push_count += 1
            duty_cycle = int(pow(1.5849, push_count))
            # if duty_cycle < 76:
            #     duty_cycle += 20
        upBtnOld = upBtn

        dnBtn = GPIO.input(dnBtnPin)
        if dnBtn == 1 and dnBtnOld == 0:
            # duty_cycle -= 10      # linear scale
            # duty_cycle = int(duty_cycle / 2)         # exponential scale
            
            push_count -= 1
            duty_cycle = int(pow(1.5849, push_count))
            # if duty_cycle > 15:
            #     duty_cycle -= 20
        dnBtnOld = dnBtn
        
        if(duty_cycle > 99):
            duty_cycle = 99
        if duty_cycle < 1:
            duty_cycle = 1

        myPWM.ChangeDutyCycle(duty_cycle)
        print(duty_cycle)
        time.sleep(holdTime)

except KeyboardInterrupt:
    myPWM.stop()
    GPIO.cleanup()
    print('End: GPIO cleaned!')



