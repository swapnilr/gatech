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
from ProblemSet import ProblemSet
import argparse

# The main driver file for Project1. You may edit this file to change which
# problems your Agent addresses while debugging and designing, but you should
# not depend on changes to this file for final execution of your project. Your
# project will be graded using our own version of this file.
def main():
    parser = argparse.ArgumentParser(description='Filters for what problems to solve')
    parser.add_argument('--problem_sets', type=str, choices=['Basic','Challenge', 'Classmates'], nargs='*')
    parser.add_argument('--problems', type=int, nargs='*')
    args = parser.parse_args()
    sets=[] # The variable 'sets' stores multiple problem sets.
            # Each problem set comes from a different folder in /Problems/
            # Additional sets of problems will be used when grading projects.
            # You may also write your own problems.

    for file in os.listdir("Problems"): # One problem set per folder in /Problems/
        if file.startswith('.'):
            continue
        newSet = ProblemSet(file)       # Each problem set is named after the folder in /Problems/
        sets.append(newSet)
        for problem in os.listdir("Problems" + os.sep + file):  # Each file in the problem set folder becomes a problem in that set.
            if problem.startswith('.'):
                continue
            f = open("Problems" + os.sep + file + os.sep + problem) # Make sure to add only problem files to subfolders of /Problems/
            newSet.addProblem(f)

    # Initializing problem-solving agent from Agent.java
    agent=Agent()   # Your agent will be initialized with its default constructor.
                    # You may modify the default constructor in Agent.java

    # Running agent against each problem set
    results=open("Results.txt","w")     # Results will be written to Results.txt.
                                        # Note that each run of the program will overwrite the previous results.
                                        # Do not write anything else to Results.txt during execution of the program.
    for set in sets:
        if args.problem_sets and set.getName().split()[1] not in args.problem_sets:
            continue
        results.write("%s\n" % set.getName())   # Your agent will solve one problem set at a time.
        results.write("%s\n" % "-----------")   # Problem sets will be individually categorized in the results file.
        print set.getName()
        correct = 0
        for problem in set.getProblems():   # Your agent will solve one problem at a time.
            if args.problems and int(problem.getName().split()[3]) not in args.problems:
                continue
            problem.setAnswerReceived(agent.Solve(problem))     # The problem will be passed to your agent as a RavensProblem object as a parameter to the Solve method
                                                                # Your agent should return its answer at the conclusion of the execution of Solve.
                                                                # Note that if your agent makes use of RavensProblem.check to check its answer, the answer passed to check() will be used.
                                                                # Your agent cannot change its answer once it has checked its answer.
            
            result=problem.getName() + ": " + problem.getGivenAnswer() + " " + problem.getCorrect() + " (" + problem.correctAnswer + ")"
            if problem.getCorrect() == 'Correct':
                correct += 1
            results.write("%s\n" % result)
        results.write("\n")
        print "%d correct" % correct

if __name__ == "__main__":
    main()
