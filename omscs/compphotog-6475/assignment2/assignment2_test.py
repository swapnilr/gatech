import cv2
import unittest

from assignment2 import averagePixel
from assignment2 import averageTwoImages
from assignment2 import convertToBlackAndWhite
from assignment2 import flipHorizontal
from assignment2 import numberOfPixels

class Assignment2Test(unittest.TestCase):
    def setUp(self):
        self.testImage = cv2.imread("test_image.jpg", cv2.IMREAD_GRAYSCALE)
        self.testImage2 = cv2.imread("test_image_2.jpg",
                                        cv2.IMREAD_GRAYSCALE)
        if self.testImage == None:
            raise IOError("Error, image test_image.jpg not found.")
        if self.testImage2 == None:
            raise IOError("Error, image test_image_2.jpg not found.")

    def test_numberOfPixels(self):
        self.assertEqual(type(numberOfPixels(self.testImage)), type(0))
        print "\n\nSUCCESS: numberofPixels returns the correct output type.\n"

    def test_averagePixel(self):
        self.assertEqual(type(averagePixel(self.testImage)), type(0))
        print "\n\nSUCCESS: averagePixel returns the correct output type.\n"
    
    def test_convertToBlackAndWhite(self):
        self.assertEqual(type(convertToBlackAndWhite(self.testImage)),
                         type(self.testImage))
        print "\n\nSUCCESS: convertToBlackAndWhite returns the correct output type.\n"

    def test_flipHorizontal(self):
        self.assertEqual(type(flipHorizontal(self.testImage)),
                         type(self.testImage))
        print "\n\nSUCCESS: flipHorizontal returns the correct output type.\n"

    def test_averageTwoImages(self):
        self.assertEqual(type(averageTwoImages(self.testImage,
                                               self.testImage2)),
                         type(self.testImage))
        print "\n\nSUCCESS: averageTwoImages returns the correct output type.\n"

if __name__ == '__main__':
	unittest.main()
