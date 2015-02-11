import cv2
import numpy as np
import cv

def hough_lines_draw(img, outfile, peaks, rho, theta):
    rgbImage = cv2.cvtColor(img, cv.CV_GRAY2RGB)
    hough_lines_draw_helper(rgbImage, outfile, peaks, rho, theta)

def hough_lines_draw_helper(rgbImage, outfile, peaks, rho, theta):
    for peak in peaks:
        t = np.radians(theta[peak[1]])
        p = rho[peak[0]]
        cosTheta = np.cos(t)
        sinTheta = np.sin(t)
        x = p * cosTheta
        y = p * sinTheta
        x1 = int(x + 1000 * (-sinTheta))
        y1 = int(y + 1000 * (cosTheta))
        x2 = int(x - 1000 * (-sinTheta))
        y2 = int(y - 1000 * (cosTheta))

        cv2.line(rgbImage,(x1,y1),(x2,y2),cv.CV_RGB(0,255,0))
    cv2.imwrite(outfile, rgbImage)
    return rgbImage


