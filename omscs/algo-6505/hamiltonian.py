import pycosat

def reduce_it(G):
    """ Input: an adjacency matrix G of arbitrary size represented as a list of lists.
        Output: the clauses of the cnf formula output in pycosat format.  
        Each clause is be reprented as a list of nonzero integers.
        Positive numbers indicate positive literals, negatives negative literal.
        Thus, the clause (x_1 \vee \not x_5 \vee x_4) is represented 
        as [1,-5,4].  A list of such lists is returned."""
    rules = []
    # Size of Graph
    n = len(G)
    
    # Each literal x_ij represents node j being at position i of the hamiltonian path
    
    # Each node must be on the path
    # For each j, we add the clause (x_1j or ... or x_nj)
    for node in range(1,n+1):
        rule = []
        for position in range(1,n+1):
            rule.append(literal(position, node))
        rules.append(rule)
    
    # No node must be present more than once on the path
    # For each j, we add clauses (not x_ij or not x_kj) for all pairs i,k where i != k
    for node in range(1,n+1):        
        for position1 in range(1,n+1):
            for position2 in range(1,n+1):
                rule = [0 - literal(position1,node)]
                if position1 != position2:
                    rule.append(0 - literal(position2, node))
                    rules.append(rule)
    
    # There has to be a node at each position on the path
    # For each position i, we add the clause (x_i1 or ... or x_in)
    for position in range(1,n+1):
        rule = []
        for node in range(1,n+1):
            rule.append(literal(position, node))
        rules.append(rule)
    
    # For any given position i, there is exactly one node
    # For each position i, we add clauses (not x_ij or not x_ik) when j != k
    for position in range(1,n+1):        
        for node1 in range(1,n+1):
            for node2 in range(1,n+1):
                rule = [0 - literal(position, node1)]
                if node1 != node2:
                    rule.append(0 - literal(position, node2))
                    rules.append(rule)

    # Nothing that is not on the graph can be on the path
    # For each adjacent positions k, k+1, we look at all node pairs that aren't
    # on the graph and add the clause (not x_ki or not x_k+1j)
    for node1 in range(1,n+1):        
        for node2 in range(1,n+1):
            if G[node1-1][node2-1] != 1:
              for position in range(1, n):
                  rule = [0 - literal(position, node1)]
                  rule.append(0 - literal(position+1, node2))
                  rules.append(rule)
    return rules
    
def literal(position, node):
    return int(str(position) + str(node))
##End Your Code HERE...

def main():
    #A graph with a hamiltonian path
    G = [[0, 0, 0, 1, 1], 
    [0, 0, 0, 0, 1], 
    [0, 0, 0, 1, 0], 
    [1, 0, 1, 0, 1], 
    [1, 1, 0, 1, 0]]

    clauses = reduce_it(G)

    sol = pycosat.solve(clauses)

    assert(sol != 'UNSAT')

    #A graph without a hamiltonian path
    G = [[0, 1, 1, 1, 1], 
    [1, 0, 0, 0, 0], 
    [1, 0, 0, 0, 0], 
    [1, 0, 0, 0, 1], 
    [1, 0, 0, 1, 0]]

    clauses = reduce_it(G)

    sol = pycosat.solve(clauses)

    assert (sol == 'UNSAT')

if __name__ == "__main__":
    main()