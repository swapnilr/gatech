import numpy as np
import scipy as sp
import cv2

# TODO(swapnilr): Move to common
RED = 0
GREEN = 1
BLUE = 2
def getImageName(pset, qn, part, counter):
  return 'ps%d-%d-%s-%d.png' % (pset, qn, part, counter)

def getName(qn, part, counter):
  return getImageName(pset=0, qn=qn, part=part, counter=counter)

def getImage(index=0):
  if index==0:
    return cv2.imread('cropped_house.png')
  elif index==1:
    return cv2.imread('cropped_boat.png')
  else:
    raise IndexError('Index out of bounds')

def getChannel(image, channel_index=RED, copy=False):
  channel = image[:,:,channel_index]
  if copy:
    channel = channel.copy()
  return channel

def writeImage(filename, img):
  return cv2.imwrite('output/%s' % filename, img)

def part1():
  writeImage(getName(1,'a',1), getImage(0))
  writeImage(getName(1, 'a', 2), getImage(1))

def part2a():
  image1 = getImage(0)
  image1_red = getChannel(image1, RED, True)
  image1_blue = getChannel(image1, BLUE, True)
  image1[:,:,RED] = image1_blue
  image1[:,:,BLUE] = image1_red
  writeImage(getName(2, 'a', 1), image1)

def part2b():
  writeOneChannel(channel_index=GREEN)

def writeOneChannel(channel_index=RED, part='b'):
  image1 = getImage(0)
  image1_channel = getChannel(image1, channel_index, True)
  writeImage(getName(2, part, 1), image1_channel)

def part2c():
  writeOneChannel(part='c')

def part2():
  part2a()
  part2b()
  part2c()

def part3():
  img1 = getImage()
  img2 = getImage(1)
  img1_green = getChannel(img1, GREEN)
  img2_green = getChannel(img2, GREEN)
  h,w = img1_green.shape
  h_start = (h-100)/2
  w_start = (w-100)/2
  img1_square = img1_green[h_start:h_start + 100, w_start:w_start+100]
  h,w = img2_green.shape
  h_start = (h-100)/2
  w_start = (w-100)/2
  img2_green[h_start:h_start+100, w_start:w_start+100] = img1_square
  writeImage(getName(3,'a',1) ,img2_green)

def getStats(image):
  """
    Returns the stats as a 4-tuple (min, max, mean, std dev)
  """
  return (image.min(), image.max(), image.mean(), image.std())

def printStats(stats):
  minimum, maximum, mean, std_dev = stats
  print "Statistics: Min - %d, Max %d, Mean %f, Stddev %f" %(minimum, maximum, mean, std_dev)

def part4():
  img1_green = getChannel(getImage(), GREEN)
  stats = getStats(image)
  minimum, maximum, mean, std_dev = stats
  # Part 2
  f = lambda(a): np.uint8((( float(a) - mean)/std_dev)*10 + mean)
  fv = np.vectorize(f)
  img1_mat = fv(img1_green)
  writeImage(getName(4, 'b', 1), img1_mat)
  # Part 3
  img1_shifted = np.roll(img1_green, -2, axis=1)
  writeImage(getName(4, 'c', 1), img1_shifted)
  # Part 4
  img1_sub = img1_green - img1_shifted
  writeImage(getName(4, 'd', 1), img1_sub)

def part5(channel=GREEN, part='a'):
  sigma = 0
  x = 'y'
  img1 = getImage()
  cv2.imshow("original", img1)
  while x.lower() == 'y':
    sigma += 1
    img1_noisy = img1.copy()
    img1_noisy[:,:,channel] += np.random.randn(img1.shape[0], img1.shape[1])*sigma
    cv2.imshow("noisy", img1_noisy)
    print "Sigma is %d. Add more noise? " % sigma, 
    x = raw_input()
    cv2.destroyWindow("noisy")
  writeImage(getName(5,part,1), img1_noisy)
  print "Sigma is %d" %  sigma
  noisy_blue = img1.copy()
  noisy_blue[:,:,BLUE] += np.random.randn(img1.shape[0], img1.shape[1]) * sigma
  cv2.imshow("noisy blue", noisy_blue)
  writeImage(getName(5, 'b', 1), noisy_blue)
  print "Press any key to close windows"
  raw_input()
  cv2.destroyAllWindows()

def main():
  part1()
  part2()
  part3()
  part4()
  part5()

if __name__ == '__main__':
  main()
