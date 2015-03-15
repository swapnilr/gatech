import cv2
import numpy as np
from scipy import signal
import cv

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
    print len(final_indices)
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


def q2():
    pass

def q3():
    pass

def main():
    q1()
    q2()
    q3()

if __name__ == '__main__':
    main()
