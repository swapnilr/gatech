def getShape(shape, initial_angle, final_angle, flips=(False, False)):
    #TODO: Use flips
    if shape == 'arrow':
        return Arrow(initial_angle, final_angle)
    elif shape == 'circle':
        return Circle(initial_angle, final_angle)
    elif shape == 'triangle':
        return Triangle(initial_angle, final_angle)
    elif shape == 'plus':
        return Plus(initial_angle, final_angle)
    elif shape == 'rectangle':
        return Rectangle(initial_angle, final_angle)
    elif shape == 'half-arrow':
        return HalfArrow(initial_angle, final_angle)
    elif shape == 'Pac-man':
        return PacMan(initial_angle, final_angle)
    else:
        return Shape(initial_angle, final_angle)

class Shape(object):

    def __init__(self, initial_angle, final_angle, complete_rotation=360, half_rotation=180):
        self.initial_angle = initial_angle
        self.final_angle = final_angle
        self.completeRotation = complete_rotation
        self.halfRotation = half_rotation

    def isVerticallyReflected(self):
        return self.getRotationAngle() == 0

    def isHorizontallyReflected(self):
        return self.getRotationAngle() % self.halfRotation == 0

    def getRotationAngle(self):
        return abs(self.final_angle - self.initial_angle) % self.completeRotation

    def getEquivalentRotationAngle(self, angle):
        return angle % self.completeRotation

class Arrow(Shape):
    
    def isVerticallyRelfected(self):
        return self.getRotationAngle() % self.halfRotation == 0

    def isHorizontallyReflected(self):
        return self.getRotationAngle() == 0


class Circle(Shape):
   
    def __init__(self, initial_angle, final_angle, complete_rotation=1, half_rotation=1):
        super(Circle, self).__init__(initial_angle, final_angle, complete_rotation, half_rotation)


class Triangle(Shape):
    pass

class Plus(Shape):

    def __init__(self, initial_angle, final_angle, complete_rotation=90, half_rotation=90):
        super(Plus, self).__init__(initial_angle, final_angle, complete_rotation, half_rotation)

class Rectangle(Shape):

    def __init__(self, initial_angle, final_angle, complete_rotation=180, half_rotation=180):
        super(Rectangle, self).__init__(initial_angle, final_angle, complete_rotation, half_rotation)

class HalfArrow(Shape):

    def __init__(self, initial_angle, final_angle, complete_rotation=360, half_rotation=360):
        super(HalfArrow, self).__init__(initial_angle, final_angle, complete_rotation, half_rotation)

class PacMan(Shape):
    #pass 
    #def isVerticallyRelfected(self):
    #    return self.getRotationAngle() % self.halfRotation == 0

    def isHorizontallyReflected(self):
        return self.getRotationAngle() % self.halfRotation == 0 and not self.isVerticallyReflected()


