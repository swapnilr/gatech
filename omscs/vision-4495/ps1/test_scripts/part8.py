# ps1
import cv2
from find_circles import find_circles
from hough_circles_acc import hough_circles_acc
from hough_peaks import hough_peaks
from hough_lines_acc import hough_lines_acc
from hough_lines_draw import hough_lines_draw_helper
import numpy as np
import cv
import time
## Real Image
def lines(overlay):
    
    img = cv2.imread('input/ps1-input3.png', 0)
    smoothed = cv2.GaussianBlur(img, (5,5), 1)
    edges = cv2.Canny(smoothed, 50, 100, apertureSize = 3)
    cv2.imshow("edges",edges)
    (H, theta, rho) = hough_lines_acc(edges)
    size = np.floor(np.asarray(H.shape) / 150.0) * 2 + 1
    peaks = hough_peaks(H, 6, NHoodSize=size)
    for peak in peaks:
        print peak
    hough_lines_draw_helper(overlay, 'output/ps1-8-a-1.png', peaks, rho, theta)

def filter_peaks(peaks, distance=50, degree_diff=2):
    filtered = []
    for i in range(len(peaks)):
        for j in range(len(peaks)):
            if i != j:
                correctDist = abs(peaks[i][0] - peaks[j][0]) < distance
                correctDeg = abs(peaks[i][1] - peaks[j][1]) < degree_diff
                if correctDist and correctDeg:
                    filtered.append(peaks[i])
    return filtered

#hough_lines_draw(smoothed, 'output/ps1-8-a-1.png', filter_peaks(peaks), rho, theta)


img = cv2.imread('input/ps1-input3.png', 0)
smoothed = cv2.GaussianBlur(img, (3,3), 1)
edges = cv2.Canny(smoothed, 100, 150, apertureSize=3)
H = hough_circles_acc(img, 20)
centers, radii = find_circles(img, range(20, 51), numCircles=15)
rgbImage = cv2.cvtColor(img, cv.CV_GRAY2RGB)
for i in range(len(centers)):
    y,x = centers[i]
    cv2.circle(rgbImage, (x,y), radii[i], cv.CV_RGB(0,255,0))
cv2.imshow("rgbImage", rgbImage)
lines(rgbImage)
time.sleep(30)
exit()
#cv2.imwrite('output/ps1-5-a-3.png', rgbImage)

# 5-b

centers, radii = find_circles(img, range(20, 51), numCircles=14)
rgbImage = cv2.cvtColor(img, cv.CV_GRAY2RGB)
for i in range(len(centers)):
    y,x = centers[i]
    cv2.circle(rgbImage, (x,y), radii[i], cv.CV_RGB(0,255,0))

cv2.imwrite('output/ps1-5b-1.png', rgbImage)

