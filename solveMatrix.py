import re

import sympy
import matrix 

units = range(0, 10)
squares = [x**2 for x in range(0, 10)]
cubes = [x**3 for x in range(0, 10)]

def _sortedCoeffs(unknowns, coeffs):
    keys = unknowns
    print "ks = ",keys
    keys.sort()
    return map(coeffs.get, keys)
    
def SolveMatrix(raw_unknowns, unknowns, coeffs, sumTotal):
    print "Matrix solution"
    
    # print "unknowns: ",unknowns
    # print "raw_unknowns: ",raw_unknowns
    # print "coeffs: ", coeffs
    
    a_t = sympy.Matrix(_sortedCoeffs(unknowns, coeffs))        
    a_tI = matrix.appendIdentity(a_t)
    # print "a_tI = \n",a_tI
    
    RTfrac = a_tI.rref()[0]
    # print "RTFrac = \n",RTfrac
    Rf = RTfrac[:,0]
    Tf = RTfrac[:,1:]
    Tf_t = Tf.transpose()
    
    RT = matrix.unimod(a_tI)
    R = RT[:,0]        
    T = RT[:,1:]
    # print "T = \n",T
    R_t = R.transpose()
    T_t = T.transpose()
    print "T_t = \n",T_t
            
    k_symbols = []
    for i in range(0, len(R)):
        k_symbols.append(sympy.Symbol('k_%d'%i))            
    K = sympy.Matrix(k_symbols)
    
    R_txK = R_t * K
    if R_txK.shape != (1,1):
        raise TypeError('expected 1x1')
    
    K[0] = sumTotal
    
    unknowns = T_t * K
    # print "unknowns values: \n", unknowns
    
    unknowns_f = Tf_t * K
    print "unknowns _frac values: \n", unknowns_f                        
    
    def fn(K):
        t = str(unknowns_f[-1])
        func = re.sub(r'k_([0-9])', r'K[\1]', t)
        return eval(func)
    
    
    print "fn = \n",fn(K)        
    
    print unknowns
    print units 
    print squares 
    print cubes 

    return "Blee"