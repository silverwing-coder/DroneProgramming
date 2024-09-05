<h4>Last Update: July-2024</h4>
<h3>FIT0731 Pan Tilt Hat for Raspberry Pi</h3>

<h4>Hardware Assembly and Program Instructions </h4>

 --> Refer to <a href="https://wiki.dfrobot.com/Pan_Tilt_Hat_For_Raspberry_Pi_SKU_FIT0731"> wiki.dfrobot.com</a>

 1. PCA9685: 12 bit PWM Servo Driver controller --> I2C interface
 2. TSL2591: Light-to-Digital converter

<h4>1. Environment Setup </h4>

 ```
 $ sudo raspi-config
    -- > Interface Options --> I2c --> Enable

$ sudo reboot
```

<h4>2. Install Libraries </h4>
<h4> 2-1. Install BCM2835B (C-programming only. Not required for Python): Broadcom Chip in RPi (refer to：http://www.airspayce.com/mikem/bcm2835/) </h4>

 ```
$ wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.68.tar.gz
$ tar zxvf bcm2835-1.68.tar.gz 
$ cd bcm2835-1.68/
$ sudo ./configure && sudo make && sudo make check && sudo make install
 ```

<h4> 2-2. Install wiringPi (Not Necessary for New O.S. Kernel) </h4>

```
# $ sudo apt-get install wiringpi --> not work
# For Raspberry Pi system after may 2019, an upgrade is required.
$ wget https://project-downloads.drogon.net/wiringpi-latest.deb
$ sudo dpkg -i wiringpi-latest.deb
$ gpio -v
$ # run gpio -v version 2.52 will appear, if not, installtion error happens
```

<h4>3. Download Program: Use Python Examples/Libraries </h4>

 ```
$ sudo apt-get install p7zip-full
$ wget http://www.waveshare.net/w/upload/9/96/Pan-Tilt_HAT_code.7z
$ 7z x Pan-Tilt_HAT_code.7z -r -o./Pan-Tilt_HAT_code
$ sudo chmod 777 -R  Pan-Tilt_HAT_code
$ cd Pan-Tilt_HAT_code/RaspberryPi/python
 ```
