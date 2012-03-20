#import os
#import re
#import math 
#import getpass
#import sys
#
#import fractions
#import sympy
#import matrix
#
#
#from login import LoggerInner
#from webUtils import WebUtils
#
#import eea
#import grind
#import matrix
#
#bs_username = "cYate"
#bs_password = ""
#
#cookiefile = "brightshadows.cookies"
#
#baseurl = "http://www.bright-shadows.net"
#
#challengepath = "/challenges/programming/calculate"
#linkPath = challengepath + "/tryout.php"
#solutionPath = challengepath + "/solution.php"
#
#UNITS = range(0, 10)
#SQUARES = [x**2 for x in range(0, 10)]
#CUBES = [x**3 for x in range(0, 10)]

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
	print 'get nonzero solutions for ux + vy = z where u = %d, v = %d, z = %d'%(u, v, z)
	print 'xValues in ', xValues
	print 'yValues in ', yValues
	
	a, b, d = ExtendedEuclid(u, v)

	print 'a = %d, b = %d, d = %d'%(a, b, d)
	print 'ua+vb = ', (u*a+v*b)
	
	solutions = []

	print 'to get ua+vb = %d...'%z

	# xk = a + (551)k (a=212)
	# yk = b - (13)k (b=-5)
	kLim1 = ((abs(a)*z) / v) + 1 # to get xk > 0
	print 'klim1= abs(%d/%d)+1 = %d'%((a*z), v, kLim1)
	kLim2 = ((abs(b)*z) / u) + 1 # to get yk > 0
	print 'klim2= abs(%d/%d)+1 = %d'%((b*z), u, kLim2)

	minK = min(kLim1, kLim2)
	maxK = max(kLim1, kLim2)

	print 'mink = %d, maxk= %d'%(minK, maxK)
	for k in range(minK, minK+1): # should be maxk
		xk = a*z - v*k/d	
		yk = b*z + u*k/d
		print 'k = ', k
		print 'xk %d = (%d*%d) + %d*%d/%d) = '%(xk, a, z, v, k, d)
		print 'yk %d = (%d*%d) + %d*%d/%d) = '%(yk, b, z, v, k, d)

		if xk in xValues and yk in yValues:

			solutions.append((xk, yk))

	return solutions
#
#def Tuplify(expression, negate = False):
## turn things like 224242*a**2 into a tuple (coeff, symbol, exponent)
#	coeff = 0
#	symbol = ''
#	exponent = 0
#
#	if "**" in expression: #(expected true apart from the scalar)
#		t = expression.split("**")
#		exponent = int(t[1])
#		if "*" in t[0]:
#			t2 = t[0].split("*")
#			coeff = int(t2[0])
#			symbol = t2[1]
#		else:
#			if t[0][0] == '-':
#				coeff = -1
#			else:
#				coeff = 1
#			symbol = t[0][1::]
#	elif "*" in expression:
#		t = expression.split("*")
#		coeff = int(t[0])
#		symbol = t[1]
#		exponent = 1 
#	else:
#		if re.search("[a-z]", expression):
#			if expression[0] == '-':
#				coeff = -1
#			else: 
#				coeff = 1
#			
#			symbol = expression[0::]
#			exponent = 1
#		else:
#			coeff = int(expression)
#
#	if negate:
#		return (-coeff, symbol, exponent) 
#	else:
#		return (coeff, symbol, exponent) 
#
#

UNITS = range(0, 10)
SQUARES = [x**2 for x in range(0, 10)]
CUBES = [x**3 for x in range(0, 10)]

def SolveEEA(args):
		print "Solve EEA args = ", args
		
		scalars = [ a for a in args if a[1] == '' ]
		
		z = scalars[0][0]
		u = args[1][0]
		xPow = args[1][2]

		v = args[2][0]
		yPow = args[2][2]

		ranges = [UNITS, SQUARES, CUBES]
		
		result = [] 		
		results = NonZeroSolutions(u, v, z, ranges[xPow-1], ranges[yPow-1])

		for r in results:
			if xPow == 1:
				tx = r[0]
			elif xPow == 2:				
				tx = SQUARES.index(r[0])
			elif xPow == 3:
				tx = CUBES.index(r[0])
			if yPow == 1:
				ty = r[1]	
			elif yPow == 2:
				ty = SQUARES.index(r[1])
			elif yPow == 3:
				ty = CUBES.index(r[1])
			result.append((tx, ty))

		if len(result) == 1:
			return "%d%d"%(result[0][0],result[0][1])
		else:
			return "Multiple!"

# solns = NonZeroSolutions(9, 5, 81, 9, 9)
#		print solns

#		a, b, d = eea(13, 551)
#		a, b, d = eea(352, 168)
#		a, b, d = eea(3458, 4864)
#		a, b, d = eea(-3463, 6843)
#		a, b, d = eea(45, 25)
#		print (a, b, d)
#		a, b, d = eea(9, 5)
#		print (a, b, d)
#		a, b, d = eea(49, 29)
#		print (a, b, d)
#
