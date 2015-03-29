import cv2
import numpy as np

def readImage(filename):
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE).astype(np.float32)
    return image/255.0
