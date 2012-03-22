import unittest

from number_base import BaseCalc

class NumberBaseTests(unittest.TestCase):
    def testParse(self):
        sut = BaseCalc('[1234]10]')
        self.assertEqual('1234', sut.input_value)
        self.assertEqual(10, sut.base)        
    
    def testParseFormatFail(self):        
        with self.assertRaises(ValueError):
            sut = BaseCalc('1234')
            
if __name__ == '__main__':
    unittest.main()
    
