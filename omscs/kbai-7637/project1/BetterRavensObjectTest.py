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

    def testBasic(self):
        bro = BetterRavensObject(self.RO)
        assert(len(bro.getAttributes()) == 2)

    def testContains(self):
        bro = BetterRavensObject(self.RO)
        assert('shape' in bro)

    def testGet(self):
        bro = BetterRavensObject(self.RO)
        assert(bro['shape'] == 'circle')

    def testSet(self):
        bro = BetterRavensObject(self.RO)
        bro['shape'] = 'square'
        assert(bro['shape'] == 'square')

    def testName(self):
        bro = BetterRavensObject(self.RO)
        assert(bro.getName() == 'Z')

    def testEquals(self):
        bro = BetterRavensObject(self.RO)
        otherRO = RavensObject('Y')
        attr1 = RavensAttribute('size', 'large')
        attr2 = RavensAttribute('shape', 'square')
        otherRO.attributes = [attr1, attr2]
        otherBro = BetterRavensObject(otherRO)
        assert(bro != otherBro)
        bro['shape'] = 'square'
        assert(bro == otherBro)

    def testIter(self):
        bro = BetterRavensObject(self.RO)
        for key, value in bro:
            assert(bro[key] == value)

if __name__ == '__main__':
    unittest.main()
