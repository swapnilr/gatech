import cv2
from hough_lines_acc import hough_lines_acc
from hough_peaks import hough_peaks
import time
from hough_lines_draw import hough_lines_draw

i1 = cv2.imread('input/ps1-input0.png',0)
edges = cv2.Canny(i1, 100, 200)
H, t, r = hough_lines_acc(edges)
cv2.imshow("H", H)
peaks = hough_peaks(H, 10)
print peaks
hough_lines_draw(i1, None, peaks, r, t)
time.sleep(10)
cv2.destroyAllWindows()
