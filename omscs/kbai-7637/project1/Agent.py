# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.
import itertools
import copy
from Agent2x1 import Agent2x1

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return a String representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These Strings
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName().
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(String givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will#not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # @param problem the RavensProblem your agent should solve
    # @return your Agent's answer to this problem
    def Solve(self,problem):
        if problem.getProblemType() == '2x1':
           agent = Agent2x1()
           agent.Solve(problem)
        return "5"

    def __solve2x1(self, problem):
        for objectMap in self.mappings(A.getObjects(), B.getObjects()): 
            # Add Mapping to nothing, and calculating weights of mappings
            for newFig in self.__applyMappings(C, self.__getAttrMappings(objectMap)):
                for option in ["1", "2", "3", "4", "5", "6"]:
                    if self.__matches(newFig, figures.get(newFig)):
                        # Later get most likely option, not just perfect option
                        return option 
        return "6"

    def __applyMappings(figure, mappings):
        D = copy.deepcopy(C)
        for mapping in self.mappings(copy.deepcopy(C), mappings.keys()):
            yield self.__applyMapping(D, mapping)

    def __applyMapping(obj, mapping):
        pass

    def __getAttrMappings(objectMap):
        """
        Returns:
            dict[obj] = {attrName: (initValue, finalValue)}
        """
        s = {}
        for object1, object2 in objectMap:
            betterObj = BetterRavensObject(object2)
            s[object1] = {}
            for attr in object1.getAttributes:
                if betterObj.hasAttr(attr.getName()):
                    s[object1][attr.getName()] = (attr.getValue(), betterObj.getValue(attr.getName()))
        return s

    def __matches(figure1, figure2):
        pass
