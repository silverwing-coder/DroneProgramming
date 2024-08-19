###
# pip3 install dht11 : if necessary(installed by default)
# pin out(3 Pin) from left: 
#   Type-1. Signal --> Vcc --> Ground 
#   Type-22. VCC --> Signal --> Ground

import RPi.GPIO as GPIO
import dht11
import time

GPIO.setmode(GPIO.BOARD)
myDHT = dht11.DHT11(pin=11)

try:
    while True:
        # pass
        result = myDHT.read()
        # print(result.is_valid())
        if result.is_valid():
            print('Temperature is: ', result.temperature)
            print('Humidity is: ', result.humidity)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print('GPIO cleaned up.')




