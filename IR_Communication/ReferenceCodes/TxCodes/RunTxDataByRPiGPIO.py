'''
# This program is a python code sending data on 38 kHz IR Frequencey by RPi.GPIO ligrary #
    ** RPi.GPIO library does not work sinnce it cannot support real-time GPIO control
'''


import os
import sys
import math
import time
import hashlib
import datetime
import RPi.GPIO



# Number of command line arguments.
ARG_COUNT = 2
# Data to send command line argument.
ARG_EXE = 0
ARG_DATA = 1

# GPIO Pin connected to IR receiver.
GPIO_RX_PIN = 21
# GPIO Pin connected to IR transmitter.
GPIO_TX_PIN = 19

# GPIO level to switch transmitter off.
TX_OFF_LEVEL = 0
# GPIO level to switch transmitter on.
TX_ON_LEVEL = 1
# Period to signify end of Tx message.
TX_END_PERIOD = 0.01
# Single level period, one period is a binary 0, two periods are a binary 1. Tx/Rx Rate of 3KHz. 
TX_LEVEL_PERIOD = 0.0003
# Infra Red Rx device VS1838B operates at 38KHz carrier frequency.
# TX_CARRIER_PERIOD = 0.000026316
TX_CARRIER_PERIOD = 0.000026315789
# Start bits transmitted to signify start of transmission.
TX_START_BITS = 1


# Data encryption key.
ENCRYPTION_KEY = [ 0xC5, 0x07, 0x8C, 0xA9, 0xBD, 0x8B, 0x48, 0xEF, 0x88, 0xE1, 0x94, 0xDB, 0x63, 0x77, 0x95, 0x59 ]
# Data packet identifier.
PACKET_SIGNATURE = [ 0x63, 0xF9, 0x5C, 0x1B ]

# Data packet to transmit.
DataPacket = {
   "SIGNATURE": PACKET_SIGNATURE,
   "DATA_LENGTH": 0,
   "DATA": [],
   "CHECKSUM": 0,
}

def TxIrLevel(Bit, PeriodCount):
   # For bit 0 don't transmit for required period.
   # For bit 1 transmit carrier frequency for required period.

   # Code for external hardware carrier generator.
   Period = int(PeriodCount * (TX_LEVEL_PERIOD / TX_CARRIER_PERIOD))
   if Bit == 1:
      RPi.GPIO.output(GPIO_TX_PIN, TX_ON_LEVEL)
   time.sleep(Period * 2 * TX_CARRIER_PERIOD)
   RPi.GPIO.output(GPIO_TX_PIN, TX_OFF_LEVEL)

   # Code for internal software carrier generator.
   # PYTHON SLEEP IS NOT ACURATE ENOUGH TO GENERATE A UNIFORM PERIOD FOR THE
   # CARRIER SIGNAL.
   # Period = int(PeriodCount * (TX_LEVEL_PERIOD / TX_CARRIER_PERIOD))
   # for Count in range(Period):
   #    if Bit == 1:
   #       RPi.GPIO.output(GPIO_TX_PIN, TX_ON_LEVEL)
   #       time.sleep(TX_CARRIER_PERIOD)
   #       RPi.GPIO.output(GPIO_TX_PIN, TX_OFF_LEVEL)
   #       time.sleep(TX_CARRIER_PERIOD)
   #    else:
   #       time.sleep(2 * TX_CARRIER_PERIOD)



# Transmit a byte of data from the IR device.
def TxIrByte(Byte):
   global CurrentTxLevel

   BitMask = (1 << 7)
   for BitCount in range(8):
      # Get the next bit from the byte to transmit.
      Bit = (Byte & BitMask)
      BitMask = int(BitMask / 2)

      # Toggle GPIO level.
      if CurrentTxLevel == TX_OFF_LEVEL:
         CurrentTxLevel = TX_ON_LEVEL
      else:
         CurrentTxLevel = TX_OFF_LEVEL
      if Bit == 0:
         BitCount = 1
      else:
         BitCount = 2
      TxIrLevel(CurrentTxLevel, BitCount)



# A very basic encrypt/decript function, for keeping demonstration code simple. Use a comprehensive function in production code.
def BasicEncryptDecrypt(Data):
   KeyCount = 0
   KeyLen = len(ENCRYPTION_KEY)
   for Count in range(len(Data)):
      Data[Count] ^= ENCRYPTION_KEY[KeyCount]
      if KeyCount >= KeyLen:
         KeyCount = 0



#  /*******************************************/
# /* Configure Raspberry Pi GPIO interfaces. */
#/*******************************************/
RPi.GPIO.setwarnings(False)
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(GPIO_RX_PIN, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
RPi.GPIO.setup(GPIO_TX_PIN, RPi.GPIO.OUT, initial=TX_OFF_LEVEL)



# Check for command line argument.
if len(sys.argv) < ARG_COUNT:
   sys.stdout.write("\n" + sys.argv[ARG_EXE] + " [SEND_DATA]\n\n")
else:
   # Place data into data packet and set packet values ready to be sent.
   DataPacket["DATA_LENGTH"] = len(sys.argv[ARG_DATA])
   #Tokenise and encrypt data to be sent.
   DataPacket["DATA"] = list(sys.argv[ARG_DATA])
   for Count in range(len(DataPacket["DATA"])):
      DataPacket["DATA"][Count] = ord(DataPacket["DATA"][Count])
   BasicEncryptDecrypt(DataPacket["DATA"])
   # Calculate checksum of data for transmission validation.
   DataPacket["CHECKSUM"] = 0
   for Byte in DataPacket["DATA"]:
      DataPacket["CHECKSUM"] ^= Byte

   # Display data packet being sent.
   sys.stdout.write("\nSENDING PACKET:\n")
   sys.stdout.write(str(DataPacket) + "\n\n")

   count = 0
   while count < 10:

      # Switch on IR transmitter.
      CurrentTxLevel = TX_ON_LEVEL
      # Wait for the number of start bits.
      TxIrLevel(CurrentTxLevel, TX_START_BITS)

      # Transmit data packet signature.
      for Byte in DataPacket["SIGNATURE"]:
         TxIrByte(Byte)

      # Transmit data packet data length.
      TxIrByte(DataPacket["DATA_LENGTH"])

      # Transmit data packet encrypted data.
      for Byte in DataPacket["DATA"]:
         TxIrByte(Byte)

      # Transmit data packet data checksum.
      TxIrByte(DataPacket["CHECKSUM"])

      # Switch off IR transmitter.
      CurrentTxLevel = TX_OFF_LEVEL
      RPi.GPIO.output(GPIO_TX_PIN, CurrentTxLevel)

      # End of transmission period.
      time.sleep(TX_END_PERIOD)

      count = count + 1