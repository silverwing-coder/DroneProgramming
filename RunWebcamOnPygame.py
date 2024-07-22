
'''
Created by Sangmork Park for keyboard input verification on pygame
Last update: July-2024

'''

import cv2
import pygame
from pygame.locals import *
import numpy as np
import sys
import time

pygame.init()
pygame.display.set_caption('PYGAME')
screen = pygame.display.set_mode([640,480])
pygame.display.flip()
capture = cv2.VideoCapture(0)

start = time.time()
while True:
    _, image = capture.read()
    # screen.fill([0, 0, 0])

    image = cv2.flip(image, 1)
    end = time.time()
    fps = int(1 / (end - start))
    cv2.putText(image, str(fps), (30, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
    # cv2.imshow('OPENCV', image)

    '''
    1. covert color channel: opencv (BGR) --> pygame (RGB)
    2. flip image to convert it to pygame surface --> pygame surface flips theed source image
    '''
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)
    image = np.rot90(image)
    image = pygame.surfarray.make_surface(image)
    screen.blit(image, (0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == pygame.K_DOWN:
                print('Down key pressed.')
            if event.key == pygame.K_UP:
                print('Up key pressed.')
            if event.key == pygame.K_LEFT:
                print('Left key pressed.')
            if event.key == pygame.K_RIGHT:
                print('Right key pressed.')
            if event.key == pygame.K_q:
                # cv2.destroyAllWindows()
                capture.release()
                pygame.quit()
                sys.exit(0)
    start = end
