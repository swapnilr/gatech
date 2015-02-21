#   The value is an RavensTransformation(FTFSet/OTFSet). RavensTransformation holds
#     1. For each object in source, OTF to each object in goal
#     2. A priority queue that gives us all FTFs by weight, combining OTFs together.
#     3. A map from weight to a set of object transformations that have that weight
from Queue import PriorityQueue
from ObjectTransformation import ObjectTransformation
import itertools

class RavensTransformation():
    """Class Representing all possible figure transformations.
    
    Definitions:
      Source: RavensFigure, the figure that is being mapped from
      Goal: RavensFigure, the figure that is being mapped to

    Data structures:
      Map: String-OTF, string is the name of the transformation A-X:B-Y, to OTF holding the transformation
      Map: String-List<OTF>, name of the source object, to list of OTFs Z:[A-Z:B-Y, A-Z:B-X]
             used for retrieving all transformations for a given object in the source
      PriorityQueue: FTFs, priority is determined by combined weight of all the transformations
      Map: Int-List<OTF>, map from weight of OTF to all the OTFs that have that weight 
    """

    def __init__(self, source, goal):
        self.source = source
        self.goal = goal
        #self.nameToOTF = {}
        self.weightToOTFs = {}
        self.sourceObjToOTFs = {}
        self.ftfs = PriorityQueue()
        for sourceObj in source.getObjects():
            for goalObj in goal.getObjects():
                sourceBRO = BetterRavensObject(sourceObj, source)
                goalBRO = BetterRavensObject(goalObj, goal)
                # Generate ObjectTransformation
                otf = ObjectTransformation(sourceBRO, goalBRO)
                #self.nameToOTF[otf.getName()] = otf
                if otf.getWeight() in self.weightToOTFs:
                    self.weightToOTFs[otf.getWeight()].append(otf)
                else:
                    self.weightToOTFs[otf.getWeight()] = [otf]
                if otf.source.getName() in self.sourceObjToOTFs:
                    self.sourceObjToOTFs[otf.source.getName()].append(otf)
                else:
                    self.sourceObjToOTFs[otf.source.getName()] = [otf]
        # Generate all possible otf combinations and add to priority queue
        # self.ftfs.put((ftf.getWeight(), ftf))
        # Start with brute force combination, later maybe have better error checking
        # TODO: Take into accounts weights for deletion, multimapping here
        def allOptions(listOfLists):
            if(len(listOfLists) == 1:
                return [[item] for item in listOfLists[0]]
            car = listOfLists[0]
            cdr = listOfLists[1:]
            ret = []
            for el in car:
                for el2 in cdr:
                    ret.append(el2 + [el])
            return ret
        
        listOfOTFLists = []
        for mappedOTFs in self.sourceObjToOTFs.itervalues():
            listOfOTFLists.append(mappedOTFs)


        for otfList in allOptions(listOfOTFLists):
            ftf = FigureTransformation(otfList)
            self.ftfs.put((ftf.getWeight(), ftf))

    def __iter__(self):
        return self

    def next(self):
        if self.ftfs.empty():
            raise StopIteration()
        return self.ftfs.get()
