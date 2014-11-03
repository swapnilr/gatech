#Your task is twofold:
#1. Implement the polycomp(A,B) procedure below so 
#   that it returns the composition of polynomials A and B.
#2. Explain why your algorithm is O(n^3 log n) or 
#   (better still) O(n^3)
 
#In the procedure polycomp(A,B), the polynomials are given 
#as numpy arrays with type int. In numpy as in most numerical 
#packages, polynomials are represented as arrays with the 
#coefficient on the largest power oming first.  Thus, an 
#array A on length n would represent the polynomial 
#
#A[0] * x**(n-1) + A[1] * x**(n-1) + ...+ A[n-2] * x + A[n-1].
#
#We will use the same convention here.
#
#
#Two possible strategies include:
#1. Adapt one of the standard strategies for evaluating 
#   polynomials (e.g. Horner's rule) to the task of composing them.
#   If n is the larger order of the polynomials, this will give 
#   you a O(n^3 \log n) algorithm
#
#2. Use the fft (scipy.fft, scipy.ifft) to achieve a 
#   O(n^3) algorithm.  Be careful about the order of 
#   your coefficients.
#
#
#Some potentially useful calls are:
#
############################################################
#C = np.zeros(n, dtype=int) #to create an array of n zeros
#(http://docs.scipy.org/doc/numpy/reference/generated/numpy.zeros.html)
#
###########################################################
#C = np.convolve(A,B) #to convolve the arrays A and B
#(http://docs.scipy.org/doc/numpy/reference/generated/numpy.convolve.html)
#
############################################################
#V = np.polyval(A,x) #Evaluates A at the point values in x.  
# Note that A[-1] is the constant term
#(http://docs.scipy.org/doc/numpy/reference/generated/numpy.polyval.html)
#
############################################################
#c = fft(C, npts) #where npts is the number of points that will be output.
#C = ifft(c, npts) #where npts is the number of points that will be output.
#Note that C[0] is the constant term.
#(http://docs.scipy.org/doc/numpy/reference/routines.fft.html)
#
############################################################
#C = C[::-1] # to reverse the array C
#
############################################################
#C = C.real.round().astype(int) #To round complex numbers to ints along real axis
#
############################################################

import numpy as np
from numpy.fft import fft, ifft

def polycomp(A,B):
    """Computes A(B(x))"""
    #Your code here
    #return n3logn(A,B)
    return n3(A,B)

def n3(A, B):
    # This function takes O(n^3) time. The exact time for each of the different functions is
    # outlined below
    n = max(len(A),len(B))**2
    # Running FFT at n^2 points takes O(n^2 log n) time
    pts = fft(B[::-1], n)
    # Evaluate A at n^2 points takes O(n^3) time, as evaluating at a single point would
    # take O(n) time
    evals = np.polyval(A, pts)
    # ifft at n^2 points takes O(n^2 log n) time
    C = ifft(evals, n)
    C = C[::-1].real.round().astype(int)
    return C

def n3logn(A, B):
    # Running time is n^3 log(n)
    # Each convolve operation takes nlogn time. Here the n passed can be up to n^2 size.
    # Thus the longest time a convolve can take is (n^2) log (n^2) = 2n^2 log(n) = O(n^2) logn
    # We call convolve at most n times. Thus total running time is O(n^3 log n)
    C = np.zeros(max(len(A),len(B))**2, dtype = int)
    for i in A:
        C = np.convolve(C,B)
        C[-1] += i
    return C
    
def main():
    A = np.array([2, 1, 1], dtype=int)
    B = np.array([1, 3, 2], dtype=int)
    ans = polycomp(A, B)
    assert type(ans) is np.ndarray
    assert np.array_equal(ans, np.array([2, 12, 23, 15,  4], dtype=int))

if __name__ == '__main__':
    main()

