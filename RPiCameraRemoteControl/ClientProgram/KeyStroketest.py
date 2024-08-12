import keyboard
import time

while True:
    try:
        if keyboard.is_pressed('left'):
            print('You Pressed left!')
        elif keyboard.is_pressed('right'):
            print('You Pressed right!')
        elif keyboard.is_pressed('down'):
            print('You Pressed down!')
        elif keyboard.is_pressed('up'):
            print('You Pressed up!')
        elif keyboard.is_pressed('q'):
            break
        time.sleep(0.1)
    except:
        break