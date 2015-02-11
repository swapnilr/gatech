import numpy as np
import math
import cv

def hough_lines_acc(BW, RhoResolution=1.0, Theta=np.linspace(-90, 89, 180)):
    # % Compute Hough accumulator array for finding lines.
    # %
    # % BW: Binary (black and white) image containing edge pixels
    # % RhoResolution (optional): Difference between successive rho values, in pixels
    # % Theta (optional): Vector of theta values to use, in degrees
    # %
    # % Pay close attention to the coordinate system specified in the assignment.
    # % Note: Rows of H should correspond to values of rho, columns those of theta.
    # 
    # %% TODO: Your code here
    rows, columns = BW.shape
    diagonal = math.sqrt(rows ** 2 + columns ** 2)
    bins = math.ceil(diagonal/RhoResolution)
    rhos = 2*bins + 1
    limit = bins * RhoResolution
    rho = np.linspace(-limit, limit, rhos)
    # TODO: Store in a higher type array and normalize
    H = np.zeros((rho.size, Theta.size), dtype=np.uint64)
    theta = Theta
    radiansTheta = np.radians(Theta)
    cosTheta = np.cos(radiansTheta)
    sinTheta = np.sin(radiansTheta)
    for row in range(rows):
        for col in range(columns):
            if BW[row][col]:
                for thetaIdx in range(len(Theta)):
                    #rhoVal = col * cosTheta[thetaIdx] + row * sinTheta[thetaIdx]
                    #print rhoVal, rho[rhoVal]
                    #rhoIdx = np.nonzero(np.abs(rho-rhoVal) == np.min(np.abs(rho-rhoVal)))
                    #print rhoIdx
                    #rhoIdx = rhoIdx[0]
                    #H[rhoIdx[0]][thetaIdx] += 1
                    rhoV = round(col * cosTheta[thetaIdx] + row * sinTheta[thetaIdx]) + diagonal
                    H[rhoV, thetaIdx] += 1
    return H, theta, rho

def hough_lines_acc2(BW, RhoResolution=1.0, Theta=np.linspace(-90,89, 180)):
    height, width = BW.shape
    rhoCount = cv.Round(((width + height) * 2 + 1)/RhoResolution)
    radiansTheta = np.radians(Theta)
    cosTheta = np.cos(radiansTheta)
    sinTheta = np.sin(radiansTheta)
    theta = np.linspace(-91, 90, 182)
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
