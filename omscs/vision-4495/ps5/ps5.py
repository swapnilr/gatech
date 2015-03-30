from lk_flow import lk_flow
import util
import cv2
import numpy as np
import pyramid
import warp
from hierarchical_lk import hierarchical_lk

def upscale(image):
    return (image * 255).astype(np.uint8)

def q1a():
    init = util.readImage('input/TestSeq/Shift0.png')
    final = util.readImage('input/TestSeq/ShiftR2.png')
    final2 = util.readImage('input/TestSeq/ShiftR5U5.png')
    plotDisplacements(init, final, 'output/ps5-1-a-1.png')
    plotDisplacements(init, final2, 'output/ps5-1-a-2.png')

def q1b():
    init = util.readImage('input/TestSeq/Shift0.png')
    final = util.readImage('input/TestSeq/ShiftR10.png')
    plotDisplacements(init, final, 'output/ps5-1-b-1.png')
    final = util.readImage('input/TestSeq/ShiftR20.png')
    plotDisplacements(init, final, 'output/ps5-1-b-2.png')
    final = util.readImage('input/TestSeq/ShiftR40.png')
    plotDisplacements(init, final, 'output/ps5-1-b-3.png')

def plotDisplacements(init, final, filename):
    U,V = lk_flow(init, final)
    U = upscale(U)
    V = upscale(V)
    U = cv2.cvtColor(U,cv2.COLOR_GRAY2RGB)
    V = cv2.cvtColor(V,cv2.COLOR_GRAY2RGB)
    false_color_U = cv2.applyColorMap(U, cv2.COLORMAP_JET)
    false_color_V = cv2.applyColorMap(V, cv2.COLORMAP_JET)
    false_color = np.concatenate((false_color_U, false_color_V), axis=1)
    cv2.imwrite(filename, false_color)

def main():
    init = util.readImage('input/TestSeq/Shift0.png')
    final = util.readImage('input/TestSeq/ShiftR2.png')
    #final = util.readImage('input/TestSeq/ShiftR5U5.png')
    #final = util.readImage('input/TestSeq/ShiftR10.png')
    #final = util.readImage('input/TestSeq/ShiftR20.png')
    #final = util.readImage('input/TestSeq/ShiftR40.png')
    
    U,V = lk_flow(init, final)
    #U, V = hierarchical_lk(init, final)

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

def q2a():
    image = util.readImage('input/DataSeq1/yos_img_01.jpg')
    gauPyr = pyramid.gaussPyramid(image, 3)
    q2_helper(gauPyr, 'output/ps5-2-b-1.png')

def q2b():
    image = util.readImage('input/DataSeq1/yos_img_01.jpg')
    gauPyr = pyramid.gaussPyramid(image, 3)
    lapPyr = pyramid.laplPyramid(gauPyr)
    q2_helper(lapPyr, 'output/ps5-2-b-2.png')

def q2_helper(pyramid, filename):
    rows, columns = pyramid[0].shape
    final_image = pyramid[0]
    for p in pyramid[1:]:
        r2, c2 = p.shape
        con = np.zeros((rows, c2))
        con[0:r2, 0:c2] = p
        final_image = np.concatenate((final_image, con), axis=1)
    cv2.imwrite(filename, upscale(final_image))

def q3a():
    image1 = util.readImage('input/DataSeq1/yos_img_01.jpg')
    image2 = util.readImage('input/DataSeq1/yos_img_02.jpg')
    image3 = util.readImage('input/DataSeq1/yos_img_03.jpg')
    q3helper(image1, image2, 1)
    q3helper(image2, image3, 5)
    image1 = util.readImage('input/DataSeq2/0.png')
    image2 = util.readImage('input/DataSeq2/1.png')
    image3 = util.readImage('input/DataSeq2/2.png')
    q3helper(image1, image2, 3)
    q3helper(image2, image3, 7)

def q3helper(image1, image2, part):
    gauPyr1 = pyramid.gaussPyramid(image1, 3)
    gauPyr2 = pyramid.gaussPyramid(image2, 3)
    for i in range(len(gauPyr1)):
        plotDisplacements(gauPyr1[i].astype(np.float32), gauPyr2[i].astype(np.float32), 'output/ps5-3-a-%d-%d.png' % (part, i))
        #continue
        U,V = lk_flow(gauPyr1[i].astype(np.float32), gauPyr2[i].astype(np.float32))
        warped = warp.warp(gauPyr2[i].astype(np.float32), U, V)
        diff = warped - gauPyr1[i].astype(np.float32)
        cv2.imwrite("output/ps5-3-a-%d-%d.png" %(part + 1, i), upscale(diff))
        #import time
        #time.sleep(5)

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
    #q1a()
    #q1b()
    #q2a()
    #q2b()
    q3a()
