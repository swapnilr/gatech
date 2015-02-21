from BetterRavensObject import BetterRavensObject
import util
import Shape

WEIGHTS = {}

class AttributeTransformation(object):
    
    def __init__(self, key, initial_value, final_value):
        self.key = key
        self.initial_value = initial_value
        self.final_value = final_value

    def __eq__(self, other):
        return self.key == other.key and self.initial_value == other.initial_value and self.final_value == other.final_value

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "(%s, %s)" %(self.initial_value, self.final_value)

    def getAsSet(self, value):
        valueList = []
        if value and ',' in value:
            valueList = value.split(',')
        else:
            valueList = [value]
        return set(valueList)

    def getWeight(self):
        return WEIGHTS.get(self.key, 1)

    def finalize(self, combination, other_ftf):
        pass

class FillTransformation(AttributeTransformation):
    
    def __init__(self, key, initial_value, final_value):
        self.key = key
        self.initial_value = self.cleaned(initial_value)
        self.final_value = self.cleaned(final_value)

    def cleaned(self, value):
        valueSet = self.getAsSet(value)
        val = 0
        # Values here are a bitwise representation, where quadrant I is 1, quadrant II is 10(binary)
        # quadrant III is 100 and quadrant IV is 1000. The fill is thus a bitwise or based on which
        # quadrants are filled
        for fill in valueSet:
            if fill == 'no':
                val |= 0
            elif fill == 'yes':
                val |= 15
            elif fill == 'left-half':
                val |= 6
            elif fill == 'top-half':
                val |= 3
            elif fill == 'right-half':
                val |= 9
            elif fill == 'bottom-half':
                val |= 12
            elif fill == 'top-left':
                val |= 2
            elif fill == 'bottom-left':
                val |= 4
            elif fill == 'top-right':
                val |= 1
            elif fill == 'bottom-right':
                val |= 8
        return val

    def __eq__(self, other):
        if self.initial_value != 0:
            #TODO: Solve this
            pass
        else:
            #TODO: Can be things other than or
            return other.final_value == self.final_value | other.initial_value
        return self.key == other.key and self.initial_value == other.initial_value and self.final_value == other.final_value


class LocationTransformation(AttributeTransformation):
    
    def __init__(self, key, initial_value, final_value, parent):
        super(LocationTransformation, self).__init__(key, self.getAsSet(initial_value), self.getAsSet(final_value))
        self.parent = parent
        # On creation, scrub all names on mapped values to initial_value set. That is, if we're mapping
        # from A to B, all objects in B should be named according to A(based on the correspondence that is
        # present in this FigureTransformation
        reverse_map = {}
        for name in self.parent.getObjectNames():
            reverse_map[self.parent.getNameTranslation(name)] = name
        def func(x):
            try:
                return reverse_map[x]
            except KeyError as k:
                return x
        self.final_value = set(map(func, self.final_value))

    def finalize(self, combination, other_ftf):
        # Now replace the names in both figures based on this map. That is, when A->C map is generated,
        # all figures in C and candidate solution should be mapped to names in A based on the A->C map
        combination.update({None:None})
        reverse_map = {}
        #TODO: This is not robust to deletion. Fix
        #for name in self.parent.getObjectNames():
        #    reverse_map[self.parent.getNameTranslation(name)] = name
        #def func(x):
        #    try:
        #        return other_ftf.getNameTranslation(reverse_map[x])
        #    except KeyError as k:
        #        return x
        #final_values = set(map(func, self.final_value))
        try:
            initial_values = set(map(combination.get, self.initial_value))
            final_values = set(map(combination.get, self.final_value))
        except Exception as e:
            print self.parent.getObjectNames()
            raise
        #print "AHHHHHHHH"
        #print self.initial_value
        #print initial_values, final_values
        #print combination
        self.mapped_initial_value = initial_values
        self.mapped_final_value = final_values

    def __eq__(self, other):
        #print self.key == other.key
        #print self.mapped_initial_value == other.initial_value
        #print self.mapped_final_value, self.mapped_final_value == other.final_value
        return self.key == other.key and self.mapped_initial_value == other.initial_value and self.mapped_final_value == other.final_value

class OrientationTransformation(AttributeTransformation):
    
    def __init__(self, key, initial_value, final_value, shape, flips):
        super(OrientationTransformation, self).__init__(key, initial_value, final_value)
        self.shape = Shape.getShape(shape, initial_value, final_value, flips)

    def __eq__(self, other):
        bothVerticallyReflected = (self.shape.isVerticallyReflected() and other.shape.isVerticallyReflected())
        bothHorizontallyReflected = (self.shape.isHorizontallyReflected() and other.shape.isHorizontallyReflected())
        sameRotationAngle = (other.shape.getEquivalentRotationAngle(self.shape.getRotationAngle()) == self.shape.getEquivalentRotationAngle(other.shape.getRotationAngle()))
        #print other.shape.getEquivalentRotationAngle(self.shape.getRotationAngle()), self.shape.getEquivalentRotationAngle(other.shape.getRotationAngle())
        #print bothVerticallyReflected, bothHorizontallyReflected, sameRotationAngle
        return bothVerticallyReflected or bothHorizontallyReflected or sameRotationAngle


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

class FigureTransformation():

    def __init__(self):
        self.objTransMap = {}
        self.reverseNameMap = {}

    def add(self, obj, transformation):
        assert(isinstance(obj, str))
        assert(isinstance(transformation, ObjectTransformation))
        self.objTransMap[obj] = transformation
        #self.reverseNameMap[transformation.getObject(1)] = obj

    def getAName(self, BName):
        return self.reverseNameMap[BName]

    def get(self, obj):
        return self.objTransMap[obj]

    def getObjectNames(self):
        return self.objTransMap.keys()

    def getNameTranslation(self, name):
        return self.get(name).getObject(1).getName()

    def __iter__(self):
        return self.objTransMap.iteritems()

    def __str__(self):
        string = "%s\nFigure: \n" % self.getTransformation()
        for name, otf in self:
            string = "%s\n%s" %(string, otf)
        return string

    def __eq__(self, other):
        for combination in util.generic_pairs(self.getObjectNames(), other.getObjectNames()):
            match = True
            self.finalize(dict(combination), other)
           # print "Trying Combination " + str(combination)
            for pair in combination:
                if self.get(pair[0]) != other.get(pair[1]):
                    #print "These 2 don't match: "
                    #print "---------------------"
                    #print self.get(pair[0])
                    #print "---------------------"
                    #print other.get(pair[1])
                    match = False
                    break
            if match:
                #for pair in combination:
                #    print "O1----%s-----\nO2----%s----" % (self.get(pair[0]), other.get(pair[1]))
                #    self.get(pair[0]) == other.get(pair[1])
                #print dict(combination)
                return match
        return False

    def __ne__(self, other):
        return not self == other

    def getTransformation(self):
        d = {}
        for key in self.getObjectNames():
            d[key] = self.getNameTranslation(key)
        return d

    def finalize(self, combination, other):
        for transformation in self.objTransMap.values():
            transformation.finalize(combination, other)
    
    def getWeight(self):
        return sum(map(lambda x: x.getWeight(), self.objTransMap.values()))
