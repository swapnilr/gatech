import numpy as np

#Suppose there is a procedure inA that decides a language A.  
#Use dynamic programming (not memoization) to create an 
#algorithm that decides A* while calling inA only O(n^2) times, 
#where n is the length of the input string.

#This is run by "Submit"
def inAstar(x, inA):
    """ Returns true if x is in A^* and false otherwise.
    The input inA should be assumed to be a function 
    that takes are string as input and return True or False."""
    #Your code here
    matrix = []
    # Calling O(n^k) procedure inA n^2 times, leading to a running time of
    # O(n^(k+2))
    for i in range(len(x) + 1):
        matrix.append([])
        for j in range(len(x) + 1):
            matrix[i].append(inA(x[i:j]))
    # The following code runs depth first search on the graph that is represented
    # by the adjacency matrix 'matrix'
    import Queue
    queue = Queue.Queue()
    for index, val in enumerate(matrix[0]):
        if val:
            queue.put(index)
    seen = [False] * (len(x) + 1)
    seen[0] = True
    while not queue.empty():
        s = queue.get()
        seen[s] = True
        if s == len(x):
            return True
        for index, val in enumerate(matrix[s]):
            if not seen[index] and val:
                queue.put(index)
    return False


#This is run by "Test Run"
def main():
    def inA(x):
        return x in ['0','10']

    assert(inAstar('0101000010', inA))

    assert(not inAstar('000110010', inA))

if __name__ == '__main__':
    main()

