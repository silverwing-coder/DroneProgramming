
'''
Edited by Sangmork Park, July-2024
This python code ....
1.  Receives 38 kHz IR signal from  IR LED Sensor connected to RPi GPIO.
2.  Decode the bit stream into data-packet.
3.  The data-packet contains 4 bytes packet signature, 1 byte data length,
    4 bytes data, and checksum bit. The data is decoded for data exchange
    and drone control commnds.

@ input: IR signal
@ output: command signal
'''

import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep

from EncodeDecode import EncodeDecodePacket as edp

INPUT_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN, GPIO.IN)

# One pulse distance = 562 micro-seconds on NEC protocol IR communication.
'''
NEC IR Tx protocol uses 562.5 micro-seconds pulse distance encoding of 
the message bits on carruer frequency of 38 kHz(26.3 micro seconds)
'''
PULSE_DIST= 563

# convert eight bit binary number into hexa-decimal format

class IR_Receiver(): 

    def binary2hex(self, bin_num):
        int_num = int(bin_num, 2)
        # hex_num = hex(int_num)
        return int_num


    def receiveDataPacket(self):
        print('READY TO Rx...')
        while True:
            
            # Received data packet
            rxed_packet = []

            # initialise GPIO --> Start frrom space('zero') 
            signal = 1
            while signal:
                signal = GPIO.input(INPUT_PIN)
            
            # bit stream of received data
            signal_data = []

            # packet preamble and data transfer termination variable -> don't accecpt too much data 
            num_of_pulses = 0

            # initaial start time for pulse / space distance measurement
            start_time = datetime.now()

            prev_signal = 0
            signal_count_variable = 0
            while True:
                if signal != prev_signal:
                    now = datetime.now()
                    signal_length = now - start_time
                    start_time = now

                    # cancel noise signals and and packet preambles
                    # --> accpet valuable signals only 
                    # (if the distance is too short or too long, discard the signal)  
                    if((signal_length.microseconds > PULSE_DIST/2) 
                        and (signal_length.microseconds < PULSE_DIST*4)): 
                        # print(prev_signal, "-", signal_length.microseconds)
                        signal_data.append((prev_signal, signal_length.microseconds))
                        signal_count_variable += 1

                # verify data transfer termination condition and noise, 
                if signal:
                    num_of_pulses += 1
                else:
                    num_of_pulses = 0
                if num_of_pulses > PULSE_DIST * 10:
                    break

                # discard oversized packet
                if signal_count_variable > 16 * 8 * 2:
                    signal_count_variable = 0
                    break

                prev_signal = signal
                signal = GPIO.input(INPUT_PIN)
            # print('sig_count:', signal_count_variable)

            data_bits = ''
            bit_count = 0
            byte_count = 0
            if signal_count_variable != 0:
                # print('SIGNAL RECEIVED!')
                # bit_count = 0
                for (signal, distance) in signal_data:
                    # print(signal, ":", distance)
                    if(signal == 1):
                        if(distance > PULSE_DIST * 2):
                            # data_bits.append(1)
                            data_bits = data_bits + '1'
                            # print('1', end='')
                        else:
                            # data_bits.append(0)
                            data_bits = data_bits + '0'
                            # print('0', end='')
                        bit_count += 1

                    # if (bit_count > 0 and bit_count % 8 == 0):
                    if (bit_count > 0 and bit_count % 8 == 0):
                        # print(data_bits)
                        rxed_packet.append(self.binary2hex(data_bits))
                        print(self.binary2hex(data_bits))
                        bit_count = 0
                        data_bits = ''
                        byte_count += 1
                        # byte = 
                        # print("  ", end="") 

                # print('PACKET_SIZE: ', str(byte_count), ' bytes.')
                print('RECEIVED PACKET: ', len(rxed_packet), ' bytes.')
                print(rxed_packet)

                decoder = edp()

                received_data = decoder.getDncodedData(rxed_packet)
                # received_data = decoder.crypted_data

                if(len(received_data) == 8):
                    print("RECEIVED: ", received_data)
                else:
                    print('DATA RECEIVE ERROR')

            
if __name__ == '__main__':
    receiver = IR_Receiver()
    receiver.receiveDataPacket()