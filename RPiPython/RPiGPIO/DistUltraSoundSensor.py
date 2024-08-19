# Purpose: Measure distance from ultra-sound sensor to an object
### Sensor pin out: 
#   1. Vcc: power input (+)
#   2. Trigger: send out ultra-sound
#   3. Echo: receive returned ultra-sound
#   4. Gnd: ground (-)
### Circuit connection 
#   1. Vcc -- 5 V on Raspberry pi
#   2. Trig -- GPIO 4 on Raspberry pi
#   3. Echo -- GPIO 18 on Raspberry pi 
#      (+) Echo --  1 Kohm register -- 2 Kohm register -- Gnd on sensor  ** why ?
#   4. Gnd -- Gnd on Raspberry pi

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 4
ECHO = 18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

while GPIO.input(ECHO) == False:
    start = time.time()

while GPIO.input(ECHO) == True:
    end = time.time()

sig_time = end - start

# cm
distance = sig_time / 0.000058  # inches: 0.000148

print('Distance: {} cm'.format(distance))

GPIO.cleanup()