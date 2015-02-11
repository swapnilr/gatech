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
## Real Image

# 6-a - Smoothing Image 
img = cv2.imread('input/ps1-input2.png', 0)
smoothed = cv2.GaussianBlur(img, (3,3), 1)
#cv2.imshow("input", img)
# 6-b - Finding edges
edges = cv2.Canny(smoothed, 100, 150, apertureSize = 3)
#cv2.imwrite('output/ps1-4-b-1.png', edges)
cv2.imshow("edges",edges)
#time.sleep(60)
#exit()

# 4-c - Find lines
#(H, theta, rho) = hough_lines_acc(edges)
#H2 = (H * (255.0/H.max())).astype(np.uint8)
#rows, columns = H.shape
#accumulator = np.zeros((rows, columns, 3), dtype=np.uint8)
#accumulator[:,:,2] = H2
#size = np.floor(np.asarray(H.shape) / 150.0) * 2 + 1
#peaks = hough_peaks(H, 6, NHoodSize=size);
#for peak in peaks:
#    print peak
#    y,x = peak
#    cv2.circle(accumulator, (x,y), 10, cv.CV_RGB(255,0,0))
#cv2.imwrite('output/ps1-4-c-1.png', accumulator)
#hough_lines_draw(smoothed, 'output/ps1-6-a-1.png', peaks, rho, theta)

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

#hough_lines_draw(smoothed, 'output/ps1-6-c-1.png', filter_peaks(peaks), rho, theta)


img = cv2.imread('input/ps1-input2.png', 0)
smoothed = cv2.GaussianBlur(img, (3,3), 1)
edges = cv2.Canny(smoothed, 100, 150, apertureSize=3)
H = hough_circles_acc(img, 20)
centers = hough_peaks(H, 10)
rgbImage = cv2.cvtColor(img, cv.CV_GRAY2RGB)
for center in centers:
    y,x = center
    cv2.circle(rgbImage, (x,y), 20, cv.CV_RGB(0,255,0))
cv2.imshow("rgbImage", rgbImage)
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

