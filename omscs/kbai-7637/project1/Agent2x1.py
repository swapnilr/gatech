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
                print transformations[A_name]
                d = common.mappings(A.getObjects(), C.getObjects(), getTransformations=False)
                for mapping in d:
                    for key in mapping:
                        print mapping[key]
        return "6"
