
# import time

from PCA9685 import PCA9685 # type: ignore
import socket

SERVER_IP_ADDRESS = '10.42.0.1'
UDP_PORT_NUMBER = 8888

UDP_BUFFER = 1024 # buffer size: 1024

# socket for control command exchange
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.bind((SERVER_IP_ADDRESS, UDP_PORT_NUMBER))
print('Server is Up and Waiting ....')

# pan-tilt initialization
tiltAngle = 5
panAngle = 80
controller = PCA9685()
controller.setPWMFreq(50)
controller.setRotationAngle(0, tiltAngle)
controller.setRotationAngle(1, panAngle)

while True:    
    
    # command message from UDP client
    command, udpClientAddress = udpSocket.recvfrom(UDP_BUFFER)
    command = command.decode('utf-8')
    
    # print(command)
    # print('Client Address: ', clientAddress[0], '-', clientAddress[1])
    print('Command client from: ', udpClientAddress)

    if command == 'p-':                 # LEFT
        if (panAngle >= 10):
            panAngle = panAngle - 0.25
    if command == 'p+':                 # RIGHT
        if (panAngle <= 170):
            panAngle = panAngle + 0.25
    if command == 't-':                 # UP
        if (tiltAngle >= 5):
            tiltAngle = tiltAngle - 0.25
    if command == 't+':                 # DOWN
        if (tiltAngle <= 70):
            tiltAngle = tiltAngle + 0.25

    if command == 'EXIT':
        break
        
    controller.setRotationAngle(0, tiltAngle)
    controller.setRotationAngle(1, panAngle)

    returnMessage = ('Pan: ' + str(panAngle) + ', Tilt: ' + str(tiltAngle)).encode('utf-8')
    udpSocket.sendto(returnMessage, udpClientAddress)

udpSocket.close()
exit(1)


