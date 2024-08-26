<h4>Update: Aug. 2024</h4>

<h3>Micro Python on Thonny</h3>

<h4>I.  Dwonload and install Thonny from  <a href="https://thonny.org/">Thonny.org </a></h4>
<h4>II. Download and install microcontroller firmware and Flash it on the microcontroller.</h4>

-   Refer to <a href="https://randomnerdtutorials.com/flashing-micropython-firmware-esptool-py-esp32-esp8266/">"Random Nerd Tutorials - 1"</a> and <a href="https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/">"Random Nerd Tutorials-2"</a> for ESP32 and ESP8266

1. Download MicroPython firmware from <a href="https://micropython.org/download/">"micropython.org"</a>

2. Flash MicorPython Firmware with esptool.py on ESP32 and ESP8266
   -> Follow instructions on <a href="https://randomnerdtutorials.com/flashing-micropython-firmware-esptool-py-esp32-esp8266/-1">"Random Nerd Tutorials - 1 "</a>.

    ```sh
    $ pip install esptool
    $ pip install setuptools
    $ python -m esptool
    ```

    ..... and then, follow the instructions for respective microcontroller.

    ```sh
    $ python -m esptool --chip esp8266 erase_flash
    $ python -m esptool --chip esp8266 --port COM7 write_flash --flash_mode dio --flash_size detect 0x0 C:\Users\sangp\Downloads\ESP8266_GENERIC-20240602-v1.23.0.bin

    ```

<h4>III. Setup Thonny for MicroPython.</h4>

1. Flash MicroPython firmware using Thonny IDE: Tools -> Options -> Interpreter .... follwing the instructions on <a href="https://randomnerdtutorials.com/getting-started-thonny-micropython-python-ide-esp32-esp8266/">"Random Nerd Tutorials-2"</a>
