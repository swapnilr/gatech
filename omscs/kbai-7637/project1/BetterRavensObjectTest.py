import unittest
from RavensObject import RavensObject
from RavensAttribute import RavensAttribute
from BetterRavensObject import BetterRavensObject

class TestBetterRavensObject(unittest.TestCase):
    
    def setUp(self):
        self.RO = RavensObject('Z')
        attr1 = RavensAttribute('shape', 'circle')
        attr2 = RavensAttribute('size', 'large')
        self.RO.attributes = [attr1, attr2]
        self.bro = BetterRavensObject(self.RO)

    def testBasic(self):
        assert(len(self.bro.getAttributes()) == 2)

    def testContains(self):
        assert('shape' in self.bro)

    def testGet(self):
        assert(self.bro['shape'] == 'circle')

    def testSet(self):
        self.bro['shape'] = 'square'
        assert(self.bro['shape'] == 'square')

    def testName(self):
        assert(self.bro.getName() == 'Z')

    def testEquals(self):
        otherRO = RavensObject('Y')
        attr1 = RavensAttribute('size', 'large')
        attr2 = RavensAttribute('shape', 'square')
        otherRO.attributes = [attr1, attr2]
        otherBro = BetterRavensObject(otherRO)
        assert(self.bro != otherBro)
        self.bro['shape'] = 'square'
        assert(self.bro == otherBro)

    def testIter(self):
        for key, value in self.bro:
            assert(self.bro[key] == value)

if __name__ == '__main__':
    unittest.main()
