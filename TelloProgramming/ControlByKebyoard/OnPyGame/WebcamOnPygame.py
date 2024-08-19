''' 
Update: July-2024
    - Test the input keys on pygame
    - Display window and key inputs are on pygame
    - Webcam image caputre is supported by OpenCV
'''

import pygame       # type: ignore
import cv2

capture = cv2.VideoCapture(0)
_, camera_frame = capture.read()

window = pygame.display.set_mode(camera_frame.shape[1::-1])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    success, camera_image = capture.read()
    if success:
        camera_surf = pygame.image.frombuffer(
            camera_image.tobytes(), camera_image.shape[1::-1], "BGR")
    else:
        break
    window.blit(camera_surf, (0, 0))
    pygame.display.flip()
    pygame.display.set_caption('PY-GAME WINDOW')

pygame.quit()
exit()