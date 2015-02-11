# ps1
import cv2
from find_circles import find_circles
from hough_circles_acc import hough_circles_acc
from hough_peaks import hough_peaks
from hough_lines_acc import hough_lines_acc
from hough_lines_draw import hough_lines_draw
import numpy as np
import cv
## Simple Image

# 1-a - Compute Edges
img = cv2.imread('input/ps1-input0.png', cv2.IMREAD_UNCHANGED)  # already grayscale
img_edges = cv2.Canny(img, 50, 150, apertureSize=3)
cv2.imwrite('output/ps1-1-a-1.png', img_edges) # save as output/ps1-1-a-1.png

# 2-a - Get Hough Accumulator Array
(H, theta, rho) = hough_lines_acc(img_edges);  # defined in hough_lines_acc.py
# Normalize accumulator array
H2 = (H * (255.0/H.max())).astype(np.uint8)
rows, columns = H.shape
accumulator = np.zeros((rows, columns, 3), dtype=np.uint8)
accumulator[:,:,2] = H2
cv2.imwrite('output/ps1-2-a-1.png', accumulator)

# 2-b - Get Peaks
peaks = hough_peaks(H, 10);  # defined in hough_peaks.py
for peak in peaks:
    y,x = peak
    cv2.circle(accumulator, (x,y), 10, cv.CV_RGB(255,0,0))
cv2.imwrite('output/ps1-2-b-1.png', accumulator)

# 2-c - Draw lines
hough_lines_draw(img, 'output/ps1-2-c-1.png', peaks, rho, theta)
