import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)

GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

#1
GPIO.output(29, GPIO.HIGH)
GPIO.output(31, GPIO.LOW)
GPIO.output(33, GPIO.LOW)
GPIO.output(35, GPIO.LOW)
GPIO.output(37, GPIO.LOW)
time.sleep(1)

#2
GPIO.output(29, GPIO.LOW)
GPIO.output(31, GPIO.HIGH)
GPIO.output(33, GPIO.LOW)
GPIO.output(35, GPIO.LOW)
GPIO.output(37, GPIO.LOW)
time.sleep(1)

#3
GPIO.output(29, GPIO.HIGH)
GPIO.output(31, GPIO.HIGH)
GPIO.output(33, GPIO.LOW)
GPIO.output(35, GPIO.LOW)
GPIO.output(37, GPIO.LOW)
time.sleep(1)

#4
GPIO.output(29, GPIO.LOW)
GPIO.output(31, GPIO.LOW)
GPIO.output(33, GPIO.HIGH)
GPIO.output(35, GPIO.LOW)
GPIO.output(37, GPIO.LOW)
time.sleep(1)

#5
GPIO.output(29, GPIO.HIGH)
GPIO.output(31, GPIO.LOW)
GPIO.output(33, GPIO.HIGH)
GPIO.output(35, GPIO.LOW)
GPIO.output(37, GPIO.LOW)
time.sleep(1)

#6
GPIO.output(29, GPIO.LOW)
GPIO.output(31, GPIO.HIGH)
GPIO.output(33, GPIO.HIGH)
GPIO.output(35, GPIO.LOW)
GPIO.output(37, GPIO.LOW)
time.sleep(1)

#7
GPIO.output(29, GPIO.HIGH)
GPIO.output(31, GPIO.HIGH)
GPIO.output(33, GPIO.HIGH)
GPIO.output(35, GPIO.LOW)
GPIO.output(37, GPIO.LOW)
time.sleep(1)

#8
GPIO.output(29, GPIO.LOW)
GPIO.output(31, GPIO.LOW)
GPIO.output(33, GPIO.LOW)
GPIO.output(35, GPIO.HIGH)
GPIO.output(37, GPIO.LOW)
time.sleep(1)

#16
GPIO.output(29, GPIO.LOW)
GPIO.output(31, GPIO.LOW)
GPIO.output(33, GPIO.LOW)
GPIO.output(35, GPIO.LOW)
GPIO.output(37, GPIO.HIGH)
time.sleep(3)

#20
GPIO.output(29, GPIO.LOW)
GPIO.output(31, GPIO.LOW)
GPIO.output(33, GPIO.HIGH)
GPIO.output(35, GPIO.LOW)
GPIO.output(37, GPIO.HIGH)
time.sleep(3)

GPIO.cleanup()