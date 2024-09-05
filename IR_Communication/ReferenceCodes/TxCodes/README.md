<h4>Edited July-2024</h4>

<h3>Data Transmission on IR Communication Channel </h3>
'Python' and 'C' codes are implemented for transmitting data through IR communication network which provides alternative communication channel for drones in adversary / constrained operational environment of RF communication network.

<h4>Program Ececution Environment Setup<h4>

    --> Refer to: https://github.com/bschwind/ir-slinger/blob/master/README.md

<ol>
<li>Install libpigpio C-library: Python script does not support kernel-level, fine-tuned GPIO control. libpigpio library supports kernel-level execution of application for stable GPIO PIN control. </li>

``` sh
// Install libpigpio
$ git clone https://github.com/joan2937/pigpio.git
$ cd pigpio
$ make
$ sudo make install
```
<li>Stop pigpio daemon </li>

``` sh
$ sudo systemctl kill pigpiod

```
<li>Run program on root previlege</li>

``` sh
$ sudo application-name
```
<li>When compile C-codes, link all necessary object files.</li>

``` sh
$ gcc test.c -lm -lpigpio -pthread -lrt
```
</ol>