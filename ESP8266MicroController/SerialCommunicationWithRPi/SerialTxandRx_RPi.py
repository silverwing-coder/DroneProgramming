'''
Edited by Sangmork Park, Aug-2024
    -   This python-code is created to demonstrate serial communication between a micro controller and Raspberry Pi.
    -   RPi sends a message -> Micro controller echo the message -> RPi receive the message back and print.
'''

import sys
import serial # type: ignore
import time

def receive_data_simple():
    '''serial communication via USB port'''
    # usb_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    '''serial communication via UART pins'''
    usb_port = serial.Serial('/dev/ttyAMA0', 115200, timeout=5)

    try:
        while True:
            line = str(usb_port.readline())
            
            if len(line) == 0:
                print("Time out! Exit.\n")
                sys.exit()
            
            if "esp_start" in line:
                msg_start = line.index('esp_start')
                msg_end = line.index('esp_end')
                msg = line[msg_start+9:msg_end]
                print(msg)

    except KeyboardInterrupt:
        print("Rx: serial comm closed.")
        usb_port.close()

def send_data():
    '''serial communication via USB port'''
    # usb_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    '''serial communication via UART pins'''
    usb_port = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    # time.sleep(1)

    usb_port.reset_input_buffer()
    print('Tx: ESP8266 connected')

    try:
        while True:
            time.sleep(0.1)
            print('Tx in progress....')
            data = 'Send data from RPi. \n'
            usb_port.write(data.encode('utf-8'))

            line = str(usb_port.readline())
            if "esp_start" in line:
                msg_start = line.index('esp_start')
                msg_end = line.index('esp_end')
                msg = line[msg_start+9:msg_end]
                print(msg)

    except KeyboardInterrupt:
        print("Tx: serial comm closed.")
        usb_port.close()


if __name__ == '__main__':
    # receive_data_simple()
    send_data()

