import socket
import keyboard
import time

SERVER_IP_ADDRESS = '10.42.0.1'
UDP_PORT_NUMBER = 8888
BUFFER_SIZE = 1024 # buffer size: 1024

# socket for control command Tx
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFFER_SIZE)

command = ''
while True:
    try:
        if keyboard.is_pressed('left'):
            command = 'p-'
        elif keyboard.is_pressed('right'):
            command = 'p+'
        elif keyboard.is_pressed('down'):
            command = 't+'
        elif keyboard.is_pressed('up'):
            command = 't-'
        elif keyboard.is_pressed('q'):
            command = 'EXIT'
        time.sleep(0.01)

    except:
        break

    if (command == 'p-' or command == 'p+' or command == 't-'
            or command == 't+' or command == 'EXIT'):
        command = command.encode('utf-8')
        udpSocket.sendto(command, (SERVER_IP_ADDRESS, UDP_PORT_NUMBER))

        data, serverAddress = udpSocket.recvfrom(BUFFER_SIZE)
        data = data.decode('utf-8')

        print('Data from server: ', data)
        print('Server Address: ', serverAddress)

udpSocket.close()
exit(1)