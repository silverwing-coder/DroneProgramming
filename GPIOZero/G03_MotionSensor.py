from gpiozero import LED, MotionSensor, InputDevice
from signal import pause
from time import sleep

pir = MotionSensor(17)
# ipd = InputDevice(pin=4)
led = LED(26)

# while True:
#     print(pir.is_active)
#     sleep(0.5)

# led.on()
# sleep(3)

def print_on():
    print('motion on')

def print_off():
    print('motion off')

pir.when_no_motion = print_off
pir.when_motion = print_on

pause()

# while True:
#     print(ipd.value)
#     sleep(1)