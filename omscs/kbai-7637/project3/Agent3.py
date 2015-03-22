# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.
import features
import cv2
import numpy as np
from scipy import signal
from Queue import PriorityQueue as PQ

class Agent3:
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
        figures = problem.getFigures()
        A = cv2.imread(figures["A"].fullpath, cv2.CV_LOAD_IMAGE_GRAYSCALE).astype(np.int32)
        B = cv2.imread(figures["B"].fullpath, cv2.CV_LOAD_IMAGE_GRAYSCALE).astype(np.int32)
        C = cv2.imread(figures["C"].fullpath, cv2.CV_LOAD_IMAGE_GRAYSCALE).astype(np.int32)
        best_guess = float("inf")
        answer = ""
        #corr = signal.correlate2d(A, B)
        #corr = signal.fftconvolve(A, B)
        sumpq = PQ()
        diffpq = PQ()
        ssimpq = PQ()
        mulpq = PQ()
        trapzpq = PQ()
        ssdpq = PQ()

        # Generate values for ALL of the guesses, then with [1,2,3,4], use the ratio 1:2  to 1:4 to guess how
        # confident you are in the guess, use the confidence as weight
        for guess in map(str, range(1,7)):
            trial = cv2.imread(figures[guess].fullpath, cv2.CV_LOAD_IMAGE_GRAYSCALE).astype(np.int32)
            sumpq.put((features.sumFeature(A, B, C, trial).value(), guess))
            diffpq.put((features.diffFeature(A, B, C, trial).value(), guess))
            ssimpq.put((features.ssimFeature(A, B, C, trial).value(), guess))
            #sumpq.put((features.corrFeature(A, B, C, trial, corr)
            mulpq.put((features.mulFeature(A, B, C, trial).value(), guess))
            trapzpq.put((features.trapzFeature(A, B, C, trial).value(), guess))
            ssdpq.put((features.ssdFeature(A, B, C, trial).value(), guess))
            #print trial, gsf
            #val = gsf#.value()
            #if val < best_guess:
            #    best_guess = val
            #    answer = guess
        weightMap = {0:1.0, 1:0.8, 2:0.6, 3:0.4, 4:0.2,5:0.1}
        totalPQ = []
        FEATURES = 6
        for i in range(FEATURES):
            totalPQ.append(PQ())
        for i in range(6):
            totalPQ[0].put((-weightMap[i], sumpq.get()[1]))
            totalPQ[1].put((-weightMap[i], diffpq.get()[1]))
            totalPQ[2].put((-weightMap[i], ssimpq.get()[1]))
            totalPQ[3].put((-weightMap[i], mulpq.get()[1]))
            totalPQ[4].put((-weightMap[i], trapzpq.get()[1]))
            totalPQ[5].put((-weightMap[i], ssdpq.get()[1]))
        finalVal = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0}
        for i in range(6):
            for j in range(FEATURES):
                v, guess = totalPQ[j].get()
                finalVal[guess] += -v
        val=0
        answer = ""
        for guess in map(str, range(1,7)):
            if val < finalVal[guess]:
                answer = guess
                val = finalVal[guess]
        return answer
