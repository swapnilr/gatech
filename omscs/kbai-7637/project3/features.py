import numpy as np
from skimage.measure import structural_similarity as ssim
from scipy import signal

class Feature(object):
    
    def __init__(self, image1, image2, image3, image4):
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.image4 = image4

class sumFeature(Feature):

    def value(self):
        return abs((self.image2.sum() - self.image1.sum()) - (self.image4.sum() - self.image3.sum()))

class trapzFeature(Feature):

    def value(self):
        return abs(np.trapz(np.trapz(self.image2) - np.trapz(self.image1) - (np.trapz(self.image4) - np.trapz(self.image3))))

class ssdFeature(Feature):

    def value(self):
        return abs(np.sum((self.image2-self.image1)**2) - (np.sum((self.image4-self.image3)**2)))

class diffFeature(Feature):

    def value(self):
        return abs((self.image2 - self.image1).sum() - (self.image4 - self.image3).sum())

class mulFeature(Feature):

    def value(self):
        return abs(((self.image2 * self.image1) - (self.image4 * self.image3)).sum())

class ssimFeature(Feature):

    def __init__(self, image1, image2, image3, image4):
        self.image1 = image1.astype(np.uint8)
        self.image2 = image2.astype(np.uint8)
        self.image3 = image3.astype(np.uint8)
        self.image4 = image4.astype(np.uint8)

    def value(self):
        #print self.image2.shape, self.image1.shape, self.image4.shape, self.image3.shape
        return abs(ssim(self.image2, self.image1) - ssim(self.image4, self.image3))

class corrFeature(Feature):

    def __init__(self, image1, image2, image3, image4, corr):
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.image4 = image4
        self.corr = corr

    def value(self):
        return abs((self.corr - signal.fftconvolve(self.image4, self.image3)).sum())


