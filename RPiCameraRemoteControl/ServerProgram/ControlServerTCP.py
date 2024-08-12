
# import time

from PCA9685 import PCA9685
import socket
import threading

SERVER_IP_ADDRESS = '10.42.0.1'
CONTROL_PORT_NUMBER = 8888
BUFFER_SIZE = 1024

# socket for control command exchange
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP_ADDRESS, CONTROL_PORT_NUMBER))
server_socket.listen()
print('Server is up and listening ....')

# pan-tilt initialization
tiltAngle = 5
panAngle = 80
controller = PCA9685()
controller.setPWMFreq(50)
controller.setRotationAngle(0, tiltAngle)
controller.setRotationAngle(1, panAngle)

def move_pan_tilt(command):
    # print('CMD:', command)
    global panAngle, tiltAngle

    if command == 'p-':                 # LEFT
        if (panAngle >= 10):
            panAngle = panAngle - 0.5
    if command == 'p+':                 # RIGHT
        if (panAngle <= 170):
            panAngle = panAngle + 0.5
    if command == 't-':                 # UP
        if (tiltAngle >= 5):
            tiltAngle = tiltAngle - 0.5
    if command == 't+':                 # DOWN
        if (tiltAngle <= 70):
            tiltAngle = tiltAngle + 0.5

    controller.setRotationAngle(0, tiltAngle)
    controller.setRotationAngle(1, panAngle)

def handle_control_client(client):
    while True:
        try:
            command = client.recv(1024).decode('ascii')
            # print(command)

            move_pan_tilt(command)
            status = 'Pan: ' + str(panAngle) + ', Tilt: ' + str(tiltAngle)
            client.send(status.encode(('ascii')))
        except:
            client.close()
            break

def main():
    while True:
        client, address = server_socket.accept()
        print(f'Connected with {str(address)}')

        client.send('Connected to the Server...'.encode('ascii'))
        
        control_thread = threading.Thread(target=handle_control_client, args=(client, ))
        control_thread.start()


if __name__ == '__main__':
    main()