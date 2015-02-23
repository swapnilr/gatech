import common
import random

class Agent2x1():

    def Solve(self, problem):
        figures = problem.getFigures()
        A = figures.get("A")
        B = figures.get("B")
        C = figures.get("C")
        choices = ["1", "2", "3", "4", "5", "6"]
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
        print problem.getName()
        for repeat in [True, False]:
          for AB_ftf in common.mappings(A.getObjects(), B.getObjects(), repeats=repeat):
            for testName in choices:
                testFigure = figures.get(testName)
                for CD_ftf in common.mappings(C.getObjects(), testFigure.getObjects(), repeats=repeat):
                    #ab_trans = AB_ftf.getNameTranslation('') == 'Y' and AB_ftf.getNameTranslation('X') == 'X' and AB_ftf.getNameTranslation('Y') == 'Z'
                    #cd_trans = CD_ftf.getNameTranslation('Z') == 'Y' and CD_ftf.getNameTranslation('Y') == 'Z' and CD_ftf.getNameTranslation('X') == 'X'
                    #if testName == "2" and ab_trans and cd_trans:
                    #  print "----------------------------------------------------------------"
                    #  print "Trying %s" % testName
                    #  print "AB %s" % AB_ftf
                    #  print "CD %s" %CD_ftf
                    if AB_ftf == CD_ftf:
                        answer = problem.checkAnswer(testName)
                        if answer != testName:
                            print "Name - %s, Answer - %s, Guess - %s" % (
                                    problem.getName(), answer, testName)
                            print AB_ftf
                            print CD_ftf
                        return testName
                    #if testName == "2" and ab_trans and cd_trans:
                    #    print "----------------------------------------------------------------"
        guess = random.choice(choices)
        print "Guessing!" 
        #print "Name - %s, Answer - %s, Guess - %s" % (
        #    problem.getName(), problem.checkAnswer(guess), guess)
        return guess
