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

UNITS = range(0, 10)
SQUARES = [x**2 for x in range(0, 10)]
CUBES = [x**3 for x in range(0, 10)]

def SolveGrind(equation_calc, unknowns, values):		
	m2 = len(unknowns)
	m = 10 ** m2	
#		print "max = ", m
	for i in range(0, m-1):
		tempi = i

		for u in unknowns:				
			values[u] = tempi % 10
			tempi /= 10

		res = eval(equation_calc)
		if res:
			r = 0
			for u in unknowns[:-1]:
				r += values[u]
				r *= 10
			r += values[unknowns[-1]]

			break
	stringResult = "ground"
	return stringResult