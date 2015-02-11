import cv2
from hough_lines_acc import hough_lines_acc
from hough_lines_acc import hough_lines_acc2
from hough_peaks import hough_peaks
from hough_peaks import hough_peaks2
import time
from hough_lines_draw import hough_lines_draw
from hough_circles_acc import hough_circles_acc
import numpy as np

def generateLines(original, edges):
    H, t, r = hough_lines_acc2(edges)
    H2 = (H * (255.0/H.max())).astype(np.uint8)
    #cv2.imshow("H", H2)
    #for i in [10.0, 25.0, 50.0, 75.0]:
    size = np.floor(np.asarray(H.shape) / 150) * 2 + 1
    #peaks = hough_peaks(H, 6, NHoodSize=size,Threshold=0.1*np.amax(H))
    peaks = hough_peaks2(H, 6)
    for peak in peaks:
          #print H.shape, peak
        print peak[0], np.radians(peak[1])
    hough_lines_draw(original, None, peaks, r, t)
    #time.sleep(10)
    #cv2.destroyAllWindows()

i1 = cv2.imread('input/ps1-input1.png',0)
i2 = cv2.GaussianBlur(i1, (3,3), 1)
edges = cv2.Canny(i2,50,150,apertureSize = 3)
lines = cv2.HoughLines(edges,1,np.pi/180,132)
print lines
lines = [[]]

for rho,theta in lines[0]:
    if theta < 1:
        continue
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(i2,(x1,y1),(x2,y2),(0,0,255),2)

#cv2.imshow("hough",i2)
#time.sleep(60)


rows, cols = i1.shape
#M = cv2.getRotationMatrix2D((cols/2,rows/2),45,1)
#cv2.imshow("noisy", i1);
#time.sleep(10)
#i1 = cv2.warpAffine(i1,M,(cols,rows))
#cv2.imshow("test", dst)
i2 = cv2.GaussianBlur(i1, (3,3), 1)
#cv2.imshow("blurred", i2)
edges = cv2.Canny(i1, 100, 200)
#cv2.imshow("edge1", edges)
edges = cv2.Canny(i2,50, 150, apertureSize = 3)
#cv2.imshow("edge2", edges)
generateLines(i1, edges)


time.sleep(60)
cv2.destroyAllWindows()
