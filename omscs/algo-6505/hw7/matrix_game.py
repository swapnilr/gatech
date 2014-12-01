#Let A be a matrix with m rows and n columns.  Such a matrix defines 
#a two-person game as follows.  Two players, Row and Column play a 
#game where Row selects a row i and Column selects a column j. 
#If A[i][j] >0 Row receives a payoff amount of A[i][j] . If A[i][j] <0,
#Row pays an amount of -A[i][j] to Column.  The payoff matrix A is 
#known to both players.
#
#Suppose Row picks the ith row with probability p[i] and announces this 
#vector p.  Knowing this vector, Column will choose column j that 
#minimizes Row's expected payout.  Thus, the expected payout is 
#z = min_j \sum p[i]*A[i][j].  Naturally, Row then will want to 
#choose the vector (p1,,pm) so as to maximize this quantity.  
#Express Row's problem as a linear program.  Of course, p[i] >=0
#and \sum_i p[i] = 1.
#
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
# Here is a super-simple example
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

def rowStrategy(A):
    (m,n) = A.shape
    beginModel('basic')  
    verbose(False)
    p_v = var(range(m+1))
    constraints = []
    func = p_v[m]
    v = p_v[m]
    for j in range(n):
        pa_sum = 0
        for i in range(m):
            pa_sum += p_v[i]*float(A[i][j])
        #print pa_sum, v
        constraints += [pa_sum >= v]
        
    p_sum = 0
    for i in range(m):
        p_sum += p_v[i]
        #constraints += [p_v[i] >= 0]
    #constraints += [ None < p_v[m]]
    #print p_sum
    constraints += [p_sum == 1]#, 1 >= p_sum]
    #print func
    #print constraints
    maximize(func)
    st(constraints)
    st(None <= p_v[m])
    solve()
    endModel()
    #sys.stderr.write(str(np.array([p_v[i].primal for i in range(m+1)])))
    #sys.stderr.write("\n")
    p = []
    for i in range(m):
        p.append(p_v[i].primal)
    return np.array(p, dtype=float)

    #return n

def main():
    A = np.array([[1,0],
                [0,1]],dtype=float)

    x = rowStrategy(A)
    ans = np.array([0.5,0.5], dtype=float)
    assert(np.allclose(x,ans))

    assert ( min(x.dot(A)) + 1.0e-8 > 0.5)

if __name__ == '__main__':
    main()






