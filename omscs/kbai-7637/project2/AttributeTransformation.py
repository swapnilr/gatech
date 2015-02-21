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

