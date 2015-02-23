import cmd
from BetterRavensFigure import BetterRavensFigure
from RavensTransformation import ObjectTransformation

class InteractiveAgent(cmd.Cmd):

    def do_list_figures(self, line):
        "List Figures"
        for key in self.figures:
            print key

    def do_print_figure(self, figure):
        "Print figure"
        if figure not in self.figures:
            print "Figure Name not found"
            return
        brf = BetterRavensFigure(self.figures[figure])
        print brf

    def do_list_objects(self, figure):
        "List objects in figure"
        if figure not in self.figures:
            print "Figure Name not found"
            return
        brf = BetterRavensFigure(self.figures[figure])
        for obj in brf.objects.itervalues():#self.figures[figure].getObjects():
            print obj

    def do_get_answer(self, line):
        print self.answer

    def do_print_object(self, line):
        "print_object [Figure] [Object]"
        parts = line.split()
        if len(parts) != 2:
            print "Incorrect number of arguments"
            return
        if parts[0] not in self.figures:
            print "Figure name not found"
            return
        brf = BetterRavensFigure(self.figures[parts[0]])
        if parts[1] not in brf:
            print "Object name not found"
            return
        obj = brf[parts[1]]
        print obj

    def do_get_transformation(self, line):
        "get_transformations [Figure 1] [Object 1] [Figure 2] [Object 2]"
        parts = line.split()
        if len(parts) != 4:
            print "Incorrect number of arguments."
            return
        if parts[0] not in self.figures or parts[2] not in self.figures:
            print "Incorrect figure names"
            return
        transformation = self.get_transformation(parts[0], parts[1], parts[2], parts[3])
        if type(transformation) == type(1):
            return
        print transformation

    def get_transformation(self, f1, o1, f2, o2):
        brf1 = BetterRavensFigure(self.figures[f1])
        brf2 = BetterRavensFigure(self.figures[f2])
        if o1 not in brf1 or o2 not in brf2:
            print "Incorrect object names"
            return -1
        transformation = ObjectTransformation([brf1[o1].RO, brf2[o2].RO])
        return transformation

    def do_comp_transformations(self, line):
        "comp_transformations [F1]-[O1] [F2]-[O2] [F3]-[O3] [F4]-[O4]"
        parts = line.split()
        if len(parts) != 4:
            print "Incorrect number of arguments"
            return
        figs = []
        objs = []
        for i in range(4):
            p = parts[i].split('-')
            if len(p) != 2:
                print "%s formatted incorrectly" % p
                return
            figs.append(p[0])
            objs.append(p[1])
        t1 = self.get_transformation(figs[0], objs[0], figs[1], objs[1])
        t2 = self.get_transformation(figs[2], objs[2], figs[3], objs[3])
        if type(t1) == type(1) or type(t2) != type(t1):
            return
        print t1 == t2

    def do_exit(self, line):
        "Exit"
        return True

    def Solve(self, problem):
        self.figures = problem.getFigures()
        #Setup variables
        self.answer=problem.checkAnswer("1")
        self.cmdloop()
        
