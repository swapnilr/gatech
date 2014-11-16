#This exercise asks you to solve a problem using
#a maximum flow algorithm as a subroutine.  For 
#this purpose, you may use the provided maximumflow 
#module, which contains the following three functions
#
#(flow,cut) = maxflow_mincut(C,s,t):
#   C is assumed to be n x n numpy.ndarray and s and t are integers.
#
#   The flow network is defined by 
#   1) Vertices V = {0,...,n-1}
#   2) Edges E = {(i,j) | C[i][j] > 0}
#   3) Capacity given by the matrix C
#   4) Source vertex s
#   5) Sink vertex t
#
#   The flow is returned as an n x n numpy.ndarray.
#   The cut is returned as an array of length n where c[i] = 1
#   vertex i is in the same side of the partition as s and c[i] = 0
#   otherwise.
#
#v = flowValue(F,s,t):
#   F is assumed to be n x n numpy.ndarray representing the flow
#   and s and t are integers.  The function returns the value of 
#   the flow.
#
#v = cutValue(M,cut):
#   M is assumed to be n x n numpy.ndarray representing the capacites
#   and s and t are integers. The function the value sum of the edge
#   capacities of the cut.
#

#Implement the function below according to the documentation.
#TASK
#Implement an algorithm for the problem below and analyze its
#running time.
#
# Input: 
# Lists r and c of lengths m and n respectively, 
# consisting of positive integers.

# Output:
# An m-by-n matrix (a numpy 2d array) consisting of only 
# 0 and 1 entries, where the sum over the ith row is r[i] and
# the sum over the jth column is c[j].  If no such matrix exist,
# return None.

# Analysis
# Letting K = sum(r), your algorithm should run in O(mnK) time 
# on the RAM model.  Explain why it has this running time.

import numpy as np
from maximumflow import maxflow_mincut, flowValue

#Run by "Submit" button
def find_mtx(r,c):
    """Input: lists r and c.
         Output: A 0/1 matrix with dimensions len(r) x len(c)
                        where the sum of the ith row is r[i] and the 
                        sum of the jth column is c[j].  If no such
                        matrix exists None is returned."""
    #Your Code Here
    assert(sum(r) == sum(c))
    graph_size = len(r) + len(c) + 2
    K = sum(r)
    C = np.zeros((graph_size,graph_size), dtype=int)
    s = 0
    t = 1
    # Indices for r vertices are [2, len(r) + 2)
    for i in range(len(r)):
        C[s][i+2] = r[i]
    # Indices for c vertices are [len(r) + 2, graph_size)
    for i in range(len(c)):
        C[i+2+len(r)][t] = c[i]
    for i in range(2,len(r)+2):
        for j in range(len(r)+2, graph_size):
            C[i][j] = 1
    flow,cut = maxflow_mincut(C,s,t)
    M = np.zeros((len(r),len(c)), dtype=int)
    for i in range(2,len(r)+2):
        for j in range(len(r)+2, graph_size):
            if flow[i][j] == 1:
                M[i-2][j-(len(r)+2)] = 1
    if flowValue(flow,s,t) != sum(r):
        return None
    return M
    

#Run by "Test Run" button
def main():
    #Here are contraints where there is no satisfying matrix
    (r,c) = ([3, 1, 3], [1, 3, 3])

    assert(find_mtx(r,c) is None)

    #Here are constraints where there is a satisfying matrix
    (r,c) = ([1, 2, 2], [1, 1, 3])

    M = find_mtx(r,c)

    assert( M is not None)

    rsum = [0 for i in range(len(r))]
    csum = [0 for i in range(len(c))]

    for i in range(len(r)):
        for j in range(len(c)):
            assert(M[i][j] in [0,1])
            rsum[i] += M[i][j]
            csum[j] += M[i][j]

    assert(rsum == r)
    assert(csum == c)
    
if __name__ == "__main__":
    main()

