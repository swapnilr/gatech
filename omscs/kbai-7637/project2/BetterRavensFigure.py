from BetterRavensObject import BetterRavensObject

class BetterRavensFigure():
    def __init__(self, RF):
        self.RF = RF
        self.objects = {}
        for obj in RF.getObjects():
            self.objects[obj.getName()] = BetterRavensObject(obj)
    
    def __getitem__(self, item):
        return self.objects[item]

    def __setitem__(self, item, value):
        self.objects[item] = value

    def __contains__(self, item):
        return item in self.objects

    def __iter__(self):
        return self.getObjects().iteritems()

    def getObject(self, name):
        return self.objects[name]

    def getName(self):
        return self.RF.getName()

    def getObjects(self):
        return self.objects
