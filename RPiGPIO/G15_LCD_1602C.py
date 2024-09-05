## LCD 1602C type: 4 pin connection
## Setup
#   1. sudo raspi-config --> enable I2C
#   2. lsmod | grep i2c --> reboot if necessary 
#   3. sudo apt-get install i2c-tools
#   4. i2cdetect -y 1 --> if raspberry version is higher than 2
#   5. sudo apt-get install libi2c-dev
#   6. sudo pip3 install smbus2
#   7. download lcd-configuration library from "www.toptechboy.com"