# ps1
import cv2
from find_circles import find_circles
from hough_circles_acc import hough_circles_acc
from hough_peaks import hough_peaks
from hough_lines_acc import hough_lines_acc
from hough_lines_draw import hough_lines_draw
import numpy as np
import cv
import time

img = cv2.imread('input/ps1-input2.png', 0)
smoothed = cv2.GaussianBlur(img, (3,3), 1)
edges = cv2.Canny(smoothed, 100, 100, apertureSize=3)
cv2.imshow("edges", edges)
centers, radii = find_circles(img, range(20, 51), numCircles=14)
rgbImage = cv2.cvtColor(img, cv.CV_GRAY2RGB)
for i in range(len(centers)):
    y,x = centers[i]
    cv2.circle(rgbImage, (x,y), radii[i], cv.CV_RGB(0,255,0))
#H = hough_circles_acc(img, 20)
#centers = hough_peaks(H, 10)
#rgbImage = cv2.cvtColor(img, cv.CV_GRAY2RGB)
#for center in centers:
#    y,x = center
#    cv2.circle(rgbImage, (x,y), 20, cv.CV_RGB(0,255,0))
cv2.imwrite('output/ps1-7a-1.png', rgbImage)

