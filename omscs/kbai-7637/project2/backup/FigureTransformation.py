class FigureTransformation():
    
    def __init__(self, otfList):
        self.otfList = otfList

    def __str__(self):
        s = "["
        for elem in self.otfList:
            s += "%s " % str(elem)
        s += "]"
        return s

    def getWeight(self):
        return sum(map(lambda x: x.getWeight(), self.otfList)) 

    def __iter__(self):
        return iter(self.otfList)
