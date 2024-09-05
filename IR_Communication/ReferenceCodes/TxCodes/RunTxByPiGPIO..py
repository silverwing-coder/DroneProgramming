'''
# This program is a python code sending data on 38 kHz IR Frequencey # 
- Created by Sangmork Park in July-2024
1.  Components needed: Raspberry Pi, IR LED(KY005), Breadboard, Jumper Wires, 
    (Optional) Register, NPN Transitor for better control
2.  Necessary Libraries: 'pigpio' 
    $ pip instal pigpio, python3-pigpio (inclued in Pi O.S. by default)
    ** RPi.GPIO library does not work sinnce it cannot support real-time GPIO control
3.  Setup environment
    $ sudo systemctl enable pigpiod
    $ sudo systemctl start pigpiod
'''

import pigpio
import time

pi = pigpio.pi()

GPIO_PIN = 19

pi.set_PWM_frequency(GPIO_PIN, 38000)

def send_ir_signal(data):
    for bit in data:
        if bit == '1':
            pi.set_PWM_dutycycle(GPIO_PIN, 128)
            # usage: set_PWM_dutycycle(PIN, 255*0.5) --> 50% duty cycle
        else:
            pi.set_PWM_dutycycle(GPIO_PIN, 0)
        time.sleep(0.0001)

data = "101010101010111110"
count = 1
while count < 10:
    send_ir_signal(data)
    count += 1

