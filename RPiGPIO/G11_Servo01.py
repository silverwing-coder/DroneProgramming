### Servo specification  ###
# Pins Lay out:  Red --> power (3.3 v), Brown --> ground, Orange --> control (pwm signal)
# Period = 20 mSec = .02 second --> frequency = 50 Hz
# Duty Cycle:   1 ~ 2 %  --> 0 degree
#               10 ~ 15 % --> 18 degree


import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BOARD)

pwmPin = 7      # BCM mode

GPIO.setup(pwmPin, GPIO.OUT)

freqency = 50       # period = 20 mSec
pwm = GPIO.PWM(pwmPin, freqency)
pwm.start(0)

try:
    while True:
        # pass
        dutyCycle = float(input('Enter PWM %: '))
        pwm.ChangeDutyCycle(dutyCycle)
        print(dutyCycle)
        time.sleep(.1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print('GPIO cleaned up.')