import unittest
import timeit

from calculate import Calculator
import re

class CalculatorTests(unittest.TestCase):
	def testCalculatorEmptyInitialisation(self):
		self.assertRaises(ValueError,Calculator, '')

	def testCalc_result_None_Presolve(self):
		c = Calculator('a=2')
		self.assertEqual(None, c.result)

	# def testCalc_a_2_eq_4(self):
		# c = Calculator('a_2=4')
		# self.assertEqual(['a_2'], c.unknowns)
		# c.Solve()
		# self.assertEqual(2, c.result)
	
	# def testCalc_a_1_eq_1(self):
		# c = Calculator('a_2=1')
		# self.assertEqual(['a_2'], c.unknowns)
		# c.Solve()
		# self.assertEqual(1, c.result)

	# def testCalc_a_10_eq_None(self):		
		# c = Calculator('a_2=10')
		# self.assertEqual(['a_2'], c.unknowns)
		# c.Solve()
		# self.assertEqual("no result", c.result)

	# def testCalc_a_0_eq_0(self):
		# c = Calculator('a_2=0')
		# self.assertEqual(['a_2'], c.unknowns)
		# c.Solve()
		# self.assertEqual(0, c.result)

	def testRegex(self):
		theinput = 'a424**__==++bc'
		abc = re.compile('[abc]')
		actual = sorted(set(abc.findall(theinput)))
		expected = ['a', 'b', 'c']
		self.assertEqual(expected, actual)

	def testRegex2(self):
		theinput = 'a424**__==++32b32c323c313a'
		abc = re.compile('[abc]')
		actual = sorted(set(abc.findall(theinput)))
		expected = ['a', 'b', 'c']
		self.assertEqual(expected, actual)

	def testCalc_ab_22(self):
		c = Calculator('a_2+b_3=12')
		self.assertEqual(['a_2','b_3'], c.unknowns)
		c.Solve()
		self.assertEqual('22', c.stringResult)

	def testCalc_ab_22_scaled(self):
		c = Calculator('13*a_2+551*b_3=4460')
		self.assertEqual(['a_2','b_3'], c.unknowns)
		c.Solve()
		self.assertEqual('22', c.stringResult)

	def testReformat_simple(self):
		eq = '13*a_2+551*b_3=283165'
#		exp = '+13*a**2+551*b**3-283165'
		exp = '13*a**2+551*b**3=283165'
		c = Calculator('13*a_2+551*b_3=283165')
		self.assertEqual(exp, c.equation)	

	# def testSimpleSoln(self):
		# eq = '9*a_1+5*b_1=81'
		# c = Calculator(eq)
		# c.Solve()
		# exp = [(9, 4), (0, 9)]
		# self.assertEqual(exp, c.result)	

	def testReformat_simple2(self):
		eq = '13*a_2=-551*b_3+283165'
#		exp = '+13*a**2+551*b**3-283165'		
		exp = '13*a**2+551*b**3=283165'
		c = Calculator('13*a_2+551*b_3=283165')
		self.assertEqual(exp, c.equation)	

	def testCalc_ab_98(self):
		t= timeit.Timer()
		c = Calculator('13*a_2+551*b_3=283165')
		self.assertEqual(['a_2','b_3'], c.unknowns)
		c.Solve()
		self.assertEqual('98', c.stringResult)
		print t.timeit()


	def testCalc_abcde_53682(self):
		t= timeit.Timer()
		c = Calculator('-515*a_2+5151*b_3+6611*c=1324*d_2-133*e+81398')
		self.assertEqual(['a_2','b_3', 'c_1','d_2','e_1'], c.unknowns)
		c.Solve()
		self.assertEqual(53682, c.stringResult)
		print t.timeit()

if __name__ == '__main__':
	unittest.main()
	
