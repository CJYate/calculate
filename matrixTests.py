import unittest
import matrix
import sympy

class MatrixTest(unittest.TestCase):
    def testIdentity(self):		
        m = matrix.unimod(sympy.eye(3))
        self.assertEqual(sympy.eye(3), m)
        
    def testGcd(self):
        m = sympy.Matrix([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
        gcd = matrix.calculateGcd(m)
        exp = 1
        self.assertEqual(exp, gcd)
        
    def testGcd2(self):
        m = sympy.Matrix([[2,6,12,26]])
        m2 = matrix.appendIdentity(m)
        gcd = matrix.calculateGcd(m2)
        exp = 2
        self.assertEqual(exp, gcd)
        
    def testGetLHS(self):
        m = sympy.Matrix([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
        lhs = matrix.getLhs(m)
        exp = sympy.Matrix([[1],[5],[9],[13]])
        self.assertEqual(exp, lhs)        
        
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

    def testUnimod3x3(self):
        m = sympy.Matrix([9, 5, 17])
        m2 = matrix.appendIdentity(m)
        m3 = matrix.unimod(m2)
        exp = sympy.Matrix([[1,0,7,-2],[0,1,5,-2],[0,0,-17, 5]])
        self.assertEqual(exp, m3)
    
    def testUnimod3x3_2(self):
        m = sympy.Matrix([15,21,35])
        m2 = matrix.appendIdentity(m)
        m3 = matrix.unimod(m2)
        exp = sympy.Matrix([[1,1,1,-1],[0,7,0,-3],[0,-7,-5,6]])
        self.assertEqual(exp, m3)
        
    def testUnimod8x8(self):
        m = sympy.Matrix([865, 4831, -6700, 7496, 8474, 2851, -5451])
        m2 = matrix.appendIdentity(m)
        m3 = matrix.unimod(m2)
        exp = sympy.Matrix([[1, 150, 0, 0,0,0,52,51],
        [0,148,1,0,0,0,49,50],
        [0,-198,0,0,0,1,-71,-67],
        [0,-233,0,0,0,0,-88,-83],
        [0,-373,0,-1,0,0,-132,-127],
        [0,-566,0,0,1,0,-198,-192],
        [0,-753,0,0,0,0,-261,-256]])
        
        self.assertEqual(exp, m3)
        
    def testFindMinRow(self):
        m = sympy.Matrix([[0, 1, 2],[1, 1, 2],[2, 1, 2]])
        expected = 1
        self.assertEqual(expected, matrix.findMinRow(m))
        
    def testFindMinRow2(self):
        m = sympy.Matrix([[1, 1, 2],[1, 1, 2],[2, 1, 2]])
        expected = 0
        self.assertEqual(expected, matrix.findMinRow(m))
            
    def testFindMinRow3(self):
        m = sympy.Matrix([[3, 1, 2],[4, 1, 2],[2, 1, 2]])
        expected = 2
        self.assertEqual(expected, matrix.findMinRow(m))
    
    def testSort1(self):
        m = sympy.Matrix([[3, 1, 2],[4, 1, 2],[2, 1, 2]])
        exp = sympy.Matrix([[4, 1, 2],[3, 1, 2],[2, 1, 2]])        
        self.assertEqual(exp, matrix.sort(m))
                                
    def testSort2(self):
        m = sympy.Matrix([[0,0,0],[0,1,1],[1,0,0]])
        exp = sympy.Matrix([[1,0,0],[0,1,1],[0,0,0]])        
        self.assertEqual(exp, matrix.sort(m))
                
        
if __name__ == '__main__':
    unittest.main()
