# ps1
import cv2
from find_circles import find_circles
from hough_circles_acc import hough_circles_acc
from hough_peaks import hough_peaks
from hough_lines_acc import hough_lines_acc
from hough_lines_draw import hough_lines_draw
from hough_lines_draw import hough_lines_draw_helper
import numpy as np
import cv

## Simple Image

print "Part 1"

# 1-a - Compute Edges
img = cv2.imread('input/ps1-input0.png', cv2.IMREAD_UNCHANGED)  # already grayscale
img_edges = cv2.Canny(img, 50, 150, apertureSize=3)
cv2.imwrite('output/ps1-1-a-1.png', img_edges) # save as output/ps1-1-a-1.png

print "Part 2"

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

## Basic Noisy Image

print "Part 3"

# 3-a - Smooth out Image 
img = cv2.imread('input/ps1-input0-noise.png', cv2.IMREAD_UNCHANGED)
smoothed = cv2.GaussianBlur(img, (7,7), 2)
cv2.imwrite('output/ps1-3-a-1.png', smoothed)

# 3-b - Find edges
edges = cv2.Canny(img, 100, 150, apertureSize=3)
cv2.imwrite('output/ps1-3-b-1.png', edges)
edges = cv2.Canny(smoothed, 100, 150, apertureSize=3)
cv2.imwrite('output/ps1-3-b-2.png', edges)

# 3-c - Find lines
(H, theta, rho) = hough_lines_acc(edges)
H2 = (H * (255.0/H.max())).astype(np.uint8)
rows, columns = H.shape
accumulator = np.zeros((rows, columns, 3), dtype=np.uint8)
accumulator[:,:,2] = H2
peaks = hough_peaks(H, 10, Threshold=0.69*np.amax(H));
for peak in peaks:
    y,x = peak
    cv2.circle(accumulator, (x,y), 10, cv.CV_RGB(255,0,0))
cv2.imwrite('output/ps1-3-c-1.png', accumulator)
hough_lines_draw(img, 'output/ps1-3-c-2.png', peaks, rho, theta)


## Real Image

print "Part 4"

# 4-a - Smoothing Image 
img = cv2.imread('input/ps1-input1.png', 0)
smoothed = cv2.GaussianBlur(img, (3,3), 1)
cv2.imwrite('output/ps1-4-a-1.png', smoothed)

# 4-b - Finding edges
edges = cv2.Canny(smoothed, 100, 150, apertureSize = 3)
cv2.imwrite('output/ps1-4-b-1.png', edges)

# 4-c - Find lines
(H, theta, rho) = hough_lines_acc(edges)
H2 = (H * (255.0/H.max())).astype(np.uint8)
rows, columns = H.shape
accumulator = np.zeros((rows, columns, 3), dtype=np.uint8)
accumulator[:,:,2] = H2
size = np.floor(np.asarray(H.shape) / 150.0) * 2 + 1
peaks = hough_peaks(H, 4, NHoodSize=size);
for peak in peaks:
    y,x = peak
    cv2.circle(accumulator, (x,y), 10, cv.CV_RGB(255,0,0))
cv2.imwrite('output/ps1-4-c-1.png', accumulator)
hough_lines_draw(img, 'output/ps1-4-c-2.png', peaks, rho, theta)

## Circles

print "Part 5"

# 5-a

img = cv2.imread('input/ps1-input1.png', 0)
smoothed = cv2.GaussianBlur(img, (3,3), 1)
cv2.imwrite('output/ps1-5-a-1.png', smoothed)
edges = cv2.Canny(smoothed, 75, 150)
cv2.imwrite('output/ps1-5-a-2.png', edges)
H = hough_circles_acc(img, 20)
centers = hough_peaks(H, 10)
rgbImage = cv2.cvtColor(img, cv.CV_GRAY2RGB)
for center in centers:
    y,x = center
    cv2.circle(rgbImage, (x,y), 20, cv.CV_RGB(0,255,0))
cv2.imwrite('output/ps1-5-a-3.png', rgbImage)

# 5-b

centers, radii = find_circles(img, range(20, 51), numCircles=14)
rgbImage = cv2.cvtColor(img, cv.CV_GRAY2RGB)
for i in range(len(centers)):
    y,x = centers[i]
    cv2.circle(rgbImage, (x,y), radii[i], cv.CV_RGB(0,255,0))
cv2.imwrite('output/ps1-5-b-1.png', rgbImage)


## Image with clutter

print "Part 6"

# 6-a - Finding Lines 
img = cv2.imread('input/ps1-input2.png', 0)
smoothed = cv2.GaussianBlur(img, (3,3), 1)
edges = cv2.Canny(smoothed, 100, 150, apertureSize = 3)

(H, theta, rho) = hough_lines_acc(edges)
size = np.floor(np.asarray(H.shape) / 150.0) * 2 + 1
peaks = hough_peaks(H, 6, NHoodSize=size);
hough_lines_draw(smoothed, 'output/ps1-6-a-1.png', peaks, rho, theta)

# 6-c - Find only pens

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

hough_lines_draw(smoothed, 'output/ps1-6-c-1.png', filter_peaks(peaks), rho, theta)

print "Part 7"

# 7-a - Find circles
img = cv2.imread('input/ps1-input2.png', 0)
smoothed = cv2.GaussianBlur(img, (5,5), 1)
edges = cv2.Canny(smoothed, 75, 125)
centers, radii = find_circles(img, range(20, 51), numCircles=15)
rgbImage = cv2.cvtColor(img, cv.CV_GRAY2RGB)
for i in range(len(centers)):
    y,x = centers[i]
    cv2.circle(rgbImage, (x,y), radii[i], cv.CV_RGB(0,255,0))
cv2.imwrite('output/ps1-7-a-1.png', rgbImage)


print "Part 8"

# 8 - Distorted image
def lines(overlay):
    img = cv2.imread('input/ps1-input3.png', 0)
    smoothed = cv2.GaussianBlur(img, (5,5), 1)
    edges = cv2.Canny(smoothed, 50, 100, apertureSize = 3)
    (H, theta, rho) = hough_lines_acc(edges)
    size = np.floor(np.asarray(H.shape) / 150.0) * 2 + 1
    peaks = hough_peaks(H, 6, NHoodSize=size)
    hough_lines_draw_helper(overlay, 'output/ps1-8-a-1.png', peaks, rho, theta)



img = cv2.imread('input/ps1-input3.png', 0)
smoothed = cv2.GaussianBlur(img, (3,3), 1)
edges = cv2.Canny(smoothed, 100, 150, apertureSize=3)
H = hough_circles_acc(img, 20)
centers, radii = find_circles(img, range(20, 51), numCircles=15)
rgbImage = cv2.cvtColor(img, cv.CV_GRAY2RGB)
for i in range(len(centers)):
    y,x = centers[i]
    cv2.circle(rgbImage, (x,y), radii[i], cv.CV_RGB(0,255,0))
lines(rgbImage)

print "Done."


