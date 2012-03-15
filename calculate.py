import os
import re
import math 
import getpass

import sympy
import fractions

from login import LoggerInner
from webUtils import WebUtils
import matrix 

bs_username = "cYate"
bs_password = ""

cookiefile = "brightshadows.cookies"

baseurl = "http://www.bright-shadows.net"

challengepath = "/challenges/programming/calculate"
linkPath = challengepath + "/tryout.php"
solutionPath = challengepath + "/solution.php"

units = range(0, 10)
squares = [x**2 for x in range(0, 10)]
cubes = [x**3 for x in range(0, 10)]

def ExtendedEuclid(u, v):
    u1 = 1
    u2 = 0
    u3 = u
    v1 = 0
    v2 = 1
    v3 = v
    while v3 != 0:
        q = u3 / v3
        t1 = u1 - q*v1
        t2 = u2 - q*v2
        t3 = u3 - q*v3
        u1 = v1
        u2 = v2
        u3 = v3
        v1 = t1
        v2 = t2
        v3 = t3
    return u1, u2, u3

def NonZeroSolutions(u, v, z, xValues, yValues):
    print 'get nonzero solutions for ux + vy = z where u = %d, v = %d, z = %d'%(u,v,z)
    print 'xValues in ',xValues
    print 'yValues in ',yValues
    
    a,b,d = ExtendedEuclid(u,v)

    print 'a = %d, b = %d, d = %d'%(a,b,d)
    print 'ua+vb = ',(u*a+v*b)
    
    solutions = []

    print 'to get ua+vb = %d...'%z

    # xk = a + (551)k (a=212)
    # yk = b - (13)k (b=-5)
    kLim1 = ((abs(a)*z) / v) + 1 # to get xk > 0
    print 'klim1= abs(%d/%d)+1 = %d'%((a*z),v,kLim1)
    kLim2 = ((abs(b)*z) / u) + 1 # to get yk > 0
    print 'klim2= abs(%d/%d)+1 = %d'%((b*z),u,kLim2)

    minK = min(kLim1, kLim2)
    maxK = max(kLim1, kLim2)

    print 'mink = %d, maxk= %d'%(minK,maxK)
    for k in range(minK, minK+1): # should be maxk
        xk = a*z - v*k/d    
        yk = b*z + u*k/d
        print 'k = ',k
        print 'xk %d = (%d*%d) + %d*%d/%d) = '%(xk, a, z, v, k, d)
        print 'yk %d = (%d*%d) + %d*%d/%d) = '%(yk, b, z, v, k, d)

        if xk in xValues and yk in yValues:

            solutions.append((xk, yk))

    return solutions

def Tuplify(expression, negate = False):
# turn things like 224242*a**2 into a tuple (coeff, symbol, exponent)
    coeff = 0
    symbol = ''
    exponent = 0

    if "**" in expression: #(expected true apart from the scalar)
        t = expression.split("**")
        exponent = int(t[1])
        if "*" in t[0]:
            t2 = t[0].split("*")
            coeff = int(t2[0])
            symbol = t2[1]
        else:
            if t[0][0] == '-':
                coeff = -1
            else:
                coeff = 1
            symbol = t[0][1::]
    elif "*" in expression:
        t = expression.split("*")
        coeff = int(t[0])
        symbol = t[1]
        exponent = 1 
    else:
        if re.search("[a-z]", expression):
            if expression[0] == '-':
                coeff = -1
            else: 
                coeff = 1
            
            symbol = expression[0::]
            exponent = 1
        else:
            coeff = int(expression)

    if negate:
        return (-coeff, symbol, exponent) 
    else:
        return (coeff, symbol, exponent) 


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
        self.answer = 0
                
        for a in self.args:            
            if a[1] == '':
                self.answer = a[0]
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
                    
        self.values = []
        
    def Solve(self):
        self.result = "no result"

        m1 = len(self.unknowns)
        if m1 == 2:
            self.SolveEEA()
        else:
            self.SolveMatrix()
            
#    def FindPower(self, exp):
#        se = str(exp)
#        if "**" in se:
#            return int(se.split("**")[1])
#        else:
#            return 1

    def _sortedCoeffs(self):
        keys = self.unknowns
        print "ks = ",keys
        keys.sort()
        return map(self.coeffs.get, keys)
        
    def SolveMatrix(self):
        print "Matrix solution"
        
        print "unknowns: ",self.unknowns
        print "raw_unknowns: ",self.raw_unknowns
        print "coeffs: ", self.coeffs
        
        a_t = sympy.Matrix(self._sortedCoeffs())
        print "a_t = \n",a_t
        a_tI = matrix.appendIdentity(a_t)
        print "a_tI = \n",a_tI
        RT = matrix.unimod(a_tI)
        print "RT = \n",RT
        R = RT[:,0]
        print "R = \n",R
        T = RT[:,1:]
        print "T = \n",T
        R_t = R.transpose()
        print "R_t = \n",R_t
        T_t = T.transpose()
        print "T_t = \n",T_t
        
        k_list = []
        for i in range(0, len(R)):
            k_list.append(sympy.Symbol('k_%d'%i))
        print "ks = ", k_list
        
        K = sympy.Matrix(k_list)
        print "K = \n",K       
        
        R_txK = R_t * K
        print "R_txK = ",R_txK
        if R_txK.shape != (1,1):
            raise TypeError('expected 1x1')
        
        K[0] = self.answer
        
        unknowns = T_t * K
        print "unknowns: \n", unknowns
        
    def SolveEEA(self):
        print "Solve EEA self args = ",self.args
        
        scalars = [ a for a in self.args if a[1] == '' ]
        
        z = scalars[0][0]
        u = self.args[1][0]
        xPow = self.args[1][2]

        v = self.args[2][0]
        yPow = self.args[2][2]

        ranges = [units, squares, cubes]
        
        self.result = []         
        results = NonZeroSolutions(u, v, z, ranges[xPow-1], ranges[yPow-1])

        for r in results:
            if xPow == 1:
                tx = r[0]
            elif xPow == 2:                
                tx = squares.index(r[0])
            elif xPow == 3:
                tx = cubes.index(r[0])
            if yPow == 1:
                ty = r[1]    
            elif yPow == 2:
                ty = squares.index(r[1])
            elif yPow == 3:
                ty = cubes.index(r[1])
            self.result.append((tx, ty))

        if len(self.result) == 1:
            self.stringResult = "%d%d"%(self.result[0][0],self.result[0][1])
        else:
            self.stringResult = "Multiple!"
# solns = NonZeroSolutions(9,5,81,9,9)
#        print solns

#        a,b,d = self.eea(13,551)
#        a,b,d = self.eea(352,168)
#        a,b,d = self.eea(3458,4864)
#        a,b,d = self.eea(-3463, 6843)
#        a,b,d = self.eea(45,25)
#        print (a,b,d)
#        a,b,d = self.eea(9,5)
#        print (a,b,d)
#        a,b,d = self.eea(49,29)
#        print (a,b,d)
#
    def SolveGrind(self):
    
        m2 = len(self.unknowns)
        m = 10 ** m2    
#        print "max = ", m
        for i in range(0, m-1):
            tempi = i

            for u in self.unknowns:                
                self.values[u] = tempi % 10
                tempi /= 10

            res = eval(self.equation_calc)
            if res:
                r = 0
                for u in self.unknowns[:-1]:
                    r += self.values[u]
                    r *= 10
                r += self.values[self.unknowns[-1]]

                self.result = r

                break
        self.stringResult = "ground"

if __name__ == '__main__':
    bs_password = getpass.getpass("Enter password:")
    LoggerInner(bs_username, bs_password, cookiefile)
    pageGetter = WebUtils(cookiefile, baseurl)
    problem = pageGetter.getHTML(linkPath)
    print problem
    v = re.search('\"[0-9a-z+-=_*]*\"', problem)
    print v.group()
#    vv = v.group(0)[1:-1]
    calculator = Calculator(v.group())
    calculator.Solve()
    
    print calculator.result
    
    solutionParams = "?solution="
    solpath = "%s%s%s" %(solutionPath, solutionParams, "")
    print solpath
    print pageGetter.getHTML(solpath)
