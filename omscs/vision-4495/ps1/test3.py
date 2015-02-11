import cv2
from hough_lines_acc import hough_lines_acc
from hough_peaks import hough_peaks
import time
from hough_lines_draw import hough_lines_draw
from hough_circles_acc import hough_circles_acc
import numpy as np

def generateLines(original, edges):
    H, t, r = hough_lines_acc(edges)
    H2 = (H * (255.0/H.max())).astype(np.uint8)
    cv2.imshow("H", H2)
    peaks = hough_peaks(H, 6)
    hough_lines_draw(original, None, peaks, r, t)

i1 = cv2.imread('input/ps1-input0-noise.png',0)
rows, cols = i1.shape
M = cv2.getRotationMatrix2D((cols/2,rows/2),45,1)
cv2.imshow("noisy", i1);
#time.sleep(10)
#i1 = cv2.warpAffine(i1,M,(cols,rows))
#cv2.imshow("test", dst)
i2 = cv2.GaussianBlur(i1, (7,7), 2)
cv2.imshow("blurred", i2)
edges = cv2.Canny(i1, 100, 200)
cv2.imshow("edge1", edges)
edges = cv2.Canny(i2, 75, 150)
cv2.imshow("edge2", edges)
generateLines(i2, edges)
time.sleep(20)
cv2.destroyAllWindows()
