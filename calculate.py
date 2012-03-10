import os
import re
import math 

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
		if inputLine == "":					
			raise ValueError("inputLine cannot be null")

		self.result = None

		self.Parse(inputLine)
		

	def Parse(self, inputLine):
		equation = inputLine.replace('"', '')

		equation = equation.replace("=", "==")
		equation = equation.replace("_", "**")		
		
		abc = re.compile('([a-z])')			
		self.unknowns = sorted(set(abc.findall(equation)))
		self.values = {}
		
		equation = abc.sub(r'self.values["\1"]', equation)		
		self.equation = equation

#		print "Equation to be used\n" + self.equation
	def Solve(self):
		self.result = "no result"
		
		m = 10 ** len(self.unknowns)
#		print "max = ", m
		for i in range(0, m-1):
			tempi = i

			for u in self.unknowns:				
				self.values[u] = tempi % 10
				tempi /= 10
#			print "i = %d, result = %r" % (i, eval(self.equation))

			res = eval(self.equation)
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
