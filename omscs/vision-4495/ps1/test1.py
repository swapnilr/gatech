import cv2
i1 = cv2.imread('input/ps1-input0.png',0)
edges = cv2.Canny(i1, 100, 200)
from hough_lines_acc import hough_lines_acc
H, t, r = hough_lines_acc(edges)
cv2.imshow("H", H)
from hough_peaks import hough_peaks
peaks = hough_peaks(H, 10)
print peaks
import time
time.sleep(10)
cv2.destroyAllWindows()
