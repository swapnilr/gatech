from BetterRavensObject import BetterRavensObject
import util

class AttributeTransformation():
    
    def __init__(self, key, initial_value, final_value):
        self.key = key
        self.initial_value = initial_value
        self.final_value = final_value

    def __eq__(self, other):
        return self.key == other.key and self.initial_value == other.initial_value and self.final_value == other.final_value

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "(%s, %s)" %(initial_value, final_value)

# Object Transformation is of 2 types: Relational and structural
class ObjectTransformation():
    
    def __init__(self, objectMap, transform=True):
        self.object0 = BetterRavensObject(objectMap[0])
        self.object1 = BetterRavensObject(objectMap[1])
        self.transform = transform
        if self.transform:
            self.transformations = {}
            for key, value in self.object0:
                if key in self.object1:
                    transformation = self.object1[key]
                    if value != transformation:
                        self.transformations[key] = AttributeTransformation(key, value, transformation)
            for key, value in self.object1:
                if key not in self.object0:
                    self.transformations[key] = AttributeTransformation(key, None, value)

    def __str__(self):
        string = "Object 1 - %s\nObject 2 - %s" % (
                str(self.getObject(0)), str(self.getObject(1)))
        if self.transform:
            string = "%s\nTransformations%s" % (string, str(self.getTransformations()))
        return string

    def __eq__(self, other):
        return self.getTransformations() == other.getTransformations()

    def __ne__(self, other):
        return not self == other

    def getTransformations(self):
        if not self.transform:
            raise ValueError("Transform set to False during creation")
        return self.transformations

    def getObject(self, index=0):
        if index == 0:
            return self.object0
        elif index == 1:
            return self.object1
        else:
            raise IndexError("Only 2 objects present")

class FigureTransformation():

    def __init__(self):
        self.objTransMap = {}

    def add(self, obj, transformation):
        assert(isinstance(obj, str))
        assert(isinstance(transformation, ObjectTransformation))
        self.objTransMap[obj] = transformation

    def get(self, obj):
        return self.objTransMap[obj]

    def getObjectNames(self):
        return self.objTransMap.keys()

    def __iter__(self):
        return self.objTransMap.iteritems()

    def __str__(self):
        string = "Figure: \n"
        for name, otf in self:
            string = "%s\n%s" %(string, otf)
        return string

    def __eq__(self, other):
        for combination in util.generic_pairs(self.getObjectNames(), other.getObjectNames()):
            match = True
            for pair in combination:
                if self.get(pair[0]) != other.get(pair[1]):
                    match = False
                    break
            if match:
                return match
        return False

    def __ne__(self, other):
        return not self == other
