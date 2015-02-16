from assignment5 import computeGradient
from assignment5 import imageGradientX
from assignment5 import imageGradientY
from assignment2 import convertToBlackAndWhite

import cv2
import numpy as np
import time
import math

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

def getGradient(Hx, Hy):
    rows, columns = Hx.shape
    G = np.zeros((rows, columns))
    for y in range(rows):
        for x in range(columns):
            G[y,x] = math.sqrt(Hx[y,x]**2 + Hy[y,x]**2)
    G = (G * (255.0/G.max())).astype(np.uint8)
    return G

#cv2.imshow("Prewitt x",convertToBlackAndWhite(computeGradient(img, Hx), threshold=230))
#cv2.imshow("Prewitt y",convertToBlackAndWhite(computeGradient(img, Hy), threshold=230))
Dx = imageGradientX(img)
Dy = imageGradientY(img)
Sobx, Soby = sobel()
Prex, Prey = prewitt()

for threshold in [72, 80, 88, 96, 104, 112, 120]:
    cv2.imwrite("diff-%d.png" % threshold,convertToBlackAndWhite(getGradient(Dx, Dy), threshold=threshold))
while False:
    Sx = computeGradient(img, Sobx)
    Sy = computeGradient(img, Soby)
    cv2.imwrite("sobel-%d.png" % threshold, convertToBlackAndWhite(getGradient(Sx, Sy), threshold=threshold))
    Px = computeGradient(img, Prex)
    Py = computeGradient(img, Prey)
    cv2.imwrite("prewitt-%d.png" % threshold, convertToBlackAndWhite(getGradient(Px, Py), threshold=threshold))

#cv2.imshow("Sobel x",convertToBlackAndWhite(computeGradient(img, Hx), threshold=230))
#cv2.imshow("Sobel y",convertToBlackAndWhite(computeGradient(img, Hy), threshold=230))
#time.sleep(30)

