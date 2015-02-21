from RavensTransformation import RavensTransformation
import random

class Agent2x2():

    def __init__(self):
        # This holds the map between figures and a RavensTransformation
        #   The key is "<sourceFigureName>-<goalFigureName>", such as A-B or C-5
        #   The value is an RavensTransformation(FTFSet/OTFSet). RavensTransformation holds
        #     1. For each object in source, OTF to each object in goal
        #     2. A priority queue that gives us all FTFs by weight, combining OTFs together.
        #     3. A map from weight to a set of object transformations that have that weight
        self._transformations_ = {}

    def __generateTransformations__(self, figure1, figure2):
        """Create a RavensTransformation with these 2 figures and to the transformation map"""
        # Take care about how to generate OTFs when you map to "deletion", or multimap or addition
        # If len(figure1) == len(figure2):
        #   Simple map(or maybe multimap + deletion, explore later, with heavier weights
        # elif len(figure1) > len(figure2):
        #   Object deletion(aggregation, if taking into account challenge cases)
        # else:
        #   Object addition or multimap
        transformation_name = "%s-%s" % (figure1.getName(), figure2.getName())
        self._transformations_[transformation_name] = RavensTransformation(figure1, figure2)

    def Solve(self, problem):
        figures = problem.getFigures()
        A = figures.get("A")
        B = figures.get("B")
        C = figures.get("C")
        self.__generateTransformations__(A, B)
        self.__generateTransformations__(A, C)
        choices = ["1", "2", "3", "4", "5", "6"]
        for choice in choices:
            option = figures.get(choice)
            self.__generateTransformations__(B, option)
            self.__generateTransformations__(C, option)
        
        # 1. Get "Lightest" A-B Transformation - (OTF0, .. OTFn)
        # 2. Given the weights of the each OTF (w0, ... wn), where n = max(no of figures in A|B)
        #   a. For each of C-1 through C-6
        #     i. Create a table keyed by OTF(can use)
        #     ii. For each weight wj, get all OTFs of that weight. Compare this OTF to OTFj. 
        #         If it matches, keep in the table
        #     iii. Of remaining possibilities, evaluate to get "viable" one. If viable one exists, we're done.
        #     iv. (Optional) Evaluate similarly in A-C, B-[1..6]. This can either be used as a tie breaker, a
        #          verifier or an extra hypothesis generator if we are left to guess.
        candidateRTs = map(lambda choice: self._transformations_["C-%s" % choice], choices)

        for ftf in self._transformations_["A-B"]:
            for candidateRT in candidateRTs:
               otfOptions = {}
               for otf in ftf:
                   options = candidateRT.getOTFsByWeight(otf.getWeight())
                   otfOptions[otf] = filter(lambda x: otf == x, options)
               # Evaluate Viable combinations
               # TODO: Make more intelligent
               valid = True
               for otf, options in ftf.iteritems():
                   if len(options) == 0:
                       valid = False
                       break
               if valid:
                   return candidateRT.goal.getName()
        return random.choice(choices)
