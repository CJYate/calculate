import re

import sympy

import matrix 
from solveMatrix import SolveMatrix
from tuplify import Tuplify

units = range(0, 10)
squares = [x**2 for x in range(0, 10)]
cubes = [x**3 for x in range(0, 10)]

class Calculator(object):
    def __init__(self, inputLine):
        if inputLine == "":                    
            raise ValueError("inputLine cannot be null")
        self.result = None
        self.Parse(inputLine)
        

    def Parse(self, inputLine):
        equation = inputLine.replace('"', '')
        equation = equation.replace("_", "**")        

        self.equation = equation
        
        split = equation.split('=')
        
        # prepend an explicit + if the lhs or rhs start without one
        lhs = split[0]
        if lhs[0] != '-':
            lhs = "+" + lhs
        rhs = split[1]    
        if rhs[0] != '-':
            rhs = "+" + rhs
    
        # insert spaces
        lhs = lhs.replace("+", " +")
        lhs = lhs.replace("-", " -")
        rhs = rhs.replace("+", " +")
        rhs = rhs.replace("-", " -")
        
        self.args = []

        lhsItems = lhs.split()
        for e in lhsItems:
            self.args.append(Tuplify(e))
        rhsItems = rhs.split()
        for e in rhsItems:
            self.args.append(Tuplify(e, True))

        self.raw_unknowns = []
        self.unknowns = []
        self.coeffs = {}        
                
        for a in self.args:            
            if a[1] == '':
                self.sumTotal = a[0]
            else:
                u = "%s_%d"%(a[1],a[2])
                
                # look for all the a**3, b**2 etc               
                if u not in self.unknowns:
                    self.unknowns.append(u)
                    # collate coeffs
                    self.coeffs[u] = a[0]
                else:
                    # collate coeffs
                    self.coeffs[u] = self.coeffs[u] + a[0]                    
                    
                # collect all the a, b, etc
                if a[1] not in self.raw_unknowns:
                    self.raw_unknowns.append(a[1])
                    
    def Solve(self):
        self.result = "no result"
        self.stringResult = SolveMatrix(self.raw_unknowns, self.unknowns, self.coeffs, self.sumTotal)
            
    # # def _sortedCoeffs(self):
        # # keys = self.unknowns
        # # print "ks = ",keys
        # # keys.sort()
        # # return map(self.coeffs.get, keys)
        
    # # def SolveMatrix(self):
        # print "Matrix solution"
        
        # # print "unknowns: ",self.unknowns
        # # print "raw_unknowns: ",self.raw_unknowns
        # # print "coeffs: ", self.coeffs
        
        # a_t = sympy.Matrix(self._sortedCoeffs())        
        # a_tI = matrix.appendIdentity(a_t)
        # # print "a_tI = \n",a_tI
        
        # RTfrac = a_tI.rref()[0]
        # # print "RTFrac = \n",RTfrac
        # Rf = RTfrac[:,0]
        # Tf = RTfrac[:,1:]
        # Tf_t = Tf.transpose()
        
        # RT = matrix.unimod(a_tI)
        # R = RT[:,0]        
        # T = RT[:,1:]
        # # print "T = \n",T
        # R_t = R.transpose()
        # T_t = T.transpose()
        # print "T_t = \n",T_t
                
        # k_symbols = []
        # for i in range(0, len(R)):
            # k_symbols.append(sympy.Symbol('k_%d'%i))            
        # K = sympy.Matrix(k_symbols)
        
        # R_txK = R_t * K
        # if R_txK.shape != (1,1):
            # raise TypeError('expected 1x1')
        
        # K[0] = self.sumTotal
        
        # unknowns = T_t * K
        # # print "unknowns values: \n", unknowns
        
        # unknowns_f = Tf_t * K
        # print "unknowns _frac values: \n", unknowns_f                        
        
        # def fn(K):
            # t = str(unknowns_f[-1])
            # func = re.sub(r'k_([0-9])', r'K[\1]', t)
            # return eval(func)
        
        
        # print "fn = \n",fn(K)        
        
        # print self.unknowns
        # print units 
        # print squares 
        # print cubes 
        