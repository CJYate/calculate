import itertools
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



def _sorted_coeffs(unknowns, coeffs):
    """ Sort coefficients by their terms, alphabetically
    """
    keys = unknowns    
    keys.sort()
    return map(coeffs.get, keys)



def SolveGrind(raw_unknowns, unknowns, coeffs, negTotal):		

	sumTotal = -negTotal
	print "solve brute force - raw unknow = %s\n unknonw = %s\n coeffs = %s, sum = %s " % (raw_unknowns, unknowns, coeffs, sumTotal)
	
	problem_size = len(unknowns)
	
	prod = 'itertools.product('
	for unknown in unknowns:
		expo = unknown[1]
		if expo == 1:
			prod = prod + '%s,' % UNITS
		elif expo == 2:
			prod = prod + '%s,' % SQUARES
		elif expo == 3:
			prod = prod + '%s,' % CUBES
		else:
			continue
	prod = prod + ')'
	print "prod = ",prod
	
	sorted_coefficients = _sorted_coeffs(unknowns, coeffs)
	print "sorted coeffs = ", sorted_coefficients
	
	count = 0
	for option in eval(prod):
		sum = 0
		for i in range(0, problem_size):
			sum = sum + sorted_coefficients[i] * option[i]
		#print "count = %i sum = %i" % (count, sum)

		if sum == sumTotal:
			print "Found an Answer %s, %s!," % (count, option)
			break
		
		count = count + 1
	
	stringResult = str(count).zfill(problem_size)
	
	return stringResult