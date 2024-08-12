'''
Edited by Sangmork Park, August-2024 
---------------------------------------------------------------------------
This Python program controls the pan and tilt of Raspberry Pi Camera
which provides video streaming service.
---------------------------------------------------------------------------
'''

import cv2
import socket
import imutils
import base64
import threading

from picamera2 import Picamera2 # type: ignore
from PCA9685 import PCA9685 # type: ignore

# SERVER_IP_ADDRESS = '127.0.0.1'
SERVER_IP_ADDRESS = '10.42.0.1'
STREAM_PORT = 9999
CONTROL_PORT = 8888
BUFFER_SIZE = 1024

''' Set Raspberry Pi Pan-Tilt '''
tiltAngle = 5
panAngle = 80
controller = PCA9685()
controller.setPWMFreq(50)
controller.setRotationAngle(0, tiltAngle)
controller.setRotationAngle(1, panAngle)

def move_pan_tilt(command) -> None:
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


def handle_control_client() -> None:

    ''' control server socket '''
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_socket.bind((SERVER_IP_ADDRESS, CONTROL_PORT))
    control_socket.listen()
    print('Control server listening .....')

    control_client, control_client_address = control_socket.accept()
    # print(f'Control client from {control_client_address}')
    control_client.send(f'Connected to Server ....'.encode('ascii'))

    while True:
        try:
            command = control_client.recv(1024).decode('ascii')
            # print(command)

            move_pan_tilt(command)
            status = 'Pan: ' + str(panAngle) + ', Tilt: ' + str(tiltAngle)
            control_client.send(status.encode(('ascii')))
        except:
            control_client.close()
            break

def handle_stream_client() -> None:
    
    ''' Set Raspberry-Pi Camera '''
    IMG_WIDTH = 640
    IMG_HEIGHT = 480

    camera = Picamera2()
    camera.preview_configuration.main.size = (IMG_WIDTH, IMG_HEIGHT)
    camera.preview_configuration.main.format = "RGB888"     # 8 bit RGB format
    camera.preview_configuration.align()                    # keep format size sililar to standard
    camera.configure('preview')
    camera.start()

    ''' streaming server socket '''
    stream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    stream_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFFER_SIZE)
    stream_socket.bind((SERVER_IP_ADDRESS, STREAM_PORT))
    print('Streaming server listening .....')
    # stream_client_msg, stream_client_address = stream_socket.recvfrom(BUFFER_SIZE)

    stream_client_msg, client_address = stream_socket.recvfrom(BUFFER_SIZE)
    WIDTH = 400
    while True:
        frame = camera.capture_array()
        frame = imutils.resize(frame, width=WIDTH)

        if_encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        package = base64.b64encode(buffer)
        stream_socket.sendto(package, client_address)
        # print('Send streaming .....')
    

def main() -> None:

    try:     
        stream_thread = threading.Thread(target=handle_stream_client)
        stream_thread.start()
        
        control_thread = threading.Thread(target=handle_control_client)
        control_thread.start()

    except:
        pass


if __name__ == '__main__':
    main()