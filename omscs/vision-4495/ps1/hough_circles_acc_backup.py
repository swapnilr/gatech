import numpy as np
import cv2
import math

def hough_circles_acc(BW, radius):
    # % Compute Hough accumulator array for finding circles.
    # %
    # % BW: Binary (black and white) image containing edge pixels
    # % radius: Radius of circles to look for, in pixels
                     
    # % TODO: Your code here
    H = np.zeros(BW.shape, dtype=np.uint64)
    rows, columns = BW.shape
    Theta = np.linspace(0, 359, 360)
    radiansTheta = np.radians(Theta)
    cosTheta = np.cos(radiansTheta)
    sinTheta = np.sin(radiansTheta)
    for row in range(rows):
        for col in range(columns):
            if BW[row][col]:
                for thetaIdx in range(len(Theta)):
                    a = col - radius * cosTheta[thetaIdx]
                    b = row + radius * sinTheta[thetaIdx]
                    if a >= 0 and a < columns:
                        if b >=0 and b < rows:
                            H[b, a] += 1
    return H

def hough_circles_acc2(BW,edges, radius):
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
                theta = math.atan2(dy, dx)
                #print dx, dy, theta
                a = col + radius * np.cos(theta)
                b = row + radius * np.sin(theta)
                if a >= 0 and a < columns:
                    if b >=0 and b < rows:
                        H[b][a] += 1
                dy = -dy
                dx = -dx
                theta = math.atan2(dy, dx)
                a = col +  radius * np.cos(theta)
                b = row + radius * np.sin(theta)
                if a >= 0 and a < columns:
                    if b >=0 and b < rows:
                        H[b][a] += 1
    return H
