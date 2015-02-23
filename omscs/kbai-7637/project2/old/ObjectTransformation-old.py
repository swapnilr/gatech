from BetterRavensObject import BetterRavensObject
import util
import Shape

# Object Transformation is of 2 types: Relational and structural
class ObjectTransformation():
    
    def __init__(self, objectMap, parent=None, transform=True, try_repeats=False):
        self.object0 = BetterRavensObject(objectMap[0])
        self.object1 = BetterRavensObject(objectMap[1])
        self.parent = parent
        self.transform = transform
        if self.transform:
            self.transformations = {}
            for key, value in self.object0:
                if key in self.object1:
                    transformation = self.object1[key]
                    if key == 'angle':
                        o0flip = False
                        o1flip = False
                        if 'vertical-flip' in self.object0 and self.object0['vertical-flip'] == 'yes':
                            o0flip = True
                        if 'vertical-flip' in self.object1 and self.object1['vertical-flip'] == 'yes':
                            o1flip = True
                        self.transformations['orientation'] = OrientationTransformation(key, int(value), int(transformation), shape=self.object0['shape'], flips=(o0flip, o1flip))
                    elif key == 'vertical-flip':
                        pass
                    elif (key == 'above' or key == 'inside' or key == 'left-of' or key == 'overlaps') and (try_repeats or value != transformation):
                        self.transformations[key] = LocationTransformation(key, value, transformation, parent)
                    elif value != transformation: # Add special case for orientation
                        #if key == 'above' or key == 'inside' or key == 'left-of' or key == 'overlaps':
                        #    self.transformations[key] = LocationTransformation(key, value, transformation, parent)
                        #else:#if value != transformation:
                        self.transformations[key] = self.getTransformation(key, value, transformation)
                else:
                    if key == 'above' or key == 'inside' or key == 'left-of' or key == 'overlaps':
                        self.transformations[key] = LocationTransformation(key, value, None, parent)
                    else:
                        self.transformations[key] = self.getTransformation(key, value, None)
            for key, value in self.object1:
                if key not in self.object0:
                    if key == 'above' or key == 'inside' or key == 'left-of' or key == 'overlaps':
                        self.transformations[key] = LocationTransformation(key, None, value, parent)
                    else:
                        self.transformations[key] = self.getTransformation(key, None, value)

    
    def getTransformation(self, key, initial_value, final_value):
        if key == 'fill':
            return FillTransformation(key, initial_value, final_value)
        else:
            return AttributeTransformation(key, initial_value, final_value)

    def finalize(self, combination, other_ftf):
        for key in self.transformations.keys():
            #print key, type(self.transformations[key])
            self.transformations[key].finalize(combination, other_ftf)

    def __str__(self):
        string = "Object 1 - %s\nObject 2 - %s" % (
                str(self.getObject(0)), str(self.getObject(1)))
        if self.transform:
            string = "%s\nTransformations - {" % string
            for key, value in self.getTransformations().iteritems():
                string = "%s %s: %s," %(string, str(key), str(value))
            string = "%s}" % string
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

    def getWeight(self):
        return sum(map(lambda x: x.getWeight(), self.transformations.values()))

