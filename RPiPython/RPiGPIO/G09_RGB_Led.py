import RPi.GPIO as GPIO
import time

redPin = 29
greenPin = 37
bluePin = 23

GPIO.setmode(GPIO.BOARD)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)

GPIO.output(redPin, 1)
GPIO.output(greenPin, 0)
GPIO.output(bluePin, 0)
time.sleep(3)
GPIO.output(redPin, 0)
GPIO.output(greenPin, 1)
GPIO.output(bluePin, 0)
time.sleep(3)
GPIO.output(redPin, 0)
GPIO.output(greenPin, 1)
GPIO.output(bluePin, 1)
time.sleep(3)


GPIO.cleanup()