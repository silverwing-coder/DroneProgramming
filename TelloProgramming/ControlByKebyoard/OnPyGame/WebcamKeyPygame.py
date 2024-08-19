''' 
Update: July-2024
    - Test the input keys on pygame
    - Display and key inputs are on pygame
'''

import pygame                   # pip install pygame
import cv2                      # pip install opencv-python
import time

video = cv2.VideoCapture(0)

class PyGame:
    def __init__(self):
        self.frame = video.read()
        self.window = pygame.display.set_mode(self.frame.shape[1::-1])

# Check keyboard input. It returns True if the pressed key matches with a control key (key_name)
'''
 'LEFT' - move left,    'RIGHT' - move right,   'UP'    - move back,    'DOWN'  - move forward
 'W'    - move up,      'S'     - move down,    'A'     - yaw left,     'D'     - yaw right
'''
def check_key_pressed(key_name):
    for event in pygame.event.get():
        pass
    pressed_key = pygame.key.get_pressed()
    key_id = getattr(pygame, 'K_{}'.format(key_name))
    pygame.display.update()
    return pressed_key[key_id]

def main():
    pygame.init()

    _, frame = video.read()
    # window = pygame.display.set_mode(frame.shape[1::-1])
    window = pygame.display.set_mode(frame.shape[1::-1])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        success, frame = video.read()
        if success:
            frame_surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")
            window.blit(frame_surf, (0, 0))
            pygame.display.flip()
            pygame.display.set_caption('PY-GAME')

        if check_key_pressed("LEFT"):
            print("Left key pressed.")
        elif check_key_pressed("RIGHT"):
            print("Rignt key pressed.")
        elif check_key_pressed("UP"):
            print("Up key pressed.")
        elif check_key_pressed("DOWN"):
            print("Down key pressed.")

        time.sleep(0.05)

        if check_key_pressed('q'):
            break

    pygame.quit()

if __name__ == '__main__':
    main()

