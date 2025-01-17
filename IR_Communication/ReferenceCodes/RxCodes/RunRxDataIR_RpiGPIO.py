


import os
import sys
import math
import time
import datetime
import RPi.GPIO



# GPIO Pin connected to IR receiver.
GPIO_RX_PIN = 21
# GPIO Pin connected to IR transmitter.
GPIO_TX_PIN = 19

# GPIO level to switch transmitter off.
TX_OFF_LEVEL = 0
# Period to signify end of Rx message.
RX_END_PERIOD = 0.01
# Smallest period of high or low signal to consider noise rather than data, and flag as bad data. 
RX_REJECT_PERIOD = 0.000001
# Single level period, one period is a binary 0, two periods are a binary 1. 
RX_LEVEL_PERIOD = 0.0003
# Start bits transmitted to signify start of transmission.
RX_START_BITS = 1
# Minimum received valid packet size.
MIN_RX_BYTES = 4

# Data encryption key.
ENCRYPTION_KEY = [ 0xC5, 0x07, 0x8C, 0xA9, 0xBD, 0x8B, 0x48, 0xEF, 0x88, 0xE1, 0x94, 0xDB, 0x63, 0x77, 0x95, 0x59 ]
# Data packet identifier.
PACKET_SIGNATURE = [ 0x63, 0xF9, 0x5C, 0x1B ]



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


# Initialise data.
StartBitFlag = True
ThisPeriod = RX_END_PERIOD
StartBitPeriod = RX_END_PERIOD
LastBitPeriod = RX_END_PERIOD
LastGpioLevel = 1
BitCount = 0
ByteDataCount = 0
ByteData = []
# Data packet to transmit.
DataPacket = {
   "SIGNATURE": [],
   "DATA_LENGTH": 0,
   "DATA": [],
   "CHECKSUM": 0,
}

# Infinate loop for this application.
sys.stdout.write("\nWAITING FOR DATA...\n\n")
sys.stdout.flush()
ExitFlag = False
while ExitFlag == False:
   # Check if data is currently being received.
   ThisPeriod = time.time()
   DiffPeriod = ThisPeriod - LastBitPeriod

   # If data level changes, decode long period = 1, short period = 0.
   GpioLevel = RPi.GPIO.input(GPIO_RX_PIN)
   if GpioLevel != LastGpioLevel:
      # print('GpioLevel:', GpioLevel)
      # Ignore noise.
      if DiffPeriod > RX_REJECT_PERIOD:
         # Wait for start of communication.
         if StartBitFlag == True:
            # Calculate start bit period, consider as period for all following bits.
            if StartBitPeriod == RX_END_PERIOD:
               StartBitPeriod = ThisPeriod
            else:
               StartBitPeriod = (ThisPeriod - StartBitPeriod)
               StartBitFlag = False
         else:
            if DiffPeriod < StartBitPeriod:
               StartBitPeriod = DiffPeriod

            # Receiving a data level, convert into a data bit.
            Bits = int(round(DiffPeriod / StartBitPeriod))
            if BitCount % 8 == 0:
               ByteData.append(0)
               ByteDataCount += 1
            BitCount += 1
            ByteData[ByteDataCount - 1] = (ByteData[ByteDataCount - 1] << 1)
            if Bits > 1:
                ByteData[ByteDataCount - 1] |= 1
         LastBitPeriod = ThisPeriod
      LastGpioLevel = GpioLevel
   elif DiffPeriod > RX_END_PERIOD:
      # End of data reception.
      if ByteDataCount >= MIN_RX_BYTES and StartBitPeriod > RX_REJECT_PERIOD:
         DataCount = 0
         # Validate packet signature.
         MatchFlag = True
         for Count in range(len(PACKET_SIGNATURE)):
            DataPacket["SIGNATURE"].append(ByteData[DataCount])
            if DataPacket["SIGNATURE"][DataCount] != PACKET_SIGNATURE[Count]:
               MatchFlag = False
               break
            DataCount += 1
         if MatchFlag == False:
            print(str(ByteData))
            sys.stdout.write("INVALID PACKET SIGNATURE\n")
         else:
            DataPacket["DATA_LENGTH"] = ByteData[DataCount]
            DataCount += 1
            for Count in range(DataPacket["DATA_LENGTH"]):
               if DataCount < len(ByteData):
                  DataPacket["DATA"].append(ByteData[DataCount])
               else:
                  DataPacket["DATA"].append(0)
               DataCount += 1
            if DataCount < len(ByteData):
               DataPacket["CHECKSUM"] = ByteData[DataCount]
            else:
               DataPacket["CHECKSUM"] = 0xAA
            DataCount += 1
            sys.stdout.write("RECEIVED PACKET: " + str(DataPacket) + "\n")
            # Validate packet checksum.
            Checksum = 0
            for Byte in DataPacket["DATA"]:
               Checksum ^= Byte
            if Checksum != DataPacket["CHECKSUM"]:
               sys.stdout.write("INVALID PACKET CHECKSUM\n")
            else:
               # Decrypt and display data.
               BasicEncryptDecrypt(DataPacket["DATA"])
               Data = ""
               for Count in range(DataPacket["DATA_LENGTH"]):
                  Data += chr(DataPacket["DATA"][Count])
               sys.stdout.write("DECRYPTED DATA: {:s}\n".format(Data))
         sys.stdout.write("\n")
         sys.stdout.flush()

      if (len(DataPacket["SIGNATURE"]) > 0):
         print("DataPacket: ")
         print(DataPacket)

      # Reset data to start a new monitor period.
      StartBitFlag = True
      StartBitPeriod = RX_END_PERIOD
      BitCount = 0
      ByteDataCount = 0
      ByteData = []
      # Data packet to transmit.
      DataPacket = {
         "SIGNATURE": [],
         "DATA_LENGTH": 0,
         "DATA": [],
         "CHECKSUM": 0,
      }