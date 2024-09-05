### SPI(Serial Peripherial Interface) setup
# $ pip install spidev
# $ pip install mfrc522
# $ sudo raspi-config --> Interface Options --> Enable SPI
## Edit: mfrc522 library python files as described below.

''' <Reference reading>
SPI uses 4 separate connections to communicate with the target device. 
These connections are the serial clock (CLK), Master Input Slave Output (MISO), 
Master Output Slave Input (MOSI) and Chip Select (CS).
1. The clock pin sense pulses at a regular frequency, 
   the speed at which the Raspberry Pi and SPI device agree to transfer data
   to each other. 
   For the ADC, clock pulses are sampled on their rising edge, 
   on the transition from low to high.
2. The MISO pin is a data pin used for the master (in this case the Raspberry Pi)
   to receive data from the ADC. Data is read from the bus after every clock pulse.
3. The MOSI pin sends data from the Raspberry Pi to the ADC. 
   The ADC will take the value of the bus on the rising edge of the clock. 
   This means the value must be set before the clock is pulsed.
4. Finally, the Chip Select line chooses which particular SPI device is in use. 
   If there are multiple SPI devices, they can all share the same CLK, MOSI, and MISO. 
   However, only the selected device has the Chip Select line set low, 
   while all other devices have their CS lines set high. 
   A high Chip Select line tells the SPI device to ignore 
   all of the commands and traffic on the rest of the bus
'''

import time

# from MFRC522 import MFRC522
from SimpleMFRC522 import SimpleMFRC522

# reader = MFRC522()
reader = SimpleMFRC522()
try:
    while True:
        cmd = input('Do you want to read or write? (R or W) ')
        if cmd == 'W':
            text = input('Input your text: ')
            print('Place Card on Reader')
            reader.write(text)
        if cmd == 'R':
            print('Place Card on Reader')
            id, text = reader.read()
            print('ID: ', id)
            print('Text: ', text)
        time.sleep(0.5)

except KeyboardInterrupt:
    print('Program Interrupted.')
