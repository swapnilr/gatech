# Put printing utilies, weights, mappings etc here
# Can possibly use import curses, but might be a lot more complicated than necessary

import time
import sys
from RavensTransformation import RavensTransformation
import itertools

class Verbosity():
    NONE = -1
    DEBUG = 0 # Prints details of failed connections as well
    INFO = 1 # Prints details of what connections a specific successful test made
    WARNING = 2 # Default
    ERROR = 3 # Shows only status of success/failure/error of each tests

__verbosity = Verbosity.WARNING

def getVerbosity():
    return __verbosity

def setVerbosity(verbosity):
    __verbosity = verbosity

# Since we will need to compute the transformations in order to check their weights, we
# should just return the transformation itself
# We return a list of tuples, where the first element of the tuple is an object from
# x and the second element of the tuple is an object from y
# TODO: For now this simply generates all combinations in a random order.
# Iteration 1: Add basic weights, so transformation from one object to another has a weight
#              and the weight of a particular mapping is the sum of weights of each object
#              to object mapping. A single transformation can be the sum or product of mapping
#              of individual attribute changes(depending on the attribute and the extent of
#              the change.
# Iteration 2: Add deletion.
# Iteration 3: Add 1 to Many mapping - Extrapolation/Addition. Cost of extrapolation should depend 
#              on what the new objects look like
# Iteration 4: Add Many to 1 mapping - Aggregation
def mappings(x, y, getTransformations=True):
    mappings = [zip(x, perm) for perm in itertools.permutations(y)]
    for mapping in mappings:
        transformations = {}
        for objectMap in mapping:
            transformations[objectMap[0].getName()] = RavensTransformation(objectMap, transform=getTransformations)
        yield transformations

class bcolors():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printList(ls, final=''):
    write = sys.stdout.write
    for e in ls:
        print e
        write("\033[F")
        time.sleep(1)
        write("\033[K")
    write(final)
    write('\n')


def testPrint():
    ls = []
    ls.append(bcolors.WARNING + "First Test Unsuccessful" + bcolors.ENDC)
    ls.append(bcolors.WARNING + "Second Test Unsuccessful" + bcolors.ENDC)
    ls.append(bcolors.WARNING + "Third Test Unsuccessful" + bcolors.ENDC)
    printList(ls, bcolors.OKGREEN +  bcolors.BOLD + "SUCCESS"+ bcolors.ENDC)
    printList(ls, bcolors.FAIL +  bcolors.BOLD + "FAIL"+ bcolors.ENDC)
