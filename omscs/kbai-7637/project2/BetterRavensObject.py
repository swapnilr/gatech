class BetterRavensObject():
    def __init__(self, RO, parent):
        self.RO = RO
        self.parent = parent
        self.attributes = {}
        if RO:
            for attr in RO.getAttributes():
                self.attributes[attr.getName()] = attr.getValue()

    def __eq__(self, other):
        return self.attributes == other.getAttributes()

    def __ne__(self, other):
        return not self == other

    def __getitem__(self, item):
        return self.attributes[item]

    def __setitem__(self, item, value):
        self.attributes[item] = value

    def __contains__(self, item):
        return item in self.attributes

    def __iter__(self):
        return self.getAttributes().iteritems()

    def __str__(self):
        return "%s - %s" % (str(self.getName()), str(self.getAttributes())) 

    def getAttributes(self):
        return self.attributes

    def getName(self):
        return self.RO.getName() if self.RO else None

    def getFullName(self):
        return "%s-%s" %(self.parent.getName(), self.RO.getName())
