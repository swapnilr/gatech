import numpy as np

class Feature(object):
    
    def __init__(self, image1, image2, image3, image4):
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.image4 = image4


class sumFeature(Feature):

    def value(self):
        return abs((self.image2.sum() - self.image1.sum()) - (self.image4.sum() - self.image3.sum()))
