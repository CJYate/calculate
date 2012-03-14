import sys
import re
import getpass

import sympy

import matrix
from login import LoggerInner
from webUtils import WebUtils

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

		self.unknowns = []
		self.coeffs = []
		for a in self.args:
			self.coeffs.append(a[0])
			if a[1] != '' and a[1] not in self.unknowns:
				self.unknowns.append(a[1])
		self.values = []

		print "unknowns: ",self.unknowns
		print "coeffs: ",self.coeffs

	def Solve(self):
		self.result = "no result"

		m1 = len(self.unknowns)

		mat = sympy.Matrix([self.coeffs[:-1]]).transpose()
		mat2 = matrix.appendIdentity(mat)
		a1 = matrix.unimod(mat2)
		print a1
		a2 = mat2.rref()
		print a2

#		if m1 == 2:
#			self.SolveEEA()
#		else:
#			self.SolveGrind()

if __name__ == '__main__':
	if len(sys.argv) == 2:
		bs_password = sys.argv[1]
	else:
		bs_password = getpass.getpass("Enter password:")

	LoggerInner(bs_username, bs_password, cookiefile)
	pageGetter = WebUtils(cookiefile, baseurl)
	
	problem = pageGetter.getHTML(linkPath)
	print problem
	
	v = re.search('\"[0-9a-z+-=_*]*\"', problem)
	print v.group()
	
	calculator = Calculator(v.group())
	calculator.Solve()
	
	print calculator.result
	
	solutionParams = "?solution="
	solpath = "%s%s%s" %(solutionPath, solutionParams, "")
	print solpath
	print pageGetter.getHTML(solpath)
