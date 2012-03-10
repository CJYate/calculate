import unittest
from calculate import Calculator
import re

class SympyTests(unittest.TestCase):
	def testCalculatorEmptyInitialisation(self):
		self.assertRaises(ValueError,Calculator, '')

	def testCalc_result_None_Presolve(self):
		c = Calculator('a=2')
		self.assertEqual(None, c.result)

	def testCalc_a_2_eq_4(self):
		c = Calculator('a_2=4')
		c.Solve()
		self.assertEqual(['a'], c.unknowns)
		self.assertEqual(2, c.result)

	def testCalc_a_1_eq_1(self):
		c = Calculator('a_2=1')
		c.Solve()
		self.assertEqual(['a'], c.unknowns)
		self.assertEqual(1, c.result)

	def testCalc_a_10_eq_None(self):		
		c = Calculator('a_2=10')
		c.Solve()
		self.assertEqual(['a'], c.unknowns)
		self.assertEqual("no result", c.result)

	def testCalc_a_0_eq_0(self):
		c = Calculator('a_2=0')
		c.Solve()
		self.assertEqual(['a'], c.unknowns)
		self.assertEqual(0, c.result)

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
		c.Solve()
		self.assertEqual(['a','b'], c.unknowns)
		self.assertEqual(22, c.result)

	def testCalc_ab_22_scaled(self):
		c = Calculator('13*a_2+551*b_3=4460')
		c.Solve()
		self.assertEqual(['a','b'], c.unknowns)
		self.assertEqual(22, c.result)

	def testCalc_ab_98(self):
		c = Calculator('13*a_2+551*b_3=283165')
		c.Solve()
		self.assertEqual(['a','b'], c.unknowns)
		self.assertEqual(98, c.result)

if __name__ == '__main__':
	unittest.main()
	
