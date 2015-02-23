import MEA
import SDGB
import STWGB
import SN

def build(problem):
    figures = problem.getFigures()
    A = figures.get("A")
    B = figures.get("B")
    C = figures.get("C")

    A_B = MEA.computeDelta(A, B, False)
    A_C = MEA.computeDelta(A, C, False)

    aStructure = SDGB.build(A)

    a2bTransformGraph = STWGB.buildWithAllRules(B, A_B, A_C);
    a2cTransformGraph = STWGB.buildWithAllRules(C, A_B, A_C);
    return [SN(aStructure, a2bTransformGraph), SN(aStructure, a2cTransformGraph)]
