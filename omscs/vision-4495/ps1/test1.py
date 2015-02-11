import cv2
from hough_lines_acc import hough_lines_acc
from hough_peaks import hough_peaks
import time
from hough_lines_draw import hough_lines_draw
from hough_circles_acc import hough_circles_acc
import numpy as np
from hough_lines_acc import hough_lines_acc2

i1 = cv2.imread('input/ps1-input0.png',0)
rows, cols = i1.shape
M = cv2.getRotationMatrix2D((cols/2,rows/2),12,1)
i1 = cv2.warpAffine(i1,M,(cols,rows))
#cv2.imshow("test", dst)
edges = cv2.Canny(i1, 100, 200)
#H, t, r = hough_lines_acc(edges)
#H2 = (H * (255.0/H.max())).astype(np.uint8)
#cv2.imshow("H1", H2)
H, t, r = hough_lines_acc2(edges)
H2 = (H * (255.0/H.max())).astype(np.uint8)
cv2.imshow("H", H2)
peaks = hough_peaks(H, 10)
#print peaks
hough_lines_draw(i1, None, peaks, r, t)
#circles = hough_circles_acc(edges, 20)
#cv2.imshow("hough", circles)
time.sleep(60)
cv2.destroyAllWindows()
