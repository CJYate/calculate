import sys
import re
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
			
#	def FindPower(self, exp):
#		se = str(exp)
#		if "**" in se:
#			return int(se.split("**")[1])
#		else:
#			return 1

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
		a_tI = matrix.appendIdentity(a_t)
		print "a_tI = \n",a_tI
		RT = matrix.unimod(a_tI)
		R = RT[:,0]		
		T = RT[:,1:]
		print "T = \n",T
		R_t = R.transpose()
		T_t = T.transpose()
		print "T_t = \n",T_t
		
		k_list = []
		for i in range(0, len(R)):
			k_list.append(sympy.Symbol('k_%d'%i))
		K = sympy.Matrix(k_list)
		
		R_txK = R_t * K
		if R_txK.shape != (1,1):
			raise TypeError('expected 1x1')
		
		K[0] = self.answer
#		print "eigenvals = ",T_t.eigenvals()  
#		print "eigenvects = ",T_t.eigenvects()  
		unknowns = T_t * K
#		print "LUsolve -> \n",T_t.LUsolve(K)
		print "LUdecomp = \n",T_t.LUdecomposition()
		print "unknowns values: \n", unknowns
		print self.unknowns
		print units 
		print squares 
		print cubes 

if __name__ == '__main__':
	bs_password = getpass.getpass("Enter password:")
	LoggerInner(bs_username, bs_password, cookiefile)
	pageGetter = WebUtils(cookiefile, baseurl)
	problem = pageGetter.getHTML(linkPath)
	print problem
	v = re.search('\"[0-9a-z+-=_*]*\"', problem)
	print v.group()
#	vv = v.group(0)[1:-1]
	calculator = Calculator(v.group())
	calculator.Solve()
	
	print calculator.result
	
	solutionParams = "?solution="
	solpath = "%s%s%s" %(solutionPath, solutionParams, "")
	print solpath
	print pageGetter.getHTML(solpath)
