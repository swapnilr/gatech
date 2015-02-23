import KB
import PS

class Agent2x2:

    def __init__():
        attrInfo = {} # string: set<string>

    def Solve(self, problem):
        answer = "0"
        semNetworks = KB.build(problem) # Array of SN
        answer = PS.solve(problem, semNetworks)
        problem.checkAnswer(answer) 
        return answer
