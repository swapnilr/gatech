import numpy as np
import math
import cv

def hough_lines_acc(BW, RhoResolution=1.0, Theta=np.linspace(-90,89, 180)):
    height, width = BW.shape
    rhoCount = cv.Round(((width + height) * 2 + 1)/RhoResolution)
    radiansTheta = np.radians(Theta)
    cosTheta = np.cos(radiansTheta)
    sinTheta = np.sin(radiansTheta)
    theta = np.linspace(Theta.min() - 1, Theta.max() + 1, Theta.size + 2)
    H = np.zeros((rhoCount + 2, Theta.size + 2), dtype=np.uint64)
    for y in range(height):
        for x in range(width):
            if BW[y][x]:
                for thetaIdx in range(len(Theta)):
                    r = cv.Round( x * cosTheta[thetaIdx] + y * sinTheta[thetaIdx] );
                    r += (rhoCount - 1)/2
                    H[r+1][thetaIdx + 1] += 1
    limit = (rhoCount-1)/2
    rho = np.linspace(-limit, limit, rhoCount)
    return H, theta, rho
