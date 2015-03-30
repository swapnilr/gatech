import numpy as np
import scipy as sp
import scipy.signal

def generatingKernel(parameter):
  kernel = np.array([0.25 - parameter / 2.0, 0.25, parameter,
                     0.25, 0.25 - parameter /2.0])
  return np.outer(kernel, kernel)

def reduce(image):
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
  output = [image]
  # WRITE YOUR CODE HERE.
  for i in range(levels):
      output.append(reduce(output[-1]))
  return output
  # END OF FUNCTION.

def laplPyramid(gaussPyr):
  output = []
  # WRITE YOUR CODE HERE.
  for i in range(len(gaussPyr) - 1):
      rows, columns = gaussPyr[i].shape
      output.append(gaussPyr[i] - expand(gaussPyr[i+1])[:rows, :columns] )
  output.append(gaussPyr[-1])
  return output
  # END OF FUNCTION.
