from BetterRavensObject import BetterRavensObject
import exception

class RavensTransformation():
    
    def __init__(self, objectMap):
        self.object0 = BetterRavensObject(objectMap[0])
        self.object1 = BetterRavensObject(objectMap[1])
        self.transformations = {}
        for key, value in self.object0:
            #transformation = value
            if key in self.object1:
                transformation = self.object1[key]
                self.transformations[key] = (value, transformation)

    def getTransformations(self):
        return self.transformations

    def getObject(index=0):
        if index == 0:
            return self.object1
        elif index == 1:
            return self.object2
        else:
            raise exception.IndexError("Only 2 objects present")
