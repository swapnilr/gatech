import cv2
import numpy as np
from scipy import signal
import cv
import math

# Harris Corners
KERNEL_SIZE = 5
SIGMA = 1
ALPHA = 0.05

def gradientX(image):
    #kernel = cv2.getGaussianKernel(KERNEL_SIZE, SIGMA)
    filtered = cv2.GaussianBlur(image, (KERNEL_SIZE, KERNEL_SIZE), SIGMA)
    width, height = image.shape
    output = np.zeros((width, height))
    for y in range(width):
        for x in range(height):
            x2 = min(x + 1, height - 1)
            output[y, x] = filtered[y, x2] - filtered[y, x]
    return output

def gradientY(image):
    filtered = cv2.GaussianBlur(image, (KERNEL_SIZE, KERNEL_SIZE), SIGMA)
    width, height = image.shape
    output = np.zeros((width, height))
    for y in range(width):
        for x in range(height):
            y2 = min(y + 1, width - 1)
            output[y, x] = filtered[y2, x] - filtered[y, x]
    return output

def scale(image):
    shifted = (image - np.amin(image))
    scaled = shifted/(np.amax(shifted))
    return scaled

def computeGradient(image):
    gradX = scale(gradientX(image))
    gradY = scale(gradientY(image))
    return gradX, gradY

def upscale(image):
    return (image * 255).astype(np.uint8)

def writeImage(gradX, gradY, output_fn):
    #print gradX.shape, gradY.shape
    image = upscale(np.concatenate((gradX, gradY), axis=1))
    cv2.imwrite(output_fn, image)

def q1a():
    transA = cv2.imread('input/transA.jpg', cv2.IMREAD_GRAYSCALE).astype(np.float_)
    # Scale the image to [0.0, 1.0]
    transA /= 255.0
    gradX, gradY = computeGradient(transA)
    writeImage(gradX, gradY, 'output/ps4-1-a-1.png')
    
    simA = cv2.imread('input/simA.jpg', cv2.IMREAD_GRAYSCALE).astype(np.float_)
    # Scale the image to [0.0, 1.0]
    simA /= 255.0
    gradX, gradY = computeGradient(simA)
    writeImage(gradX, gradY, 'output/ps4-1-a-2.png')


def harrisValue(image):
    gradX, gradY = computeGradient(image)
    kernel = cv2.getGaussianKernel(KERNEL_SIZE, SIGMA)
    wX = signal.convolve(gradX * gradX, kernel, mode='same')
    wXY = signal.convolve(gradX * gradY, kernel, mode='same')
    wY = signal.convolve(gradY * gradY, kernel, mode='same')

    #determinant and trace
    det = wX * wY - wXY**2
    trace = wX + wY

    return det - ALPHA*(trace**2)

def q1b():
    transA = cv2.imread('input/transA.jpg', cv2.IMREAD_GRAYSCALE).astype(np.float_)
    # Scale the image to [0.0, 1.0]
    transA /= 255.0
    hv = harrisValue(transA)
    cv2.imwrite('output/ps4-1-b-1.png', upscale(scale(hv)))
    
    transB = cv2.imread('input/transB.jpg', cv2.IMREAD_GRAYSCALE).astype(np.float_)
    # Scale the image to [0.0, 1.0]
    transB /= 255.0
    hv = harrisValue(transB)
    cv2.imwrite('output/ps4-1-b-2.png', upscale(scale(hv)))

    simA = cv2.imread('input/simA.jpg', cv2.IMREAD_GRAYSCALE).astype(np.float_)
    # Scale the image to [0.0, 1.0]
    simA /= 255.0
    hv = harrisValue(simA)
    cv2.imwrite('output/ps4-1-b-3.png', upscale(scale(hv)))

    simB = cv2.imread('input/simB.jpg', cv2.IMREAD_GRAYSCALE).astype(np.float_)
    # Scale the image to [0.0, 1.0]
    simB /= 255.0
    hv = harrisValue(simB)
    cv2.imwrite('output/ps4-1-b-4.png', upscale(scale(hv)))

def get_points(hv, threshold, radius):
    threshold_val = np.amax(hv) * threshold
    im_thresh = (hv > threshold_val) * 1

    points = im_thresh.nonzero()
    #print len(points[0])
    indices = [ (points[0][index], points[1][index]) for index in range(len(points[0]))]
    values = [ hv[index] for index in indices]

    sorted_loc = np.argsort(values)

    valid = np.zeros(hv.shape)
    valid[radius:-radius,radius:-radius] = 1
    
    final_indices = []
    for loc in sorted_loc:
        y, x = indices[loc]
        if valid[y, x] == 1:
            final_indices.append((y, x))
            valid[ y-radius: y+radius, x-radius:x+radius] = 0
    #print len(final_indices)
    return final_indices


    #import time
    #cv2.imshow("t", upscale(im_thresh))
    #time.sleep(30)

def writeImage(image, points, output_fn):
    im = cv2.cvtColor(upscale(image), cv2.COLOR_GRAY2RGB)
    for point in points:
        cv2.circle(im, (int(point[1]), int(point[0])), 3, cv.CV_RGB(0,255,0))
    cv2.imwrite(output_fn, im)

def writePoints(input_fn, output_fn, threshold=0.8, radius=10):
    im = cv2.imread(input_fn, cv2.IMREAD_GRAYSCALE).astype(np.float_)
    # Scale the image to [0.0, 1.0]
    im /= 255.0
    hv = harrisValue(im)
    points = get_points(scale(hv), threshold=threshold, radius=radius)
    writeImage(im, points, output_fn)

def q1c():
    writePoints('input/transA.jpg', 'output/ps4-1-b-1.png', 0.82)
    writePoints('input/transB.jpg', 'output/ps4-1-b-2.png', 0.82)
    writePoints('input/simA.jpg', 'output/ps4-1-b-3.png')
    writePoints('input/simB.jpg', 'output/ps4-1-b-4.png', 0.78)

def q1():
    q1a()
    q1b()
    q1c()

# SIFT Features
SIZE = 3

def getKeyPoints(image, threshold=0.8, radius=10):
    gradX, gradY = computeGradient(image)
    angle = np.degrees(np.arctan2(gradY, gradX))
    hv = harrisValue(image)
    points = get_points(scale(hv), threshold=threshold, radius=radius)
    keyPoints = []
    for pt in points:
        point = cv2.KeyPoint(x=pt[1], y=pt[0], _size=radius, _angle=angle[pt], _octave=0)
        keyPoints.append(point)
    return keyPoints

def drawKeyPoints(image1, image2, output_fn, threshold=0.8, radius=10):
    points = getKeyPoints(image1, threshold, radius)
    colored1 = cv2.cvtColor(upscale(image1), cv2.COLOR_GRAY2RGB)
    image1 = cv2.drawKeypoints(colored1, points, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    points = getKeyPoints(image2, threshold, radius)
    colored2 = cv2.cvtColor(upscale(image2), cv2.COLOR_GRAY2RGB)
    image2 = cv2.drawKeypoints(colored2, points, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    final = np.concatenate((image1, image2), axis=1)
    cv2.imwrite(output_fn, final)

def readScaled(input_fn):
    im = cv2.imread(input_fn, cv2.IMREAD_GRAYSCALE).astype(np.float_)
    # Scale the image to [0.0, 1.0]
    im /= 255.0
    return im

def q2a():
    drawKeyPoints(readScaled('input/transA.jpg'), 
                  readScaled('input/transB.jpg'), 'output/ps4-2-a-1.png',
                  threshold=0.85)
    drawKeyPoints(readScaled('input/simA.jpg'), 
                  readScaled('input/simB.jpg'), 'output/ps4-2-a-2.png',
                  threshold=0.78)



def drawPair(image1, image2, output_fn, threshold=0.8, radius=10):
    sift = cv2.SIFT()

    points1 = getKeyPoints(image1, threshold, radius)
    points1, descriptors1 = sift.compute(upscale(image1), points1)
    
    points2 = getKeyPoints(image2, threshold, radius)
    points2, descriptors2 = sift.compute(upscale(image2), points2)

    bfm = cv2.BFMatcher()
    matches = bfm.match(descriptors1, descriptors2)

    colored1 = cv2.cvtColor(upscale(image1), cv2.COLOR_GRAY2RGB)
    colored2 = cv2.cvtColor(upscale(image2), cv2.COLOR_GRAY2RGB)
    final = np.concatenate((colored1, colored2), axis=1)

    rows, columns, dim = colored1.shape


    for dmatch in matches:
        point1 = points1[dmatch.queryIdx].pt
        point2 = points2[dmatch.trainIdx].pt
        cv2.line(final, (int(point1[0]), int(point1[1])), (int(point2[0]) + columns, int(point2[1])), cv.CV_RGB(0,255,0))
    cv2.imwrite(output_fn, final)

def q2b():
    drawPair(readScaled('input/transA.jpg'),
                  readScaled('input/transB.jpg'), 'output/ps4-2-b-1.png',
                  threshold=0.85)
    drawPair(readScaled('input/simA.jpg'),
                  readScaled('input/simB.jpg'), 'output/ps4-2-b-2.png',
                  threshold=0.78)

def q2():
    q2a()
    q2b()

def q3():
    pass

def main():
    #q1()
    q2()
    q3()

if __name__ == '__main__':
    main()
