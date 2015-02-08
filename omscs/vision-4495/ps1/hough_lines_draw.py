import cv2
import numpy as np
import cv

def hough_lines_draw(img, outfile, peaks, rho, theta):
    #     % Draw lines found in an image using Hough transform.
    #     %
    #     % img: Image on top of which to draw lines
    #     % outfile: Output image filename to save plot as
    #     % peaks: Qx2 matrix containing row, column indices of the Q peaks found in accumulator
    #     % rho: Vector of rho values, in pixels
    #     % theta: Vector of theta values, in degrees
    # 
    #     % TODO: Your code here
    rgbImage = cv2.cvtColor(img, cv.CV_GRAY2RGB)
    for col in range(img.shape[1]):
        for peak in peaks:
            t = np.radians(theta[peak[1]])
            p = rho[peak[0]]
            if t == 0:
                for row in range(img.shape[0]):
                    rgbImage[row, col, 2] = 255
            else:
                print peak, peak[1], theta[peak[1]], t, np.tan(t), np.sin(t)
                row = -(1/np.tan(t)) * col + (p * (1/np.sin(t)))
                rgbImage[row,col,2] = 255
    cv2.imshow(rgbImage)
    return rgbImage
