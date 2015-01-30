import common

class Agent2x1():

    def Solve(self, problem):
        figures = problem.getFigures()
        A = figures.get("A")
        B = figures.get("B")
        C = figures.get("C")
        # Pseudocode:
        # generate mapping between A and B - Object to object mapping(G&T)
        #   get transformations required for that object to object mapping(MEA)
        #   O1: generate a mapping from A to C(G&T)
        #         Generate D, test with each of 1 to 6 to compare
        #   O2: For C : 1 to 6, generate mapping
        #         Compare mapping to mapping between A and B (G&T)
        # A to B = Object to object map + transformations per object pair.
        #          MAB[A_Obj] = {attr1: transformation, attr2:t2,...}
        # A to C = Object to object map MAC[C_obj] = A_obj
        # C -> D : MAB[MAC[C_obj]] -> {attr:transformation}. Apply to C to get D
        # Match D to 1 through 6. Compare objects and each attribute
        for transformations in common.mappings(A.getObjects(), B.getObjects()):
            for A_name in transformations:
                #print transformations[A_name] # Add verbose flag + create printing utilities
                #d = common.mappings(A.getObjects(), C.getObjects(), getTransformations=False)
                #for mapping in d:
                #    for key in mapping:
                #        print mapping[key]
                original_transformation = transformations[A_name].getTransformations()
                for test in ["1", "2", "3", "4", "5", "6"]:
                    testFig = figures.get(test)
                    for tt in common.mappings(C.getObjects(), testFig.getObjects()):
                        for C_name in tt:
                            test_trans = tt[C_name].getTransformations()
                            if test_trans == original_transformation:
                                #print "Gonna guess %s" % test
                                answer = problem.checkAnswer(test)
                                if answer != test:
                                    print "Name - %s, Answer - %s, Guess - %s" % (
                                        problem.getName(), problem.checkAnswer(test), test)
                                return test
        print "Name - %s, Answer - %s, Couldn't Guess!!" % (
            problem.getName(), problem.checkAnswer(""))
        return ""
