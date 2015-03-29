from lk_flow import lk_flow
import util
import cv2
import numpy as np
import pyramid
import warp

def upscale(image):
    return (image * 255).astype(np.uint8)

def main():
    init = util.readImage('input/TestSeq/Shift0.png')
    final = util.readImage('input/TestSeq/ShiftR2.png')
    #final = util.readImage('input/TestSeq/ShiftR5U5.png')
    #final = util.readImage('input/TestSeq/ShiftR10.png')
    #final = util.readImage('input/TestSeq/ShiftR20.png')
    #final = util.readImage('input/TestSeq/ShiftR40.png')
    
    U,V = lk_flow(init, final)

    U = upscale(U)
    V = upscale(V)

    U = cv2.cvtColor(U,cv2.COLOR_GRAY2RGB)
    V = cv2.cvtColor(V,cv2.COLOR_GRAY2RGB)

    false_color_U = cv2.applyColorMap(U, cv2.COLORMAP_JET)
    false_color_V = cv2.applyColorMap(V, cv2.COLORMAP_JET)
     
    #namedWindow("window")
    cv2.imshow("U", false_color_U)
    cv2.imshow("V", false_color_V)

    import time
    time.sleep(30)

def main2():
    image = util.readImage('input/DataSeq1/yos_img_01.jpg')
    gauPyr = pyramid.gaussPyramid(image, 4)
    import time
    for p in gauPyr:
        cv2.imshow("img", upscale(p))
        time.sleep(5)
        cv2.destroyAllWindows()

def main3():
    init = util.readImage('input/TestSeq/Shift0.png')
    final = util.readImage('input/TestSeq/ShiftR2.png')
    U,V = lk_flow(init, final)
    warped = warp.warp(final, U, V)
    cv2.imshow("original", init)
    cv2.imshow("modified", warped)
    import time
    time.sleep(30)

if __name__ == '__main__':
    main3()
