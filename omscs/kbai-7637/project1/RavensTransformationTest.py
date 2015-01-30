import unittest
from RavensObject import RavensObject
from RavensAttribute import RavensAttribute
from RavensTransformation import ObjectTransformation
from RavensTransformation import FigureTransformation

class ObjectTransformationTest(unittest.TestCase):
    
    def setUp(self):
        self.ZRO = RavensObject('Z')
        attr1 = RavensAttribute('shape', 'circle')
        attr2 = RavensAttribute('size', 'large')
        self.ZRO.attributes = [attr1, attr2]
        self.YRO = RavensObject('Y')
        attr1 = RavensAttribute('shape', 'square')
        attr2 = RavensAttribute('size', 'small')
        self.YRO.attributes = [attr1, attr2]
        self.otf = ObjectTransformation((self.ZRO, self.YRO))

    def testBasic(self):
        assert(self.otf.getObject(0))
        assert(self.otf.getObject(1))
        self.assertRaises(IndexError, self.otf.getObject, 2)

    def testGetTransformations(self):
        transformations = self.otf.getTransformations()
        assert('shape' in transformations)
        assert(transformations['shape'][0] == 'circle')
        assert(transformations['shape'][1] == 'square')
        assert('size' in transformations)
        assert(transformations['size'][0] == 'large')
        assert(transformations['size'][1] == 'small')

    def testEquals(self):
        ARO = RavensObject('A')
        attr1 = RavensAttribute('shape', 'circle')
        attr2 = RavensAttribute('size', 'large')
        ARO.attributes = [attr2, attr1]
        BRO = RavensObject('B')
        attr1 = RavensAttribute('shape', 'square')
        attr2 = RavensAttribute('size', 'small')
        BRO.attributes = [attr1, attr2]
        test_otf = ObjectTransformation((ARO, BRO))
        assert(self.otf == test_otf)
        test_otf = ObjectTransformation((BRO, ARO))
        assert(self.otf != test_otf)

class FigureTranformationTest(unittest.TestCase):
    
    def setUp(self):
        self.ZRO = RavensObject('Z')
        attr1 = RavensAttribute('shape', 'circle')
        attr2 = RavensAttribute('size', 'large')
        self.ZRO.attributes = [attr1, attr2]
        self.YRO = RavensObject('Y')
        attr1 = RavensAttribute('shape', 'circle')
        attr2 = RavensAttribute('size', 'small')
        self.YRO.attributes = [attr1, attr2]
        self.otf = ObjectTransformation((self.ZRO, self.YRO))
        self.ftf = FigureTransformation()
        self.ftf.add('Z', self.otf)


    def testSingleObjectComparison(self):
        ARO = RavensObject('A')
        attr1 = RavensAttribute('shape', 'circle')
        attr2 = RavensAttribute('size', 'large')
        ARO.attributes = [attr1, attr2]
        BRO = RavensObject('B')            
        attr1 = RavensAttribute('shape', 'circle')
        attr2 = RavensAttribute('size', 'small')        
        BRO.attributes = [attr2, attr1]
        test_otf = ObjectTransformation((ARO, BRO))
        test_ftf = FigureTransformation()
        test_ftf.add('A', test_otf)
        assert(self.ftf == test_ftf)

    def singleObjectFigureTest(self):
        pass

    def doubleObjectFigureTest(self):
        pass

    def tripleObjectFigureTest(self):
        pass

if __name__ == '__main__':
    unittest.main()

