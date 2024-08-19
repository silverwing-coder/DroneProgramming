'''
Edited by Sangmork Park, Aug-2024
Last update: 11-Aug.2024
---------------------------------------------------------------------------
This Python code is a Raspberry Pi remote control program on TCP protocol.

---------------------------------------------------------------------------
'''

import socket
import keyboard
import time

SERVER_IP_ADDRESS = '10.42.0.1'
CONTROL_PORT_NUMBER = 8888
BUFFER_SIZE = 1024

# Initialize client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP_ADDRESS, CONTROL_PORT_NUMBER))
print(f'Connected to .... {SERVER_IP_ADDRESS}:{CONTROL_PORT_NUMBER}')

command = ''
while True:
    try:
        if keyboard.is_pressed('left'):
            command = 'p-'
        if keyboard.is_pressed('right'):
            command = 'p+'
        if keyboard.is_pressed('down'):
            command = 't+'
        if keyboard.is_pressed('up'):
            command = 't-'
        if keyboard.is_pressed('q'):
            command = 'EXIT'
        time.sleep(0.05)

    except:
        break

    if (command == 'p-' or command == 'p+' or command == 't-'
            or command == 't+' or command == 'EXIT'):
        print(command)
        command = command.encode('ascii')
        client_socket.send(command)

    # message = client_socket.recv(BUFFER_SIZE).decode('ascii')
    # print(message)
    #

    if command == 'EXIT'.encode('ascii'):
        client_socket.close()
        break
