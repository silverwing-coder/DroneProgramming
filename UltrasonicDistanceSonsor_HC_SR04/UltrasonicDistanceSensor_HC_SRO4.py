'''
Tested on July-18-2024 by SAM

1. HC-SRO4 ultrasonic distance sensor field of view
    - effective viewing angle: 30 ~ 40 degrees 
2. Schematic
    - Vcc: 5.5 v
    - Sensor --> Registance --> GND
'''
from gpiozero import DistanceSensor, LED
import time
import signal

led = LED(13)
sensor = DistanceSensor(19, 26)  #(sensor-gpio, trigger-gpio)
sensor.max_distance = 3
sensor.threshold_distance = 0.2
while True:
    print('Distance to nearest object is ', int(sensor.distance * 100), ' cm')
    if sensor.distance < sensor.threshold_distance:
        led.on()
    else:
        led.off()
    time.sleep(0.5)


# sensor.when_in_range = led.on
# print('Range: ', int(sensor.distance) * 100, ' cm')
# sensor.when_out_of_range = led.off

# signal.pause()
