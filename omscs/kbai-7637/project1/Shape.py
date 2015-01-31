def getShape(shape, initial_angle, final_angle):
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

    def __init__(self, initial_angle, final_angle):
        self.initial_angle = initial_angle
        self.final_angle = final_angle

    def isVerticallyReflected(self):
        return self.getRotationAngle() == 0

    def isHorizontallyReflected(self):
        return self.getRotationAngle() % 180 == 0

    def getRotationAngle(self):
        return abs(self.final_angle - self.initial_angle) % 360


class Arrow(Shape):
    pass


class Circle(Shape):
    pass

class Triangle(Shape):
    pass

class Plus(Shape):
    pass

class Rectangle(Shape):
    pass

class HalfArrow(Shape):
    pass

class PacMan(Shape):
    pass


