# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.
import cv2
from skimage.measure import structural_similarity as ssim
from Queue import PriorityQueue as PQ

THRESHOLD = 0.8

class Agent2:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.d = {}
        for i in range(40):
            self.d[i] = cv2.imread('templates/template%d/A.png' % i, cv2.CV_LOAD_IMAGE_GRAYSCALE)

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
    def Solve(self,problem,threshold=THRESHOLD):
        figures = problem.getFigures()
        A = cv2.imread(figures["A"].fullpath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        B = cv2.imread(figures["B"].fullpath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        C = cv2.imread(figures["C"].fullpath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        guesses = {}
        for guess in ["1", "2", "3", "4", "5", "6"]:
            guesses[guess] = cv2.imread(figures[guess].fullpath, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        pq_A = PQ()
        for i, A_g in self.d.iteritems():
            pq_A.put((-ssim(A, A_g), i))
        pq_Guess = PQ()
        for i in range(5):
            val, ind = pq_A.get()
            if -val > threshold:
                B_g = cv2.imread('templates/template%d/B.png' % ind, cv2.CV_LOAD_IMAGE_GRAYSCALE)
                C_g = cv2.imread('templates/template%d/C.png' % ind, cv2.CV_LOAD_IMAGE_GRAYSCALE)
                ans_g = cv2.imread('templates/template%d/ans.png' % ind, cv2.CV_LOAD_IMAGE_GRAYSCALE)
                B_val = ssim(B_g, B)
                if B_val < threshold:
                    continue
                C_val = ssim(C_g, C)
                if C_val < threshold:
                    continue
                max_val = -2
                best_guess = 0
                for guess in ["1", "2", "3", "4", "5", "6"]:
                    guessim = ssim(guesses[guess], ans_g)
                    if guessim > max_val:
                        max_val = guessim
                        best_guess = guess
                if max_val < threshold:
                    continue
                sum_val = -val + max_val + B_val + C_val
                pq_Guess.put((-sum_val, best_guess))
        if not pq_Guess.empty():
            return pq_Guess.get()[1]
