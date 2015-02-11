import numpy as np
import cv2
import math

def hough_circles_acc(BW, radius, cannyThreshold1=75, cannyThreshold2=150):
    edges = cv2.Canny(BW, cannyThreshold1, cannyThreshold2)
    H = np.zeros(BW.shape, dtype=np.uint64)
    rows, columns = BW.shape
    Theta = np.linspace(-180, 180, 361)
    radiansTheta = np.radians(Theta)
    cosTheta = np.cos(radiansTheta)
    sinTheta = np.sin(radiansTheta)
    sobelx = cv2.Sobel(BW, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(BW, cv2.CV_64F, 0, 1, ksize=5)
    for row in range(rows):
        for col in range(columns):
            if edges[row][col]:
                dx = sobelx[row][col]
                dy = sobely[row][col]
                for i in range(2):
                    theta = math.atan2(dy, dx)
                    a = col + radius * np.cos(theta)
                    b = row + radius * np.sin(theta)
                    if a >= 0 and a < columns:
                        if b >=0 and b < rows:
                            H[b][a] += 1
                    dy = -dy
                    dx = -dx
    return H
