'''
Created by Sangmork Park, July-2024 
Last update, 12-Aug-2024
-----------------------------------------------------------------------------------
This Python program build a video streaming server captured by Raspberry-Pi camera.
- Trnasport Protol: TCP
-----------------------------------------------------------------------------------
'''

import socket
import pickle
import struct

from picamera2 import Picamera2

SERVER_IP_ADDRESS = '10.42.0.1'
VIDEO_PORT_NUMBER = 9999

''' Setup RPi Camera '''
IMG_WIDTH = 640
IMG_HEIGHT = 480

camera = Picamera2()
camera.preview_configuration.main.size = (IMG_WIDTH, IMG_HEIGHT)
camera.preview_configuration.main.format = "RGB888"     # 8 bit RGB format
camera.preview_configuration.align()                    # keep format size sililar to standard
camera.configure('preview')
camera.start()

# Create a server socket for streaming
video_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_server_socket.bind((SERVER_IP_ADDRESS, VIDEO_PORT_NUMBER))     

video_server_socket.listen(1)
print('Server is up and listening ....')
print(f'At {SERVER_IP_ADDRESS}:{VIDEO_PORT_NUMBER}')

# Accept a client connection
client_socket, client_address = video_server_socket.accept()
print(f"[*] Accepted connection from {client_address}")

while True:
    
    frame = camera.capture_array()
    # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Serialize the frame to bytes
    serialized_frame = pickle.dumps(frame)

    # Pack the data size and frame data: 'L': unsigned long long (8 bytes)
    message_size = struct.pack("Q", len(serialized_frame))
    client_socket.sendall(message_size + serialized_frame)
    print('Sending packet .....')

    # Display the frame on the server-side (optional)
    # cv2.imshow('Server Video', frame)

    # Press 'q' to quitq
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Release resources
# video_capture.release()
# cv2.destroyAllWindows()