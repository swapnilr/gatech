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
    for peak in peaks:
        print peak
        t = np.radians(theta[peak[1]])
        p = rho[peak[0]]
        if t == 0:
            print p
            cv2.line(rgbImage, (int(p),0), (int(p),img.shape[0]), cv.CV_RGB(0,255,0))
        else:
            #rho,theta = peak
            a = np.cos(t)
            b = np.sin(t)
            x0 = a*p
            y0 = b*p
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(rgbImage,(x1,y1),(x2,y2),cv.CV_RGB(0,255,0))#(0,0,255),2)

            #print p, theta[peak[1]], np.cos(t), np.sin(t)
            #cv2.line(rgbImage, (0, int(p/np.sin(t))), (img.shape[1], int((p - np.cos(t)*img.shape[0])/np.sin(t))), cv.CV_RGB(0,255,0))
    #for col in range(img.shape[1]):
    #    for peak in peaks:
    #        t = np.radians(theta[peak[1]])
    #        p = rho[peak[0]]
    #        if t == 0:
    #            #cv2.line(rgbImage, (), ()
    #            for row in range(img.shape[0]):
    #                rgbImage[row, col, 1] = 255
    #        else:
    #            #row = (p - (col * np.cos(t)))/np.sin(t)
    #            print p, t, row, col
    #            #rgbImage[row,col,2] = 255
    cv2.imshow("im", rgbImage)
    return rgbImage
