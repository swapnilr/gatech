import numpy as np
import scipy as sp
import scipy.signal

def generatingKernel(parameter):
  """ Return a 5x5 generating kernel based on an input parameter.
  Note: This function is provided for you, do not change it.
  Args:
    parameter (float): Range of value: [0, 1].
  Returns:
    numpy.ndarray: A 5x5 kernel.
  """
  kernel = np.array([0.25 - parameter / 2.0, 0.25, parameter,
                     0.25, 0.25 - parameter /2.0])
  return np.outer(kernel, kernel)

def reduce(image):
  """ Convolve the input image with a generating kernel of parameter of 0.4 and
  then reduce its width and height by two.
  Please consult the lectures and readme for a more in-depth discussion of how
  to tackle the reduce function.
  You can use any / all functions to convolve and reduce the image, although
  the lectures have recommended methods that we advise since there are a lot
  of pieces to this assignment that need to work 'just right'.
  Args:
    image (numpy.ndarray): a grayscale image of shape (r, c)
  Returns:
    output (numpy.ndarray): an image of shape (ceil(r/2), ceil(c/2))
      For instance, if the input is 5x7, the output will be 3x4.
  """
  # WRITE YOUR CODE HERE.
  kernel = generatingKernel(0.4)
  rows, columns = image.shape
  convolved = scipy.signal.convolve2d(image, kernel, 'same')
  rrows = np.ceil(rows/2.0).astype(np.int32)
  rcolumns = np.ceil(columns/2.0).astype(np.int32)
  #print rows, rows/2.0, np.ceil(rows/2.0), rrows
  reduced = np.zeros((rrows, rcolumns))
  #print convolved.shape
  #print image.shape
  #print reduced.shape
  for y in range(0, rows, 2):
      for x in range(0, columns, 2):
          reduced[y/2, x/2] = convolved[y,x]
  return reduced
  # END OF FUNCTION.

def expand(image):
  """ Expand the image to double the size and then convolve it with a generating
  kernel with a parameter of 0.4.
  You should upsample the image, and then convolve it with a generating kernel
  of a = 0.4.
  Finally, multiply your output image by a factor of 4 in order to scale it
  back up. If you do not do this (and I recommend you try it out without that)
  you will see that your images darken as you apply the convolution. Please
  explain why this happens in your submission PDF.
  Please consult the lectures and readme for a more in-depth discussion of how
  to tackle the expand function.
  You can use any / all functions to convolve and reduce the image, although
  the lectures have recommended methods that we advise since there are a lot
  of pieces to this assignment that need to work 'just right'.
  Args:
    image (numpy.ndarray): a grayscale image of shape (r, c)
  Returns:
    output (numpy.ndarray): an image of shape (2*r, 2*c)
  """
  # WRITE YOUR CODE HERE.
  kernel = generatingKernel(0.4)
  rows, columns = image.shape
  expanded = np.zeros((rows*2, columns*2))
  for y in range(0, rows*2, 2):
      for x in range(0, columns*2, 2):
          expanded[y,x] = 4*image[y/2, x/2]
  expanded = scipy.signal.convolve2d(expanded, kernel, 'same')
  return expanded
  # END OF FUNCTION.

def gaussPyramid(image, levels):
  """ Construct a pyramid from the image by reducing it by the number of levels
  passed in by the input.
  Note: You need to use your reduce function in this function to generate the
  output.
  Args:
    image (numpy.ndarray): A grayscale image of dimension (r,c) and dtype float.
    levels (uint8): A positive integer that specifies the number of reductions
                    you should do. So, if levels = 0, you should return a list
                    containing just the input image. If levels = 1, you should
                    do one reduction. len(output) = levels + 1
  Returns:
    output (list): A list of arrays of dtype np.float. The first element of the
                   list (output[0]) is layer 0 of the pyramid (the image
                   itself). output[1] is layer 1 of the pyramid (image reduced
                   once), etc. We have already included the original image in
                   the output array for you. The arrays are of type
                   numpy.ndarray.
  Consult the lecture and README for more details about Gaussian Pyramids.
  """
  output = [image]
  # WRITE YOUR CODE HERE.
  for i in range(levels):
      output.append(reduce(output[-1]))
  return output
  # END OF FUNCTION.

def laplPyramid(gaussPyr):
  """ Construct a laplacian pyramid from the gaussian pyramid, of height levels.
  Note: You must use your expand function in this function to generate the
  output. The Gaussian Pyramid that is passed in is the output of your
  gaussPyramid function.
  Args:
    gaussPyr (list): A Gaussian Pyramid as returned by your gaussPyramid
                     function. It is a list of numpy.ndarray items.
  Returns:
    output (list): A laplacian pyramid of the same size as gaussPyr. This
                   pyramid should be represented in the same way as guassPyr, 
                   as a list of arrays. Every element of the list now
                   corresponds to a layer of the laplacian pyramid, containing
                   the difference between two layers of the gaussian pyramid.
           output[k] = gauss_pyr[k] - expand(gauss_pyr[k + 1])
           Note: The last element of output should be identical to the last 
           layer of the input pyramid since it cannot be subtracted anymore.
  Note: Sometimes the size of the expanded image will be larger than the given
  layer. You should crop the expanded image to match in shape with the given
  layer.
  For example, if my layer is of size 5x7, reducing and expanding will result
  in an image of size 6x8. In this case, crop the expanded layer to 5x7.
  """
  output = []
  # WRITE YOUR CODE HERE.
  for i in range(len(gaussPyr) - 1):
      rows, columns = gaussPyr[i].shape
      output.append(gaussPyr[i] - expand(gaussPyr[i+1])[:rows, :columns] )
  output.append(gaussPyr[-1])
  return output
  # END OF FUNCTION.
