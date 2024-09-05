### HC-SR04 Ultrasonic Sensor
# power: 5 volt (3.3 volt does not work)
# echo pin --> 120 ohm --> ground pin --> 120 ohm --> ground
# -----------------------------------------------------------
# trigger: 0 --> 2 microSec, 1 --> 10 mSec, 0 --> ?
# echo: after trigger becomes dorps to '0' --> ? --> send sonic pulse 
#   --> wait until sonic pulse returns --> measure time and calculate the distance.
# ---------------------------------------------------------------------------------
#   **  How the Ultrasonic Sensor Works  ** 
#   - trigger: make system ready
#   - echo: at ready state: 0 --> go to system alert: 1 (+) signal transmit 
#                  --> go to ready state when returned signal received : 0 
# -------------------------------------------------------------------------
# - speed of sound: 343 meter/second  ~ 1,125 feet/second ~ 767 miles/hour ~ 1235 km/hour
#   --> distance (cm) = (1 / 34,300 * 1,000,000) /  


import RPi.GPIO as GPIO
import time

# GPIO.setmode(GPIO.BCM)
# trigPin = 23
# echoPin = 24

GPIO.setmode(GPIO.BOARD)
trigPin = 16
echoPin = 18
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

try:
    while True:
        # print('test')
        GPIO.output(trigPin, 0)
        time.sleep(10E-6)
        GPIO.output(trigPin, 1)
        time.sleep(100E-6)
        GPIO.output(trigPin, 0)

        while GPIO.input(echoPin) == 0:
            pass
        echoStart = time.time()

        while GPIO.input(echoPin) == 1:
            pass
        echoStop = time.time()

        pingTraveTime = echoStop - echoStart
        # print(int(pingTraveTime * 1E6))
        # print('Distance: ', int(pingTraveTime * 0.01715 * 1E6), ' cm')
        print('Disance: ', '{0:.2f}'.format(pingTraveTime * 0.01715 * 1E6), ' cm')
        time.sleep(.2)

except KeyboardInterrupt:
    GPIO.cleanup()
    print('GPIO cleaned up.')
