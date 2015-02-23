# ps2
import os
import numpy as np
import cv2
import time

from disparity_ssd import disparity_ssd
from disparity_ncorr import disparity_ncorr

def scale(image):
    return ((image - np.min(image)) * (255.0/np.max(image)) ).astype(np.uint8)

## 1-a
# Read images
L = cv2.imread(os.path.join('input', 'pair2-L.png'), 0) * (1.0 / 255.0)  # grayscale, [0, 1]
R = cv2.imread(os.path.join('input', 'pair2-R.png'), 0) * (1.0 / 255.0)

D_L = scale(disparity_ssd(L, R))
D_R = scale(disparity_ssd(R, L))

C_L = scale(disparity_ncorr(L, R))
C_R = scale(disparity_ncorr(R, L))
cv2.imwrite("part5-original-ssd-L.png", D_L)
cv2.imwrite("part5-original-ssd-R.png", D_R)
cv2.imwrite("part5-original-ncorr-L.png", C_L)
cv2.imwrite("part5-original-ncorr-R.png", C_R)
# Compute disparity (using method disparity_ssd defined in disparity_ssd.py)
for i in range(3, 16, 2):
    for j in [1, 5, 10]:
      if j < i: 
        # Blur
        Lb = cv2.GaussianBlur(L, (i,i), j)
        Rb = cv2.GaussianBlur(R, (i,i), j)
        D_L = scale(disparity_ssd(Lb, Rb))
        D_R = scale(disparity_ssd(Rb, Lb))

        C_L = scale(disparity_ncorr(Lb, Rb))
        C_R = scale(disparity_ncorr(Rb, Lb))
        cv2.imwrite("part5-%d-%d-blurred-ssd-L.png" % (i,j), D_L)
        cv2.imwrite("part5-%d-%d-blurred-ssd-R.png" % (i,j), D_R)
        cv2.imwrite("part5-%d-%d-blurred-ncorr-L.png" % (i,j), C_L)
        cv2.imwrite("part5-%d-%d-blurred-ncorr-R.png" % (i,j), C_R)
        # Sharpen
        Ls = 1.5*L - 0.5*Lb
        Rs = 1.5*R - 0.5*Rb
        D_L = scale(disparity_ssd(Ls, Rs))
        D_R = scale(disparity_ssd(Rs, Ls))

        C_L = scale(disparity_ncorr(Ls, Rs))
        C_R = scale(disparity_ncorr(Rs, Ls))
        cv2.imwrite("part5-%d-%d-sharpened-ssd-L.png" % (i,j), D_L)
        cv2.imwrite("part5-%d-%d-sharpened-ssd-R.png" % (i,j), D_R)
        cv2.imwrite("part5-%d-%d-sharpened-ncorr-L.png" % (i,j), C_L)
        cv2.imwrite("part5-%d-%d-sharpened-ncorr-R.png" % (i,j), C_R)

