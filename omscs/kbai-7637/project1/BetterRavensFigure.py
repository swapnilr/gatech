from BetterRavensObject import BetterRavensObject

class BetterRavensFigure():
    def __init__(self, RF):
        self.RF = RF
        self.objects = {}
        for obj in RF.getObjects():
            self.objects[obj.getName()] = BetterRavensObjects(obj)

    def getObject(self, name):
        return self.objects[name]

    def getName(self):
        return self.RF.getName()
