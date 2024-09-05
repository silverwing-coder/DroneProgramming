
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
# GPIO_RX_PIN = 26
GPIO_RX_PIN = 21
# GPIO Pin connected to IR transmitter.
GPIO_TX_PIN = 19

# GPIO level to switch transmitter off.
TX_OFF_LEVEL = 0
# GPIO level to switch transmitter on.
TX_ON_LEVEL = 1
# Period to signify end of Tx message.
TX_END_PERIOD = 0.01



#  /*******************************************/
# /* Configure Raspberry Pi GPIO interfaces. */
#/*******************************************/
RPi.GPIO.setwarnings(False)
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(GPIO_RX_PIN, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
RPi.GPIO.setup(GPIO_TX_PIN, RPi.GPIO.OUT, initial=TX_OFF_LEVEL)



# Check for command line argument.
if len(sys.argv) < ARG_COUNT:
   sys.stdout.write("\n" + sys.argv[ARG_EXE] + " '[SEND_DATA]'\n\n")
   sys.stdout.write("e.g.\n")
   sys.stdout.write(sys.argv[ARG_EXE] + " '0.004421 0.004499 0.000515 0.001684 0.000515 0.001687 0.000488 0.001719 0.000514 0.000567 0.000515 0.000600 0.000514 0.000602 0.000514 0.000601 0.000516 0.000603 0.000514 0.001685 0.000481 0.001719 0.000514 0.001685 0.000514 0.000574 0.000516 0.000600 0.000514 0.000599 0.000518 0.000599 0.000514 0.000599 0.000514 0.000598 0.000517 0.001685 0.000514 0.000608 0.000480 0.000633 0.000514 0.000599 0.000514 0.000598 0.000514 0.000604 0.000507 0.000603 0.000517 0.001689 0.000484 0.000604 0.000510 0.001692 0.000510 0.001687 0.000518 0.001689 0.000509 0.001690 0.000510 0.001687 0.000515 0.001685 0.000514'\n\n")
else:
   #Tokenise data to be sent.
   DataList = sys.argv[ARG_DATA].split(" ")
   DataValues = []
   for Count in range(len(DataList)):
      DataValues.append(float(DataList[Count]))

   # Display data packet being sent.
   sys.stdout.write("\nSENDING DATA:\n")
   DataLevel = TX_ON_LEVEL
   for Count in range(len(DataValues)):
      if (Count % 5) == 0:
         sys.stdout.write("\n")
      sys.stdout.write("{:03d} {:d} {:f}\t".format(Count, DataLevel, DataValues[Count]))
      if DataLevel == TX_OFF_LEVEL:
         DataLevel = TX_ON_LEVEL
      else:
         DataLevel = TX_OFF_LEVEL

   # Transmit data.
   DataLevel = TX_ON_LEVEL
   for Count in range(len(DataValues)):
      RPi.GPIO.output(GPIO_TX_PIN, DataLevel)
      if DataLevel == TX_OFF_LEVEL:
         DataLevel = TX_ON_LEVEL
      else:
         DataLevel = TX_OFF_LEVEL
      time.sleep(DataValues[Count])

   sys.stdout.write("\n\n")

   # Switch off IR transmitter.
   RPi.GPIO.output(GPIO_TX_PIN, TX_OFF_LEVEL)

   # End of transmission period.
   time.sleep(TX_END_PERIOD)