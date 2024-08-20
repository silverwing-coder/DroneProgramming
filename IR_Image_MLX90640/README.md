<h4> Last update: June-2024

<h2>IR image process with MLS90640 IR Thermal Camera</h2>

<h3>I. MLX90640 IR Thermal Camera Setup</h3>

<h4>1. Install python libraries</h4>

``` sh
$ pip install matplotlib
$ pip install scify
$ pip install numpy
$ sudo apt install python3-smbus
$ sudo apt install i2ctools
```

<h4>2. Enable I2C interface</h4>

``` sh
$ raspi-config   --> enable I2C
```

<h4>3. I2C check</h4>

``` sh
$ sudo i2cdetect -y 1
```

<h4>4. Install MLX90640 libraries</h4>

``` sh
$ pip install adafruit-blinka
$ pip install adafruit-circuitpython-mlx90640
```