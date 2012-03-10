import os
import re
import math 
import sympy 
#from sympy.abc import a,b,c,d,e,f,g

from login import LoggerInner
from webUtils import WebUtils
import fractions

bs_username = "cYate"
bs_password = "shadowmaster"

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
	for k in range(minK, maxK):
		xk = a*z + v*k/d	
		yk = b*z - u*k/d
		print 'k = ',k
		print 'xk = (%d*%d) + %d*%d/%d) = '%(xk, a, z, v, k, d)
		print 'yk = (%d*%d) + %d*%d/%d) = '%(yk, b, z, v, k, d)

		if xk in xValues and yk in yValues:

			solutions.append((xk, yk))

	return solutions

class Calculator(object):
	def __init__(self, inputLine):
		if inputLine == "":					
			raise ValueError("inputLine cannot be null")

		self.result = None

		self.Parse(inputLine)
		

	def Parse(self, inputLine):
		equation = inputLine.replace('"', '')

		equation = equation.replace("_", "**")		
		
		self.equation_m = self.Reformat(equation)
		
		equation = equation.replace("=", "==")
		abc = re.compile('([a-z])')			
		self.unknowns = sorted(set(abc.findall(equation)))
		self.values = {}
		
		equation = abc.sub(r'self.values["\1"]', equation)		
		self.equation_calc = equation

	def Reformat(self, equation):
		
		split = equation.split('=')

		lhs = split[0]
		if lhs[0] != '-':
			lhs = "+" + lhs
		rhs = split[1]	
		if rhs[0] != '-':
			rhs = "+" + rhs
	
		rhs = rhs.replace("+", "minus")
		rhs = rhs.replace("-", "plus")
		rhs = rhs.replace("minus", "-")
		rhs = rhs.replace("plus", "+")
		
		equation = lhs + rhs
		fun = sympy.sympify(equation)

		print fun.args
		self.args = fun.args
		print "Reformatted : " + equation	

		return equation

	def Solve(self):
		self.result = "no result"

		m1 = len(self.unknowns)
		if m1 == 2:
			self.SolveEEA()
		else:
			self.SolveGrind()
			
	def FindPower(self, exp):
		se = str(exp)
		if "**" in se:
			return int(se.split("**")[1])
		else:
			return 1

	def SolveEEA(self):
		print "EEA"
	
		print units
		print squares
		print cubes

		z = -self.args[0]		
		u = int(str(self.args[1]).split('*')[0])

		xPow = self.FindPower(self.args[1])
		v = int(str(self.args[2]).split('*')[0])
		yPow = self.FindPower(self.args[2])

		ranges = [units, squares, cubes]

		print 'u %d, v %d, z %d'%(u,v,z) 
		print NonZeroSolutions(u, v, z, ranges[xPow-1], ranges[yPow-1])

# solns = NonZeroSolutions(9,5,81,9,9)
#		print solns

#		a,b,d = self.eea(13,551)
#		a,b,d = self.eea(352,168)
#		a,b,d = self.eea(3458,4864)
#		a,b,d = self.eea(-3463, 6843)
#		a,b,d = self.eea(45,25)
#		print (a,b,d)
#		a,b,d = self.eea(9,5)
#		print (a,b,d)
#		a,b,d = self.eea(49,29)
#		print (a,b,d)
#
	def SolveGrind(self):
	
		m2 = len(self.unknowns)
		m = 10 ** m2	
#		print "max = ", m
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
			

if __name__ == '__main__':
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
