import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

TRIG = 4
ECHO = 18
GREEN = 17
RED = 27

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(RED, GPIO.OUT)

def green_light():
    GPIO.output(GREEN, GPIO.HIGH)
    GPIO.output(RED, GPIO.LOW)

def red_light():
    GPIO.output(RED, GPIO.HIGH)
    GPIO.output(GREEN, GPIO.LOW)

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.000001)
    GPIO.output(TRIG, False)

    begin_loop = time.time()
    start = begin_loop
    end = begin_loop
    while GPIO.input(ECHO) == False:
        start = time.time()
        if(start - begin_loop > 1):
            break

    while GPIO.input(ECHO) == True:
        end = time.time()

    if(start == end):
        distance = 0
    else:
        sig_time = end - start

        # cm
        distance = sig_time / 0.000058  # inches: 0.000148
        # print("Return distance")
    return distance


if __name__ == '__main__':
    
    while True:
        distance = get_distance()
        print('Distance: {} cm'.format(distance))
        time.sleep(0.05)

        if (distance > 20):
            green_light()
        else:
            red_light()


# GPIO.cleanup()