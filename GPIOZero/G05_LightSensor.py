from gpiozero import LightSensor, LED
from signal import pause
from time import sleep

sensor = LightSensor(18)
# sensor.wait_for_light()
# print("Light detected.")
# pause()
while True:

    print(sensor.is_active)
    sensor.wait_for_inactive()
    print("It's inactive")
    sensor.wait_for_active()
    print("It's active")
    # sensor.wait_for_light()
        # print("It's dark! ):")
    # sensor.wait_for_dark()
    # print("It's dark ! (:")
    sleep(3)

# led = LED(27)

# sensor.when_light = led.on()
# sensor.when_dar = led.off()
# # led.on()
# pause()

# led.on()
# sleep(3)
