'''
Edited by Sangmork Park, July-2024 
Last update: 02-Aug.2024
---------------------------------------------------------------------------
This Python code is a video streaming client program.

---------------------------------------------------------------------------
'''

import cv2
import socket
import pickle
import struct

SERVER_IP_ADDRESS = '10.42.0.1'
SERVER_PORT_NUMBER = 9999
CLIENT_PORT_NUMBER = 4096

# Initialize client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP_ADDRESS, SERVER_PORT_NUMBER))  

# Socket receives serialized binary data
received_data = b""

# struct: a module for packing and unpacking data to and from C representations
# 'Q': unsigned long long (8 bytes)
payload_size = struct.calcsize("Q")

while True:
    while len(received_data) < payload_size:
        # receive data by 4 KB buffer size
        packet = client_socket.recv(4 * 1024)
        if not packet:
            break
        received_data += packet

    # if no data received / transmission terminated    
    if not received_data:
        break

    # get packed_msg_size from the first element in the payload
    packed_msg_size = received_data[:payload_size]
    received_data = received_data[payload_size:]
    
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    while len(received_data) < msg_size:
        received_data += client_socket.recv(4 * 1024)

    frame_data = received_data[:msg_size]
    received_data = received_data[msg_size:]
    frame = pickle.loads(frame_data)
    
    cv2.imshow('Client', frame)

    if cv2.waitKey(1) == ord('q'):
        break

# Release resources 
cv2.destroyAllWindows()
client_socket.close()
