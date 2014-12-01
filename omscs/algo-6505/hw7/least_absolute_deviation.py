# Use linear programming to accomplish the following task.
# Given an mxn matrix A and a vector b of length m, 
# find a vector x such that |Ax-b|_1 is minimized.  
# In other words, find x such that 
# sum( abs(b[i] - (Ax)[i]) for i in range(m)) is minimized
# (Hint: you will want to introduce new variables for both 
# the positive and negative differences between b[i] (Ax)[i]).
#
# For this exercise, we will use pymprog.  Documentation
# can be found here
# http://pymprog.sourceforge.net/tutorial.html#a-dive-in-example
#
# Please read the documentation before attempting the exercise.
# Some key points to note are
#
# 1. When declare a set of variable for your linear program as in
# x = var([0,1,2])
# you get back a dictionary with [0,1,2] as the keys (they don't
# even have to be integers)
# and
# unique pymprog.variable as the values.
# 2. Thus, when you specify the objective function as in
#
# maximize( 1.0 * x[0] - 2.0 * x[1] )
# 
# or specify a set of constraints as in
#
# st( [ x[0] <= 1, x[2] <= 3])
#
# the expressions are interpretted as a computer algebra system
# would (think Mathematica) and added to the model.
#3. By default variables are constrained to be nonnegative.
# You can remove this restriction by the statment
# None <= x[0]
#
#4. Pymprog doesn't like numpy's types, so you have to cast them
# back to floats via
#
# float(c[1])
#
# for example.
#
# Here is a super-simple example of a program that uses pymprog
#
# c = numpy.array([1.0, -2.0], dtype=float)
# b = numpy.array([1.0, 3.0], dtype=float)
#
# beginModel('basic')  
# verbose(False)

# x = var([0,1,2])

# maximize( float(c[0]) * x[0] + float(c[1]) * x[1] )

# st( [ x[0] <= float(b[0]), x[2] <= float(b[1]) ])

# solve()

# endModel() #Good habit: do away with the problem

# print numpy.array([x[i].primal for i in [0,1,2]])

from pymprog import *
import numpy as np
import sys

def labsdev(A,b):
    """Input: A numpy array A with shape = (m,n) and a numpy array b.
       Output: A numpy array x that minimizes |b - Ax|_1.
    """

    (m,n) = A.shape
    beginModel('basic')  
    verbose(False)
    y = var(range(n+m))
    constraints = []
    func = 0
    for i in range(m):
        func += y[n+i]
        b_i = float(b[i])
        a_sum = 0
        for j in range(n):
            a_sum += A[i][j]*y[j]
        constraints += [y[n+i] >= b_i - a_sum, y[n+i] >= a_sum - b_i]
    minimize(func)
    st(constraints)
    solve()
    endModel()
    x_l = []
    for i in range(n):
        x_l.append(y[i].primal)
    return np.array(x_l, dtype=float)

    

def main():
    A = np.array([[1,0],
                [0,1],
                [0,1]],dtype=float)
    b = np.array([1, 2, 1],dtype=float)

    x = labsdev(A,b)

    Ax = np.dot(A,x)

    r = b - Ax

    assert (sum(abs(r[i]) for i in range(3)) == 1.0)

if __name__ == '__main__':
    main()

