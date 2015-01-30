from BetterRavensObject import BetterRavensObject

class ObjectTransformation():
    
    def __init__(self, objectMap, transform=True):
        self.object0 = BetterRavensObject(objectMap[0])
        self.object1 = BetterRavensObject(objectMap[1])
        self.transform = transform
        if self.transform:
            self.transformations = {}
            for key, value in self.object0:
                #transformation = value
                if key in self.object1:
                    transformation = self.object1[key]
                    if value != transformation:
                        self.transformations[key] = (value, transformation)

    def __str__(self):
        string = "Object 1 - %s\nObject 2 - %s" % (
                str(self.getObject(0)), str(self.getObject(1)))
        if self.transform:
            string = "%s\nTransformations%s" % (string, str(self.getTransformations()))
        return string


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
            raise exception.IndexError("Only 2 objects present")

class FigureTransformation():

    def __init__(self):
        self.objTransMap = {}

    def add(self, obj, transformation):
        assert(isinstance(obj, str))
        assert(isinstance(transformation, ObjectTransformation))
        self.objTransMap[obj] = transformation

    def get(self, obj):
        return self.objTransMap[obj]

    def __iter__(self):
        return self.objTransMap.iteritems()

    def __str__(self):
        string = "Figure %s" % (obj)
        for name, otf in self:
            string = "%s\n%s" %(string, otf)
        return string

