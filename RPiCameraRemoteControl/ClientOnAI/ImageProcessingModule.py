import numpy as np
import cv2

ALPHA, BETA = -50, 2
BRIGHT, CONTRAST = 10, 2.5
KERNEL = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
# KERNEL = [[0, 0, -1, 0, 0], [0, -1, -2, -1, 0], [-1, -2, 17, -2, -1],
#           [0, -1, -2, -1, 0], [0, 0, -1, 0, 0]]

def add_bright_contrast_addweight(image: np.array, contrast: float, brightness: int) -> np.array:
    # add brightness to each pixel value
    # scale the pixel values by adjusting contrast
    return cv2.addWeighted(image, contrast, np.zeros(image.shape, image.dtype), 0, brightness)

def add_bright_contrast_cvt_scale(image: np.array, alpha: float, beta: int) -> np.array:
    # out_image(i,j) = beta * in_image(i,j) + alpha
    return cv2.convertScaleAbs(image, alpha, beta)

def sharpen_image(image: np.array, kernel: np.array) -> np.array:
    # adjust kernel size and value
    return cv2.filter2D(image, -1, kernel)

def resize_image(image:np.array, scale: float) -> np.array:
    # image.shape = (height, width, color_channel)
    return cv2.resize(image, (int(image.shape[1]*scale), int(image.shape[0])))

def process_image(image: np.array) -> np.array:
    bc_image = add_bright_contrast_cvt_scale(image, ALPHA, BETA)
    # bc_image = add_bright_contrast_addweight(image, CONTRAST, BRIGHT)
    # bc_image = image
    kernel = np.array(KERNEL)
    return cv2.medianBlur(sharpen_image(bc_image, kernel), 3)

