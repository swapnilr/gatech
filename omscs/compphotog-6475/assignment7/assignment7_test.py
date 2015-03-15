import sys
import os
import numpy as np
import cv2

import assignment7

def test_findMatchesBetweenImages():
  """This script will perform a unit test on the matching function.
  """
  # Hard code output matches.
  image_1 = cv2.imread("images/source/sample/image_1.jpg")
  image_2 = cv2.imread("images/source/sample/image_2.jpg")

  if __name__ == "__main__":
    print 'Evaluating findMatchesBetweenImages.'

    image_1_kp, image_2_kp, matches = \
        assignment7.findMatchesBetweenImages(image_1, image_2)

    if not type(image_1_kp) == list:
      print "Error - image_1_kp has type {}. Expected type is {}. ".format(
          type(image_1_kp), list)
      return False

    if len(image_1_kp) > 0 and \
      not type(image_1_kp[0]) == type(cv2.KeyPoint()):
      print ("Error - The items in image_1_kp have type {}. " + \
            "Expected type is {}.").format(type(image_1_kp[0]),
                                           type(cv2.KeyPoint()))
      return False

    if not type(image_2_kp) == list:
      print "Error - image_2_kp has type {}. Expected type is {}. ".format(
          type(image_2_kp), list)
      return False

    if len(image_2_kp) > 0 and not type(image_2_kp[0]) == type(cv2.KeyPoint()):
      print ("Error - The items in image_2_kp have type {}. " + \
            "Expected type is {}.").format(type(image_2_kp[0]),
                                           type(cv2.KeyPoint()))
      return False

    if not type(matches) == list:
      print "Error - matches has type {}. Expected type is {}. ".format(
            type(matches), list)
      return False

    if len(matches) > 0 and not type(matches[0]) == type(cv2.DMatch()):
      print ("Error - The items in matches have type {}. " + \
            "Expected type is {}.").format(type(matches[0]), type(cv2.DMatch()))
      return False

    if len(matches) != 10:
      print ("Error - The length of matches is {}. " + \
            "The expected length is {}.").format(len(matches), 10)
      return False
    return True


if __name__ == "__main__":
  print 'Performing unit test.'
  if not test_findMatchesBetweenImages():
    print 'findMatchesBetweenImages function failed. Halting testing.'
    sys.exit()

  print 'Unit test passed.'

  
  sourcefolder = os.path.abspath(os.path.join(os.curdir, 'images', 'source'))
  outfolder = os.path.abspath(os.path.join(os.curdir, 'images', 'output'))

  print 'Image source folder: {}'.format(sourcefolder)
  print 'Image output folder: {}'.format(outfolder)

  print 'Searching for folders with images in {}.'.format(sourcefolder)

  # Extensions recognized by opencv
  exts = ['.bmp', '.pbm', '.pgm', '.ppm', '.sr', '.ras', '.jpeg', '.jpg', 
    '.jpe', '.jp2', '.tiff', '.tif', '.png']

  # For every image in the source directory
  for dirname, dirnames, filenames in os.walk(sourcefolder):
    setname = os.path.split(dirname)[1]

    image_1 = None
    image_1_gs = None
    image_2 = None
    image_2_gs = None

    for filename in filenames:
      name, ext = os.path.splitext(filename)
      if ext in exts:
        if '_1' in name:
          print "Reading image_1 {} from {}.".format(filename, dirname)
          image_1 = cv2.imread(os.path.join(dirname, filename))
          image_1_gs = cv2.imread(os.path.join(dirname, filename), 0)

        elif '_2' in name:
          print "Reading image_2 {} from {}.".format(filename, dirname)
          image_2 = cv2.imread(os.path.join(dirname, filename))
          image_2_gs = cv2.imread(os.path.join(dirname, filename), 0)

    if image_1 == None or image_2 == None:
      print "Did not find image_1 / image_2 images in folder: " + dirname
      continue
    else:
      print "Found images in folder {}, processing them.".format(dirname)

    print "Computing matches."
    image_1_kp, image_2_kp, matches = assignment7.findMatchesBetweenImages(
        image_1, image_2)

    print "Visualizing matches."
    output = assignment7.drawMatches(image_1, image_1_kp, image_2, image_2_kp,
                                     matches)

    output_folder = os.path.join(outfolder, setname)
    print "Writing images to folder {}".format(output_folder)

    if not os.path.exists(output_folder):
      os.makedirs(output_folder)

    cv2.imwrite(os.path.join(output_folder, "matches.jpg"), output)