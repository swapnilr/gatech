import cv2
from hough_lines_acc import hough_lines_acc
from hough_peaks import hough_peaks
import time
from hough_lines_draw import hough_lines_draw
from hough_circles_acc import hough_circles_acc2
from hough_circles_acc import hough_circles_acc
import numpy as np
import cv
from find_circles import find_circles
import math

def generateLines(original, edges):
    size = 30
    optima = find_circles(original,edges, range(20, 51))
    #H = hough_circles_acc(edges, size)

    #H2 = (H * (255.0/H.max())).astype(np.uint8)
    #cv2.imshow("H", H2)
    #for i in [10.0, 25.0, 50.0, 75.0]:
    #  size = np.floor(np.asarray(H.shape) / i) * 2 + 1
    #peaks = hough_peaks(H, 10)
    rgbImage = cv2.cvtColor(original, cv.CV_GRAY2RGB)
    i = 0
    done = []
    def dist(pos1, pos2):
        y0, x0 = pos1
        y1, x1 = pos2
        return math.sqrt((y1-y0)**2 + (x1-x0)**2)

    NHoodSize = 40
    while i < 14:
        if optima.empty():
            break
        loc, radius = optima.get()[1]
        isValid = True
        for point in done:
            if dist(point, loc) < NHoodSize:
                isValid = False
                break
        if not isValid:
            continue
        i += 1
        y,x = loc
        done.append(loc)
        cv2.circle(rgbImage, (x,y), radius, cv.CV_RGB(0,255,0))
    #for peak in peaks:
    #    y,x = peak
    #    cv2.circle(rgbImage, (x,y), size, cv.CV_RGB(0,255,0))
    cv2.imshow("final", rgbImage)
    #  hough_lines_draw(original, None, peaks, r, t)
    #  time.sleep(10)
    #  cv2.destroyAllWindows()

i1 = cv2.imread('input/ps1-input1.png',0)
rows, cols = i1.shape
M = cv2.getRotationMatrix2D((cols/2,rows/2),45,1)
#cv2.imshow("noisy", i1);
#time.sleep(10)
#i1 = cv2.warpAffine(i1,M,(cols,rows))
#cv2.imshow("test", dst)
i2 = cv2.GaussianBlur(i1, (5,5), 2)
#cv2.imshow("blurred", i2)
edges = cv2.Canny(i1, 100, 200)
#cv2.imshow("edge1", edges)
edges = cv2.Canny(i2, 75, 150)
cv2.imshow("edge2", edges)

generateLines(i1, edges)
time.sleep(60)
cv2.destroyAllWindows()
