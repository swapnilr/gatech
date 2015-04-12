# ASSIGNMENT 10
# Your Name

""" Assignment 10 - Building an HDR image

This file has a number of functions that you need to fill out in order to
complete the assignment. Please write the appropriate code, following the
instructions on which functions you may or may not use.

GENERAL RULES:
    1. DO NOT INCLUDE code that saves, shows, displays, writes the image that
    you are being passed in. Do that on your own if you need to save the images
    but the functions should NOT save the image to file. (This is a problem
    for us when grading because running 200 files results a lot of images being
    saved to file and opened in dialogs, which is not ideal). Thanks.

    2. DO NOT import any other libraries aside from the three libraries that we
    provide. You may not import anything else, you should be able to complete
    the assignment with the given libraries (and in most cases without them).

    3. DO NOT change the format of this file. Do not put functions into classes,
    or your own infrastructure. This makes grading very difficult for us. Please
    only write code in the allotted region.

"""

import cv2
import logging
import numpy as np
import os
import random


def normalizeImage(img):
    """ This function normalizes an image from any range to 0->255.0.

    Note: This sounds simple, but be very careful about getting this right. I
    heavily suggest you follow the steps listed below.

    1. Set 'out' equal to 'img' subtracted by the minimum of the image. For 
    example, if your image range is from 10->20, subtracting the minimum will 
    make the range from 0->10. The benefit of this is that if the range is from
    -10 to 10, it will set the range to be from 0->20. Since we will have to
    deal with negative values, it is important you normalize the function this
    way. We do the rounding for you so do not do any casting or rounding for the
    input values (a value like 163.92 will be cast to 163 by the return
    statement that casts everything to a uint8).

    2. Now, multiply 'out' by (255 / max) where max is the max value of 'out'.
    This max is computed after you subtract the minimum (not before).

    3. return out.

    Args:
        img (numpy.ndarray): A grayscale or color image represented in a numpy
                             array. (dtype = np.float)

    Returns:
        out (numpy.ndarray): A grasycale or color image of dtype uint8, with
                             the shape of img, but values ranging from 0->255.
    """
    # We initialize this as float since you will do arithmetic computation.
    out = np.zeros(img.shape, dtype=np.float)
    # WRITE YOUR CODE HERE.
    out = img.astype(np.float) - np.amin(img)
    out = out * (255/np.amax(out))



    # END OF FUNCTION.
    # We handle casting your matrix to a uint8. If your values do not range from
    # 0->255 this will produce overflow casting which would be erroneous.
    return np.uint8(out)
def linearWeight(pixel_value):
    """ Linear Weighting function based on pixel location.

    Note: This is a very simple weight function, we provide pseudocode below
    that should make this straightforward to implement.

    1. This function behaves as follows:
        if the pixel_value is > pixel_range_mid:
            weight = pixel_range_max - val
        else:
            weight = the pixel_value as a float.

    Args:
        pixel_value(np.uint8): A value from 0 to 255.

    Returns:
        weight(np.float): A value from 0.0 to 255.0 


    """
    # Function definitions (we refer to these values in the function desc.)
    pixel_range_min = 0.0
    pixel_range_max = 255.0
    pixel_range_mid = 0.5 * (pixel_range_min + pixel_range_max)
    weight = 0.0

    # WRITE YOUR CODE HERE.
    if pixel_value > pixel_range_mid:
        weight = pixel_range_max - pixel_value
    else:
        weight = float(pixel_value)



    # END OF FUNCTION.
    return weight

def getYXLocations(image, intensity_value):
    """ This function gets the Y, X locations of an image at a certain intensity
    value.

    It's easy to describe how to do this visually. Imagine you have a grayscale
    image that is 4x4.
    my_image = [ [ 17, 200,  48,  10],
                 [ 98, 151,  41, 182],
                 [128, 190,  98, 209],
                 [249,  27, 129, 182]]

    Now assume I ask you to return getYXLocations(my_image, 98)

    You have to return the y and x locations of where 98 appears, so in this
    case, 98 appears at 1, 0 and at 2, 2, so your function should return
    y_locs = [1, 2] and x_locs = [0, 2].

    Hint: There is a numpy function that will essentially allow you to do this
    efficiently & succintly. May be worth looking into ;).

    The less efficient but equally valid way of doing this:
    1. Iterate through the rows (y) and columns (x) of the image.
    2. if image[y, x] == intensity_value, append y to y_locs and x to x_locs.
    3. return y_locs, x_locs.

    Args:
        image (numpy.ndarray): Input grayscale image.
        intensity_value (numpy.uint8): Assume a value from 0->255.

    Returns:
        y_locs (numpy.ndarray): Array containing integer values for the y
                                locations of input intensity. Type np.int64.
        x_locs (numpy.ndarray): Array containing integer values for the x
                                locations of input intensity. Type np.int64.
    """
    # WRITE YOUR CODE HERE.


    return np.transpose(np.argwhere(image == intensity_value))
    
    # END OF FUNCTION

def computeResponseCurve(pixels, log_exposures, smoothing_lambda,
                         weighting_function):
    """ Find camera response curve for one color channel.

    Note: This is the most complicated function. We provide a decent start to
    this implementation. We want you to fill in certain sections within for
    loops and for some simple linear algebra in order to complete the
    implementation.

    Note(2): For those of you unfamiliar with Python and getting to learn it
    this semester, this will have something "weird". weighting_function is not
    a value, but rather a function. This means we pass in the name of a function
    and then within the computeResponseCurve function you can use it to compute
    the weight (so you can do weighting_function(10) and it will return a
    weight). You can see how we use weighting_function below. Feel free to ask
    questions on Piazza if the concept doesn't click in.

    Solves for x in Ax=b -> returns g where g=x[0:n]

    PART 1:
        In this part, you will fill in mat_A and mat_b with values from the
        weighting function. We have already obtained the value `wij` and now
        we need to assign it. The general idea behind creating matrix A and
        matrix b are to solve the matrix Ax = b where x is what we want to
        solve for. The idea is that we can get the correct distribution of
        intensity values by taking numerous images and their exposures and
        seeing how the pixel intensity changes based on the exposure.

        WHAT TO DO?
        1a. Set mat_A at idx_ctr, pixel_value to the value of the weighting
            function (wij). pixel_value is the value in pixels at i, j.
        1b. Set mat_A at idx_ctr, pix_range + i to the negative value of the
            weighting function.
        1c. Set mat_b at idx_ctr, 0 to the value of the weighting function
            multiplied by the log_exposure at j.

    PART 2:
        In this part we do some simple linear algebra. We are solving the
        function Ax=b. We want to solve for x. We have A and b.

        Ax = b.
        A^-1 * A * x = b.   (Note: the * multiply is the dot product here, but
                             in Python it performs an element-wise
                             multiplication so don't use it). What we want is
                             something like: my_mat.dot(other_mat)
        x = A^-1 * b.

        Pretty simple. x is the inverse of A dot b. Now, it gets a little bit
        more difficult because we can't obtain the inverse of a matrix that is
        not square. We can however use a method to get the pseudoinverse.

        This method is called the Moore-Penrose Pseudoinverse of a Matrix.

        WHAT TO DO?
        1a. Get the pseudoinverse of A. Numpy has an implementation of the
        Moore-Penrose Pseudoinverse, so this is just a function call.
        1b. Multiply that psuedoinverse -- dot -- b. This becomes x. Make sure
        x is of the size 512 x 1.

    Args:
        pixels (numpy.ndarray): Single channel input values
                                (num_pixels x num_images).
        log_exposures(numpy.ndarray): Log exposure times (size == num_images)
        smoothing_lambda(numpy.int): The smoothness constant.
        weighting_function: Function that computes the weights.

    Returns:
        g(z): log exposure corresponding to pixel value z

    """
    pix_range = pixels.shape[0]
    num_images = len(log_exposures)
    # pix_range * 2 equates to range of pixels + number of unique pixels.
    mat_A = np.zeros((num_images * pix_range + pix_range - 1, pix_range * 2),
                     dtype=np.float64)
    mat_b = np.zeros((mat_A.shape[0], 1), dtype=np.float64)

    # Create data-fitting equations
    idx_ctr = 0  # index counter
    for i in xrange(pix_range):
        for j in xrange(num_images):
            wij = weighting_function(pixels[i, j])
            # PART 1: WRITE YOUR CODE HERE
            mat_A[idx_ctr, pixels[i,j]] = wij
            mat_A[idx_ctr, pix_range + i] = -wij
            mat_b[idx_ctr, 0] = wij * log_exposures[j]
            # STOP WRITING CODE HERE.
            idx_ctr = idx_ctr + 1

    # Apply smoothing lambda throughout the pixel range.
    idx = pix_range * num_images
    for i in xrange(pix_range - 1):
        mat_A[idx + i, i] = smoothing_lambda * weighting_function(i)
        mat_A[idx + i, i + 1] = -2 * smoothing_lambda * weighting_function(i)
        mat_A[idx + i, i + 2] = smoothing_lambda * weighting_function(i)

    # Adjust color curve by setting its middle value to 0
    mat_A[-1, (pix_range / 2) + 1] = 0

    # Solve the system using Single Value Decomposition
    # Ax = b | x = A^-1 * b

    # PART 2: WRITE YOUR CODE HERE
    x = np.dot(np.linalg.pinv(mat_A), mat_b)


    # STOP WRITING CODE HERE.

    # x should be a 512 x 1 matrix (we slice it and only return 0->255).
    g = x[0:pix_range]
    return g[:,0]

def readImages(image_dir, resize=False):
    """ This function reads in input images from a image directory

    Note: This is implemented for you since its not really relevant to
    computational photography (+ time constraints).

    Don't modify this function.

    Args:
        image_dir(str): The image directory to get images from.
        resize(bool): Downsample the images by 1/4th.

    Returns:
        images(list): List of images in image_dir. Each image in the list is of
                      type numpy.ndarray.
        images_gray(list): List of images (grayscale) in image_dir.

    """
    # The main file extensions. Feel free to add more if you want to test on
    # an image format of yours that isn't listed (Make sure OpenCV can read it).
    file_extensions = ["jpg", "jpeg", "png", "bmp"]
    # Get all files in folder.
    image_files = sorted(os.listdir(image_dir))
    # Remove files that do not have the appropriate extension.
    for img in image_files:
        if img.split(".")[-1].lower() not in file_extensions:
            image_files.remove(img)

    # Read in the gray and color images.
    num_images = len(image_files)
    images = [None] * num_images
    images_gray = [None] * num_images
    for image_idx in xrange(num_images):
        images[image_idx] = cv2.imread(os.path.join(image_dir,
                                                    image_files[image_idx]))
        images_gray[image_idx] = cv2.cvtColor(images[image_idx],
                                              cv2.COLOR_BGR2GRAY)
        if resize:
            images[image_idx] = images[image_idx][::4,::4]
            images_gray[image_idx] = images_gray[image_idx][::4,::4]
    return images, images_gray

def computeHDR(image_dir, log_exposure_times, smoothing_lambda = 100,
               resize = False):
    """ This function does the actual HDR computation.

    Note: This brings together all of the functions above. Don't modify this.

    The basic overview is below:
    1. Read in images. (readImages function)
    2. Define some defaults.
    3. Get random YX locations for each intensity values. (getYXLocations)
    4. Get intensity values for each YX location. (done in function)
    5. Compute response curves for each channel. (computeResponseCurve)
        Note: We pass in the linearWeight function here.
    6. Build image radiance map from response curves.
    7. Normalize the image radiance map.

    Note(2): We do not perform tone mapping which is an additional step of HDR
    images due to filters which are not readily available in the libraries we
    use. There are great resources for how to do this but the output image will
    give you a decent idea of how tone mapping can be performed. This is why the
    output will not have as many bright tones as some HDR algorithms output.

    Args:
        image_dir(str): The input directory.
        log_exposure_times(numpy.ndarray): The log exposure times.
        smoothing_lambda(np.int): A constant lambda value.
        resize(bool): Should you resize the input.

    Returns:
        hdr_image(numpy.ndarray): The HDR image.
    """
    # STEP 1: Read in images from provided directory.
    images, images_gray = readImages(image_dir, resize)
    num_images = len(images)

    # STEP 2: Define default values.
    pixel_range_min = 0.0
    pixel_range_max = 255.0
    pixel_range_mid = 0.5 * (pixel_range_min + pixel_range_max)
    num_points = int(pixel_range_max + 1)
    image_size = images[0].shape[0:2]

    # Obtain the number of channels from the image shape.
    if len(images[0].shape) == 2:
        num_channels = 1
        logging.warning("WARNING: This is a single channel image. This code " +\
                        "has not been fully tested on single channel images.")
    elif len(images[0].shape) == 3:
        num_channels = images[0].shape[2]
    else:
        logging.error("ERROR: Image matrix shape is of size: " + 
                      str(images[0].shape))

    locations = np.zeros((256, 2, 3), dtype=np.uint16)
    # STEP 3: For each channel:
    for channel in xrange(num_channels):
        for cur_intensity in xrange(num_points):
            # Choose middle image for YX locations.
            mid = np.round(num_images / 2)
            # STEP 3a: Choose random pixels for each intensity value.
            y_locs, x_locs = getYXLocations(images[mid][:,:,channel],
                                            cur_intensity)
            if len(y_locs) < 1:
                # This is okay, finding every single intensity is not
                # necessary and probably not available in some images.
                logging.info("Pixel intensity: " + str(cur_intensity) + 
                             " not found.")
            else:
                # Random y, x location.
                random_idx = random.randint(0, len(y_locs) - 1)

                # Pick a random current location for that intensity.
                locations[cur_intensity, :, channel] = y_locs[random_idx], \
                                                       x_locs[random_idx]

    # Pixel values at pixel intensity i, image number j, channel k
    intensity_values = np.zeros((num_points, num_images, num_channels),
                                dtype=np.uint8)
    for image_idx in xrange(num_images):
        for channel in xrange(num_channels):
            intensity_values[:, image_idx, channel] = \
                images[image_idx][locations[:, 0, channel],
                                  locations[:, 1, channel],
                                  channel]

    # Compute Response Curves
    response_curve = np.zeros((256, num_channels), dtype=np.float64)

    for channel in xrange(num_channels):
        response_curve[:, channel] = \
            computeResponseCurve(intensity_values[:, :, channel],
                                 log_exposure_times,
                                 smoothing_lambda,
                                 linearWeight)

    # Compute Image Radiance Map
    # This maps a specific pixel value (from 0->255 to its new radiance value).
    img_rad_map = np.zeros((image_size[0], image_size[1], num_channels),
                           dtype=np.float64)

    for row_idx in xrange(image_size[0]):
        for col_idx in xrange(image_size[1]):
            for channel in xrange(num_channels):
                pixel_vals = np.uint8([images[j][row_idx, col_idx, channel] \
                                      for j in xrange(num_images)])
                weights = np.float64([linearWeight(val) \
                                     for val in pixel_vals])
                sum_weights = np.sum(weights)
                img_rad_map[row_idx, col_idx, channel] = np.sum(weights * \
                    (response_curve[pixel_vals, channel] - log_exposure_times))\
                    / np.sum(weights) if sum_weights > 0.0 else 1.0

    hdr_image = np.zeros((image_size[0], image_size[1], num_channels),
                                  dtype=np.uint8)

    for channel in xrange(num_channels):
        hdr_image[:, :, channel] = \
            np.uint8(normalizeImage(img_rad_map[:, :, channel]))

    return hdr_image

# Test code to run the function.
# image_dir = "input"
# output_dir = "output"
# exposure_times = np.float64([1/160.0, 1/125.0, 1/80.0, 1/60.0, 1/40.0, 1/15.0])
# log_exposure_times = np.log(exposure_times)

# np.random.seed()
# hdr = computeHDR(image_dir, log_exposure_times, resize = True)
# cv2.imwrite(output_dir + "/hdr.jpg", hdr)
