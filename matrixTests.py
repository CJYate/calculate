import unittest
import matrix
import sympy

class MatrixTest(unittest.TestCase):
	def testIdentity(self):		
		m = matrix.unimod(sympy.eye(3))
		self.assertEqual(sympy.eye(3), m)

	def testAppend2x2(self):
		m = sympy.Matrix([5,9])
		m2 = matrix.appendIdentity(m)
		exp = sympy.Matrix([[5,1,0],[9,0,1]])
		self.assertEqual(exp, m2)

	def testUnimod2x2(self):
		m = sympy.Matrix([9, 5])
		m2 = matrix.appendIdentity(m)
		m3 = matrix.unimod(m2)
		exp = sympy.Matrix([[1,-1,2],[0,5,-9]])
		self.assertEqual(exp, m3)

if __name__ == '__main__':
	unittest.main()
