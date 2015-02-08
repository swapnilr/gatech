import numpy as np
import math

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
    rho = np.linspace(0, diagonal, diagonal/RhoResolution)
    H = np.zeros((rho.size, Theta.size), dtype=np.uint8)
    theta = Theta
    radiansTheta = np.radians(Theta)
    cosTheta = np.cos(radiansTheta)
    sinTheta = np.sin(radiansTheta)
    for row in range(rows):
        for col in range(columns):
            if BW[row][col]:
                for thetaIdx in range(len(Theta)):
                    rhoVal = col * cosTheta[thetaIdx] + row * sinTheta[thetaIdx]
                    H[rhoVal][thetaIdx] += 1
    return H, theta, rho
