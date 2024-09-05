###
# $ pip install adafruit-circuitpython-dht
#  --> board module is within adafruit-blinka : 
#  --> $ pip install --force-reinstall adafruit-blinka # if necessary #
# pin out(3 Pin) from left: 
#   Type-1. Signal --> Vcc --> Ground 
#   Type-22. VCC --> Signal --> Ground

import time
import board
import adafruit_dht

# adafruit_dht.DHT11
myDevice = adafruit_dht.DHT11(board.D17)
# print(board.D4)

while True:
    try:
        temp = myDevice.temperature
        print('Temp: ', temp)
    except RuntimeError as error:
        print(error.args[0])

    time.sleep(5)