
import cv2
import socket
import numpy as np
import base64
import threading
import keyboard
import time

# SERVER_IP_ADDRESS = '127.0.0.1'
SERVER_IP_ADDRESS = '10.42.0.1'
STREAM_PORT = 9999
CONTROL_PORT = 8888

STREAM_BUFFER_SIZE = 65536
CONTROL_BUFFER_SIZE = 1024

''' streaming server connection'''
stream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
stream_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, STREAM_BUFFER_SIZE)
message = b'Hello'
stream_socket.sendto(message,(SERVER_IP_ADDRESS, STREAM_PORT))

''' control server connection '''
control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
control_socket.connect((SERVER_IP_ADDRESS, CONTROL_PORT))
print(f'Connected to .... {SERVER_IP_ADDRESS}:{CONTROL_PORT}')


def handle_key_control():
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
            # print('CMD:', command)
            command = command.encode('ascii')
            control_socket.send(command)

        # message = client_socket.recv(BUFFER_SIZE).decode('ascii')
        # print(message)

        if command == 'EXIT'.encode('ascii'):
            break

def main() -> None:

    control_thread = threading.Thread(target=handle_key_control)
    control_thread.start()

    while True:
        video_packet, _ = stream_socket.recvfrom(STREAM_BUFFER_SIZE)
        received_data = base64.b64decode(video_packet,' /')
        # npdata = np.fromstring(received_data, dtype=np.uint8)
        npdata = np.frombuffer(received_data, dtype=np.uint8)
        # print(len(npdata))
        frame = cv2.imdecode(npdata,1)
        # frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.imshow("CLIENT", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stream_socket.close()
            control_socket.close()
            break

if __name__ == '__main__':
    main()