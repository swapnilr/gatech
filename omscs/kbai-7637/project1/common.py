# Put printing utilies, weights, mappings etc here
# Can possibly use import curses, but might be a lot more complicated than necessary

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

def mappings(x, y):
    return [zip(x, perm) for perm in itertools.permutations(y)]

# Have debug mode etc specified on the command line possibly(default it to non-verbose
def showTimes():
    import time
    from datetime import datetime
    import sys

    write = sys.stdout.write

    for i in range(10):
        s = str(datetime.now())
        print s
        write("\033[F")
        time.sleep(1)
    write('\n')

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
    import time, sys
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
