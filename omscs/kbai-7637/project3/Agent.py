# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.
import os
import subprocess

import Agent1
import Agent2
import Agent3

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.agent1 = Agent1.Agent1()
        self.agent2 = Agent2.Agent2()
        self.agent3 = Agent3.Agent3()

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
        sol = None
        try:
            sol = self.agent1.Solve(problem)
            agent = 1
        except Exception as e:
            pass
        if not sol:
            for i in [0.9, 0.8]:
                try:
                    sol = self.agent2.Solve(problem, i)
                    agent = 2
                except Exception as e:
                    pass
                if sol:
                    break
            if not sol:
                try:
                    sol = self.agent3.Solve(problem)
                    agent = 3
                except Exception as e:
                    pass
        ans = problem.checkAnswer(sol)
        # Add case based learning
        if ans != sol:
            existingTemplates = os.listdir("templates")
            nextNum = len(existingTemplates)
            figures = problem.getFigures()
            subprocess.call(['mkdir', 'templates%stemplate%d' % (os.sep, nextNum) ])
            subprocess.call(['cp', figures["A"].fullpath, 'templates%stemplate%d%sA.png' % (os.sep, nextNum, os.sep)])
            subprocess.call(['cp', figures["B"].fullpath, 'templates%stemplate%d%sB.png' % (os.sep, nextNum, os.sep)])
            subprocess.call(['cp', figures["C"].fullpath, 'templates%stemplate%d%sC.png' % (os.sep, nextNum, os.sep)])
            subprocess.call(['cp', figures[ans].fullpath, 'templates%stemplate%d%sans.png' % (os.sep, nextNum, os.sep)])
        print "%s: %s using agent %d" % (problem.getName(), sol, agent)
        return sol
