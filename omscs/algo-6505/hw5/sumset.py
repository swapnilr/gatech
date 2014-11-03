# Given two sets A and B of integers, their sum set C is defined to be 
# C = {a+b: aA, bB}.  For each c \in C, let m(c)denote the number of ways in
# which c can be obtained, i.e., m(c) = |{(a,b) : a A, b B, a+c = c}|.
# For example, if A = {1,2,3} and B={0,1,4}, then their sum set is 
# C = {1,2,5,3,6,4,7} and 
# m(1) = 1, m(2) = 2, m(3) = 2, m(4) = 1, m(5)=1, m(6) = 1, and m(7) = 1. 

# Answer the following:
# a) For two arbitrary sets A and B of integers, what is the worst-case 
#   complexity of computing their sum set? 
# ANSWER - O(n^2)
# b) Suppose now that A,B consist of integers in the range [0,n). Give 
#   an upper bound on the number of distinct elements in their sum set. 
# ANSWER - 2n - 1 : range [0, 2n - 2]
# c) With the above assumption, implement the sumset procedure below
#   using an O(nn)to find (c,m(c)) for each c \in C.

# Hint: Use numpy's convolve routine, which takes only O(n log n) 
# time to produce an algorithm that is O(n log n) overall.
#Example uses of convolve
#print np.convolve([3, 0, 2], [1, 1, 1, 1]))
#or
#print np.convolve(np.array([3, 0, 2]), np.array([1, 1, 1, 1]))

import numpy as np

def sumset(n,A,B):
    #Replace the naive implementation below with one that runs
    #in O(n log n) time.
    #YOUR CODE HERE
    C = np.zeros(2*n,dtype= int)
    A_transformed = np.zeros(n, dtype = int)
    B_transformed = np.zeros(n, dtype = int)
    for a in A:
        A_transformed[a] = 1
    for b in B:
        B_transformed[b] = 1
    C = np.convolve(A_transformed, B_transformed)
    return [ (i,C[i]) for i in range(len(C)) if C[i] > 0]

def main():
    A = [1,2,3]
    B = [0,1,4]

    C = sumset(5,A,B)

    C.sort()

    assert (C == [(1, 1), (2, 2), (3, 2), (4, 1), (5, 1), (6, 1), (7, 1)])

if __name__ == "__main__":
    main()


