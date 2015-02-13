from assignment5 import computeGradient
from assignment5 import imageGradientX
from assignment5 import imageGradientY
from assignment2 import convertToBlackAndWhite

import cv2
import numpy as np
import time
raw = cv2.imread('test_image2.jpg',0)
img = cv2.GaussianBlur(raw, (3,3), 1)

def prewitt():
    Hx = np.zeros((3,3), dtype=np.int8)
    for y in range(3):
        Hx[y, 0] = -1
        Hx[y, 2] = 1
    return Hx, Hx.transpose()

def sobel():
    Hx = np.zeros((3,3), dtype=np.int8)
    Hx[0,0] = -1
    Hx[1,0] = -2
    Hx[2,0] = -1
    Hx[2,0] = 1
    Hx[2,1] = 2
    Hx[2,2] = 1
    return Hx, Hx.transpose()

Hx, Hy = prewitt()
cv2.imshow("Prewitt x",convertToBlackAndWhite(computeGradient(img, Hx), threshold=230))
cv2.imshow("Prewitt y",convertToBlackAndWhite(computeGradient(img, Hy), threshold=230))

cv2.imshow("Diff x",convertToBlackAndWhite(imageGradientX(img), threshold=230))
cv2.imshow("Diff y",convertToBlackAndWhite(imageGradientY(img), threshold=230))


Hx, Hy = sobel()
cv2.imshow("Sobel x",convertToBlackAndWhite(computeGradient(img, Hx), threshold=230))
cv2.imshow("Sobel y",convertToBlackAndWhite(computeGradient(img, Hy), threshold=230))
time.sleep(30)

