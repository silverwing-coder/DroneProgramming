### schematic
'''
1. vcc --> 5v
2. trig --> GPIO
3. GND --> register --> Echo --> GPIO
'''
from gpiozero import DistanceSensor, LED
from time import sleep
from signal import pause

sensor = DistanceSensor(23, 24, max_distance=10, threshold_distance=0.1) 
# default max_distance = 1
# 23: Echo, 24: Trig

led = LED(17)
while True:
    print('Distance: ', sensor.distance, 'm')
    if sensor.distance < 0.1:
        led.on()
    else:
        led.off()
    sleep(1)

# sensor.when_in_range = led.on
# sensor.when_out_of_range = led.off
# pause()