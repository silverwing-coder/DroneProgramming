import RPi.GPIO as GPIO
import time

outPin = 31

GPIO.setmode(GPIO.BOARD)
GPIO.setup(outPin, GPIO.OUT)

# GPIO.output(outPin, 1)
# time.sleep(1)
# GPIO.output(outPin, 0)
# time.sleep(1)
# GPIO.output(outPin, 1)
# time.sleep(1)
# GPIO.output(outPin, 0)
# time.sleep(1)
# GPIO.output(outPin, 1)
# time.sleep(1)
# GPIO.output(outPin, 0)
# time.sleep(1)

myPWM = GPIO.PWM(outPin, 100)   # frequncy of digital wave
# myPWM.start(90)                 # duty cycle: 90 %
# time.sleep(3)
# myPWM.stop(90)
# myPWM.start(70)                 # duty cycle: 70 %
# time.sleep(3)
# myPWM.stop(70)
# myPWM.start(50)                 # duty cycle: 50 %
# time.sleep(3)
# myPWM.stop(50)
# myPWM.start(30)                 # duty cycle: 30 %
# time.sleep(3)
# myPWM.stop(30)
# myPWM.start(10)                 # duty cycle: 10 %
# time.sleep(3)
# myPWM.stop(10)

# myPWM.ChangeDutyCycle(85)
# time.sleep(5)

myPWM.start(90)                 # duty cycle: 90 %
time.sleep(5)
myPWM.ChangeFrequency(10)
time.sleep(5)

GPIO.cleanup()

