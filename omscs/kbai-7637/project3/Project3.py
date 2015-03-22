# DO NOT MODIFY THIS FILE.
#
# When you submit your project, an alternate version of this file will be used
# to test your code against the sample Raven's problems in this zip file, as
# well as other problems from the Raven's Test and former students.
#
# Any modifications to this file will not be used when grading your project.
# If you have any questions, please email the TAs.
#
#

import os
from Agent import Agent
from VisualProblemSet import VisualProblemSet
import cv2
import pickle
from util import get
import subprocess
# The main driver file for Project3. You may edit this file to change which
# problems your Agent addresses while debugging and designing, but you should
# not depend on changes to this file for final execution of your project. Your
# project will be graded using our own version of this file.
def main():
    sets=[] # The variable 'sets' stores multiple problem sets.
            # Each problem set comes from a different folder in /Problems/
            # Additional sets of problems will be used when grading projects.
            # You may also write your own problems.

    for file in os.listdir("Problems (Image Data)"): # One problem set per folder in /Problems/
        if file.startswith('.'):
            continue
        newSet = VisualProblemSet(file)       # Each problem set is named after the folder in /Problems/
        sets.append(newSet)
        for problem in os.listdir("Problems (Image Data)" + os.sep + file):  # Each file in the problem set folder becomes a problem in that set.
            if problem.startswith('.'):
                continue
            newSet.addProblem(file, problem)

    # Initializing problem-solving agent from Agent.java
    agent=Agent()   # Your agent will be initialized with its default constructor.
                    # You may modify the default constructor in Agent.java
    num = 0
    # Running agent against each problem set
    results=open("Results.txt","w")     # Results will be written to Results.txt.
                                        # Note that each run of the program will overwrite the previous results.
                                        # Do not write anything else to Results.txt during execution of the program.
    h = {}
    for set in sets:
        results.write("%s\n" % set.getName())   # Your agent will solve one problem set at a time.
        results.write("%s\n" % "-----------")   # Problem sets will be individually categorized in the results file.
        #if 'Basic' not in set.getName():
        #    continue
        for problem in set.getProblems():   # Your agent will solve one problem at a time.
            #a = problem.checkAnswer("")
            #figures = problem.getFigures()
            #A = figures["A"].fullpath
            #B = figures["B"].fullpath
            #C = figures["C"].fullpath
            #ans = figures[a].fullpath
            #folder = 'templates/template%d' % num
            #subprocess.call(['mkdir', folder])
            #subprocess.call(['cp', A, '%s/A.png' % folder])
            #subprocess.call(['cp', B, '%s/B.png' % folder])
            #subprocess.call(['cp', C, '%s/C.png' % folder])
            #subprocess.call(['cp', ans, '%s/ans.png' % folder])
            #num += 1

            problem.setAnswerReceived(agent.Solve(problem))     # The problem will be passed to your agent as a RavensProblem object as a parameter to the Solve method
                                                                # Your agent should return its answer at the conclusion of the execution of Solve.
                                                                # Note that if your agent makes use of RavensProblem.check to check its answer, the answer passed to check() will be used.
                                                                # Your agent cannot change its answer once it has checked its answer.

            result=problem.getName() + ": " + problem.getGivenAnswer() + " " + problem.getCorrect() + " (Correct Answer: " + problem.checkAnswer("") + ")"

            results.write("%s\n" % result)
        results.write("\n")
    #pickle.dump(h, open("hash.p", "wb"))

if __name__ == "__main__":
    main()
