import socket

import RPi.GPIO as GPIO
import dht11
import time

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

myDHT = dht11.DHT11(11)

bufferSz = 1024
serverIP = '192.168.39.125'
serverPort = 2222
RPiServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RPiServer.bind((serverIP, serverPort))
print('Server Up and Listening ....')

while True:
    cmd, clientAddress = RPiServer.recvfrom(bufferSz)
    cmd = cmd.decode('utf-8')
    # print(cmd)
    print('Client Address: ', clientAddress[0])

    if cmd == 'GO':
        result = myDHT.read()

        if result.is_valid() == False:
            data = 'Bad Measurement.'
            print(data)
            data = data.encode('utf-8')
            RPiServer.sendto(data, clientAddress)
            continue

        if result.is_valid():
            data = str(result.temperature) +':' + str(result.humidity)
            data = data.encode('utf-8')
            RPiServer.sendto(data, clientAddress)

    if cmd != 'GO':
        data = 'Invalid Request'
        data = data.encode('utf-8')
        RPiServer.sendto(data, clientAddress)
        break

