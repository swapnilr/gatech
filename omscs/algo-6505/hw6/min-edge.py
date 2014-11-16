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

from maximumflow import maxflow_mincut
import maximumflow
import numpy as np

#Run by "Submit" button
def minedgesmincut(C,s,t):
    """ Input: A flow network defined by C,s,t (see the documentation
        for the maximumflow module on how to interpret).
        
        Output: A minimum cost cut (again see above documentation for 
            maximumflow module) that also has the minimum number of edges."""
    #Your code here
    debug = False
    import sys
    if debug:
      sys.stderr.write("Initial Graph\n")
      for arr in C:
        for j in arr:
          sys.stderr.write("%d " % j)
        sys.stderr.write("\n")
      sys.stderr.write("%d %d \n" % (s,t) )
    flow, cut = maxflow_mincut(C,s,t)
    maxC = maximumflow.cutValue(C,cut)
    v = maximumflow.flowValue(flow,s,t)
    if debug:
        sys.stderr.write("Cut value = %d\n" % maxC)
        sys.stderr.write("Flow value = %d\n" % v)
    for arr in C:
        for j in range(len(arr)):
            arr[j] = (arr[j]*maxC + 1) if arr[j] > 0 else 0
            #arr[j] = arr[j] + maxC if arr[j] > 0 else 0
    if debug:
      sys.stderr.write("New Graph\n")
      for arr in C:    
        for j in arr:
          sys.stderr.write("%d " % j)
        sys.stderr.write("\n")
      sys.stderr.write("%d %d \n" % (s,t) )
      sys.stderr.write("Cut\n")
      for i in maxflow_mincut(C,s,t)[1]:
        sys.stderr.write("%d " % i)
      sys.stderr.write("\n")        
    return maxflow_mincut(C,s,t)[1]

#Run by "Test Run" button
def main():
    C = np.zeros((6,6), dtype=int)
    s = 4
    t = 5

    C[s][0] = 2
    C[s][1] = 2
    C[s][2] = 2
    C[0][3] = 1
    C[1][3] = 1
    C[2][3] = 1
    C[3][t] = 3

    cut = minedgesmincut(C,s,t)

    assert(np.all( cut == np.array([1,1,1,1,1,0])))

if __name__ == '__main__':
    main()


