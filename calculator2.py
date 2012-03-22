from solvematrix import SolveMatrix
from tuplify import Tuplify
from grind import SolveGrind

class Calculator2(object):
    def __init__(self, inputLine):
        if inputLine == "":
            raise ValueError("inputLine cannot be null")
        self.result = None
        self._parse(inputLine)

    def _parse(self, inputLine):
        # equation = inputLine.replace('"', '')
        # equation = equation.replace("_", "**")

        # self.equation = equation

        # split = equation.split('=')

        # # prepend an explicit + if the lhs or rhs start without one
        # lhs = split[0]
        # if lhs[0] != '-':
            # lhs = "+" + lhs
        # rhs = split[1]
        # if rhs[0] != '-':
            # rhs = "+" + rhs

        # # insert spaces
        # lhs = lhs.replace("+", " +")
        # lhs = lhs.replace("-", " -")
        # rhs = rhs.replace("+", " +")
        # rhs = rhs.replace("-", " -")

        # self.args = []

        # lhsItems = lhs.split()
        # for e in lhsItems:
            # self.args.append(Tuplify(e))
        # rhsItems = rhs.split()
        # for e in rhsItems:
            # self.args.append(Tuplify(e, True))

        # self.raw_unknowns = []
        # self.unknowns = []
        # self.coeffs = {}

        # for a in self.args:
            # if a[1] == '':
                # self.sumTotal = a[0]
            # else:
                # #u = "%s_%d" % (a[1], a[2])
                # u = (a[1], a[2])
                # # look for all the a**3, b**2 etc
                # if u not in self.unknowns:
                    # self.unknowns.append(u)
                    # # collate coeffs
                    # self.coeffs[u] = a[0]
                # else:
                    # # collate coeffs
                    # self.coeffs[u] = self.coeffs[u] + a[0]

                # # collect all the a, b, etc
                # if a[1] not in self.raw_unknowns:
                    # self.raw_unknowns.append(a[1])
        return "Parsed"
        
    def Solve(self):
        self.result = "no result"
