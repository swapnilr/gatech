class BetterRavensObject():
    def __init__(self, RO):
        self.RO = RO
        self.attributes = {}
        for attr in RO.getAttributes():
            self.attributes[attr.getName()] = attr.getValue()

    def __eq__(self, other):
        return self.attributes == other.getAttributes()

    def __getitem__(self, item):
        return self.attributes[item]

    def __setitem__(self, item, value):
        self.attributes[item] = value

    def __contains__(self, item):
        return item in self.attributes

    def getAttributes(self):
        return self.attributes

    def getName(self):
        return self.RO.getName()
