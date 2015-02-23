import AttributeTransformation

class ObjectTransformation():

    def __init__(self, sourceBRO, goalBRO):
        self.source = sourceBRO
        self.goal = goalBRO
        self.transformations = {}
        for key, initial_value in self.source:
            final_value = self.goal.get(key, None)
            if initial_value != final_value:
                self.transformations[key] = AttributeTransformation.getAttributeTransformation(key, initial_value, final_value, shape=self.source["shape"])
        for key, final_value in self.goal:
            if key not in self.source:
                self.transformations[key] = AttributeTransformation.getAttributeTransformation(key, None, final_value, shape=self.goal["shape"])
        self.transformationTuples = []
        for key, value in self.transformations.iteritems():
            self.transformationTuples.append((key, value))
        self.transformationTuples = tuple(self.transformationTuples)

    def __str__(self):
        return "Source %s\nGoal %s\nTransformations %s\n" % (self.source, self.goal, self.transformations)

    def __hash__(self):
        return hash(self.transformationTuples)

    def __eq__(self, other):
        return self.getTransformations() == other.getTransformations()

    def __ne__(self, other):
        return not self == other

    def getTransformations(self):
        return self.transformations

    def getWeight(self):
        weight =  sum(map(lambda x: x.getWeight(), self.transformations.values())) 
        if self.source.RO == None:
            weight += 10
        if self.goal.RO == None:
            weight += 10
        return weight
