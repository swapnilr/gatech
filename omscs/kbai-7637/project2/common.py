# Put printing utilies, weights, mappings etc here
# Can possibly use import curses, but might be a lot more complicated than necessary

import time
import sys
from RavensTransformation import ObjectTransformation
from RavensTransformation import FigureTransformation
import itertools
import util
from Queue import PriorityQueue

# Clean up verbosity and pretty printing

class Verbosity():
    NONE = -1
    DEBUG = 0 # Prints details of failed connections as well
    INFO = 1 # Prints details of what connections a specific successful test made
    WARNING = 2 # Default
    ERROR = 3 # Shows only status of success/failure/error of each tests

__verbosity = Verbosity.WARNING

def getVerbosity():
    return __verbosity

def writeAllowed(givenVerbosity):
    return getVerbosity() <= givenVerbosity

# Since we will need to compute the transformations in order to check their weights, we
# should just return the transformation itself
# We return a list of tuples, where the first element of the tuple is an object from
# x and the second element of the tuple is an object from y
# TODO: For now this simply generates all combinations in a random order.
# Iteration 1: Add basic weights, so transformation from one object to another has a weight
#              and the weight of a particular mapping is the sum of weights of each object
#              to object mapping. A single transformation can be the sum or product of mapping
#              of individual attribute changes(depending on the attribute and the extent of
#              the change. Sometimes location is more important, other times shape matching is more
#              important.
# Iteration 3: Add support for moving things around intelligently(understands above vs below etc)
# Iteration 3: Add 1 to Many mapping - Extrapolation/Addition. Cost of extrapolation should 
#              depend on what the new objects look like
# Iteration 4: Add Many to 1 mapping - Aggregation
# Add Shapes and shape properties(such as rotating a circle is possible with it remaining the same)
# Or invarianze to reflection. Also properties such as reflection/angle/orientation should have it's own
# handler
def mappings(x, y, getTransformations=True, repeats=False):
    tempy = y
    if len(y) < len(x):
        tempy.extend([None]*(len(x) - len(y)))
    mappings = util.pairs(x, tempy)
    if len(x) < len(y):
        mappings = util.extended_pairs(x, y)
        # Mappings defined as follows: Given x=[1], y=[1,2], we want
    queue = PriorityQueue()
    for mapping in mappings:
        ftf = FigureTransformation()
        for objectMap in mapping:
            name = objectMap[0].getName()
            otf = ObjectTransformation(objectMap, ftf, transform=getTransformations, try_repeats=repeats)
            ftf.add(name, otf)
        yield ftf
    #    queue.put((ftf.getWeight(), ftf))
    #while not queue.empty():
    #    yield queue.get()[1]


class bcolors():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ProgressPrinter():

    def __init__(self):
        self.write = sys.stdout.write
        self.write("\n")

    def updateProgress(self, text, verbosity=Verbosity.WARNING):
        if writeAllowed(verbosity):
            self.write("\033[F")
            self.write("\033[K")
            print text

def testPrint2():
    pp = ProgressPrinter()
    pp.updateProgress(bcolors.WARNING + "First Test Unsuccessful" + bcolors.ENDC)
    time.sleep(1)
    pp.updateProgress(bcolors.WARNING + "Second Test Unsuccessful" + bcolors.ENDC)
    time.sleep(1)
    pp.updateProgress(bcolors.WARNING + "Third Test Unsuccessful" + bcolors.ENDC)
    time.sleep(1)
    pp.updateProgress(bcolors.OKGREEN + bcolors.BOLD + "SUCCESS" + bcolors.ENDC)

    pp = ProgressPrinter()
    pp.updateProgress(bcolors.WARNING + "First Test Unsuccessful" + bcolors.ENDC)
    time.sleep(1)
    pp.updateProgress(bcolors.WARNING + "Second Test Unsuccessful" + bcolors.ENDC)
    time.sleep(1)
    pp.updateProgress(bcolors.WARNING + "Third Test Unsuccessful" + bcolors.ENDC)
    time.sleep(1)
    pp.updateProgress(bcolors.FAIL + bcolors.BOLD + "FAIL" + bcolors.ENDC)

