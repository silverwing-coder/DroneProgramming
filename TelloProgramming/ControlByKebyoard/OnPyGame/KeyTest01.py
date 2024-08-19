'''
This python code test the pygame keyboard inputs only.
    - Updated in July-2023
'''

import time
import pygame

def init():
    pygame.init()
    window = pygame.display.set_mode((300, 200))

def getKey(keyName):
    ans = False

    for event in pygame.event.get():
        pass

    keyPressed = pygame.key.get_pressed()
    # print(keyInput)
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    # print(myKey)

    if keyPressed[myKey]:
        ans = True
    pygame.display.update()

    return ans

def main():

    # print(getKey('a'))
    if getKey("LEFT"):
        print("Left key pressed.")
    elif getKey("RIGHT"):
        print("Rignt key pressed.")
    elif getKey("UP"):
        print("Up key pressed.")
    elif getKey("DOWN"):
        print("Down key pressed.")

    time.sleep(0.1)


if __name__ == '__main__':
    init()
    while True:
        main()