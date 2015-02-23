from weights import Weights
import Shape
def getAttributeTransformation(key, initial_value, final_value, shape):
    if key == 'fill':
        return FillTransformation(key, initial_value, final_value)
    elif key == 'angle':
        if initial_value == None:
            initial_value = 0
        if final_value == None:
            final_value = 0
        return OrientationTransformation(key, int(initial_value), int(final_value), shape)
    elif key == 'above' or key == 'inside' or key == 'left-of' or key == 'overlaps':
        return LocationTransformation(key, initial_value, final_value)
    return AttributeTransformation(key, initial_value, final_value)

class AttributeTransformation(object):
    def __init__(self, key, initial_value, final_value):
        self.key = key
        self.initial_value = initial_value
        self.final_value = final_value
        self.weight = Weights.get(self.key, 1)

    def __eq__(self, other):
        return self.key == other.key and self.initial_value == other.initial_value and self.final_value == other.final_value

    def __hash__(self):
        return hash((self.key, self.initial_value, self.final_value))

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "%s: (%s, %s)" %(self.key, self.initial_value, self.final_value)

    def getAsSet(self, value):
        valueList = []
        if value and ',' in value:
            valueList = value.split(',')
        else:
            valueList = [value]
        return set(valueList)

    def getWeight(self):
        return self.weight

class FillTransformation(AttributeTransformation):
    
    def __init__(self, key, initial_value, final_value):
        super(FillTransformation, self).__init__(key, initial_value, final_value)
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

class OrientationTransformation(AttributeTransformation):

    def __init__(self, key, initial_value, final_value, shape):
        super(OrientationTransformation, self).__init__(key, initial_value, final_value)
        self.shape = Shape.getShape(shape, initial_value, final_value)

    def __eq__(self, other):
        bothVerticallyReflected = (self.shape.isVerticallyReflected() and other.shape.isVerticallyReflected())
        bothHorizontallyReflected = (self.shape.isHorizontallyReflected() and other.shape.isHorizontallyReflected())
        sameRotationAngle = (other.shape.getEquivalentRotationAngle(self.shape.getRotationAngle()) == self.shape.getEquivalentRotationAngle(other.shape.getRotationAngle()))
        #print other.shape.getEquivalentRotationAngle(self.shape.getRotationAngle()), self.shape.getEquivalentRotationAngle(other.shape.getRotationAngle())
        #print bothVerticallyReflected, bothHorizontallyReflected, sameRotationAngle
        return bothVerticallyReflected or bothHorizontallyReflected or sameRotationAngle

    def getWeight(self):
        if self.shape.isVerticallyReflected() or self.shape.isHorizontallyReflected():
            return 1
        else:
            return 3

class LocationTransformation(AttributeTransformation):
    def __eq__(self, other):
        return True
