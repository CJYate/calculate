import os
import urllib
import urllib2
import cookielib

import numpy
import scipy.linalg

from login import LoggerInner
from webUtils import WebUtils

bs_username = "cYate"
bs_password = "shadowmaster"

cookiefile = "brightshadows.cookies"

baseurl = "http://www.bright-shadows.net"

challengepath = "/challenges/programming/calculate"
linkPath = challengepath + "/tryout.php"
solutionPath = challengepath + "/solution.php"

class Calculator(object):
	def __init__(self, inputLine):
		self.Parse(inputLine)

	def Parse(self, inputLine):
		equation = inputLine[inputLine.find('\"') + 1: inputLine.rfind('\"')]

		equation = equation.replace("-", "+-")
		equation = equation.replace("=", "=+")
		equation = equation.replace("++", "+")		
		parts = equation.split('=')

		lhs = parts[0]
		if lhs[0] == '+':
			lhs = lhs[1:]
		lhsparts = lhs.split('+')
		
		rhs = parts[1]		
		if rhs[0] == '+':
			rhs = rhs[1:]
		rhsparts = rhs.split('+')

		allparts = lhsparts
	
		for part in rhsparts:
			if part[0] == '-':
				allparts.append(part[1:])
			else:
				allparts.append("-" + part)

		allparts_split = []
		for p in allparts:
			tp = p.split('*')
			if len(tp) == 1:
				tp = [tp[0], '1']
			allparts_split.append(tp)


		self.matrixSize = len(allparts_split)
		self.unknownsValues = [t[1] for t in allparts_split]
		self.coefficients = [t[0] for t in allparts_split]
		
		print self.matrixSize
		print self.unknownsValues
		print self.coefficients

	def Solve(self):
		


LoggerInner(bs_username, bs_password, cookiefile)
pageGetter = WebUtils(cookiefile, baseurl)
problem = pageGetter.getHTML(linkPath)
print problem

calculator = Calculator(problem)

calculator.Solve()

print calculator.result

solutionParams = "?solution="
solpath = "%s%s%s" %(solutionPath, solutionParams, "")
print solpath
print pageGetter.getHTML(solpath)
