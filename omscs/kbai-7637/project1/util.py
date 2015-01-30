import itertools

def pairs(x, y):
    """
    Given 2 lists x and y, this returns a list of lists of tuples of every possible matching of X and Y
    For example:
        common.pairs(['A', 'B'] , [1,2])
        [[('A', 1), ('B', 2)], [('A', 2), ('B', 1)]]

    Note: This assumes len(x) == len(y). The caller logic must extend one of the lists to match the other
    based on other logic.
    """
    return [zip(x, perm) for perm in itertools.permutations(y)]
