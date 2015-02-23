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

def extended_pairs(x, y):
    """
    Here we assume that len(x) < len(y)

    The way we extend it is to add more elements to x picked with repetition, and zip with that

    """
    extra_possibilities = list(itertools.combinations_with_replacement(x, len(y) - len(x)))
    extras = []
    for possibility in extra_possibilities:
        tempx = x + list(possibility)
        extras.extend(pairs(tempx, y))
    tempx = x
    tempx.extend([None]*(len(y) - len(x)))
    extras.extend(pairs(tempx, y))
    return extras

def generic_pairs(x,y):
    if len(x) < len(y):
        return extended_pairs(x,y)
    return pairs(x,y)
