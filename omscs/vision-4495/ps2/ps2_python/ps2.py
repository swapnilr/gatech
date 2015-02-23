# ps2
import os
import numpy as np
import cv2
import time
## 1-a
# Read images
L = cv2.imread(os.path.join('input', 'pair0-L.png'), 0) * (1.0 / 255.0)  # grayscale, [0, 1]
R = cv2.imread(os.path.join('input', 'pair0-R.png'), 0) * (1.0 / 255.0)

# Compute disparity (using method disparity_ssd defined in disparity_ssd.py)
from disparity_ssd import disparity_ssd
D_L = disparity_ssd(L, R)
D_R = disparity_ssd(R, L)

from disparity_ncorr import disparity_ncorr
C_L = disparity_ncorr(L, R)
C_R = disparity_ncorr(R, L)

# TODO: Save output images (D_L as output/ps2-1-a-1.png and D_R as output/ps2-1-a-2.png)
# Note: They may need to be scaled/shifted before saving to show results properly
def scale(image):
    return ((image - np.min(image)) * (255.0/np.max(image)) ).astype(np.uint8)

cv2.imwrite("output/ps2-1-a-1.png", scale(D_L))
cv2.imwrite("output/ps2-1-a-2.png", scale(D_R))

# TODO: Rest of your code here
L = cv2.imread(os.path.join('input', 'pair1-L.png'), 0) * (1.0 / 255.0)  # grayscale, [0, 1]
R = cv2.imread(os.path.join('input', 'pair1-R.png'), 0) * (1.0 / 255.0)
D_L = disparity_ssd(L, R)
D_R = disparity_ssd(R, L)

cv2.imwrite("output/ps2-2-a-1.png", scale(D_L))
cv2.imwrite("output/ps2-2-a-2.png", scale(D_R))

C_L = disparity_ncorr(L, R)
C_R = disparity_ncorr(R, L)
cv2.imwrite("output/ps2-4-a-1.png", scale(C_L))
cv2.imwrite("output/ps2-4-a-2.png", scale(C_R))


L = L + np.random.randn(L.shape[0], L.shape[1])*0.03
D_L = disparity_ssd(L, R)
D_R = disparity_ssd(R, L)
cv2.imwrite("output/ps2-3-a-1.png", scale(D_L))
cv2.imwrite("output/ps2-3-a-2.png", scale(D_R))

C_L = disparity_ncorr(L, R)
C_R = disparity_ncorr(R, L)
cv2.imwrite("output/ps2-4-b-1.png", scale(C_L))
cv2.imwrite("output/ps2-4-b-2.png", scale(C_R))


L = cv2.imread(os.path.join('input', 'pair1-L.png'), 0) * (1.0 / 255.0)  # grayscale, [0, 1]
L = L * 1.1
D_L = disparity_ssd(L, R)
D_R = disparity_ssd(R, L)
cv2.imwrite("output/ps2-3-b-1.png", scale(D_L))
cv2.imwrite("output/ps2-3-b-2.png", scale(D_R))

C_L = disparity_ncorr(L, R)
C_R = disparity_ncorr(R, L)
cv2.imwrite("output/ps2-4-b-3.png", scale(C_L))
cv2.imwrite("output/ps2-4-b-4.png", scale(C_R))

L = cv2.imread(os.path.join('input', 'pair2-L.png'), 0) * (1.0 / 255.0)  # grayscale, [0, 1]
R = cv2.imread(os.path.join('input', 'pair2-R.png'), 0) * (1.0 / 255.0)
Lb = cv2.GaussianBlur(L, (13,13), 1)
Rb = cv2.GaussianBlur(R, (13,13), 1)
Ls = 1.5*L - 0.5*Lb
Rs = 1.5*R - 0.5*Rb
D_L = scale(disparity_ssd(Ls, Rs))
D_R = scale(disparity_ssd(Rs, Ls))

cv2.imwrite("output/ps2-5-a-1.png", D_L)
cv2.imwrite("output/ps2-5-a-2.png", D_R)

