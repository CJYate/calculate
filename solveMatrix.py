import re
import string
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
    
def _invertMatrix(unknowns, coeffs):
    a_t = sympy.Matrix(_sortedCoeffs(unknowns, coeffs))        
    a_tI = matrix.appendIdentity(a_t)
        
    RT = matrix.unimod(a_tI)
    R = RT[:,0]        
    T = RT[:,1:]
    R_t = R.transpose()
    T_t = T.transpose()
            
    k_symbols = []
    for i in range(0, len(R)):
        k_symbols.append(sympy.Symbol('k_%d'%i))            
    K = sympy.Matrix(k_symbols)
    
    R_txK = R_t * K
    if R_txK.shape != (1,1):
        raise TypeError('expected 1x1')
    
    # K[0] = sumTotal   
    
    unknownsMatrix = T_t * K
    return unknownsMatrix

def _getTerms(unknownsMatrix, unknowns):
    unknownTerms = []
    assert(len(unknownsMatrix) == len(unknowns))
    
    for i in range(0, len(unknowns)):
        us = str(unknownsMatrix[i])
        us2 = us.replace(' - ', ' + -')
        us3 = re.sub(r'k_([0-9])', r'K[\1]', us2)
        us_split = us3.split(' + ')
        
        unknownTerms.append((unknowns[i], us_split))
            
    return unknownTerms

def _getKterm(term, unknown):
    
    mK = re.match('(\-?[0-9]*)\*?(K\[[0-9]\])', term)
    if mK:
        ti = mK.group(1)
        if ti == '-':
            ti = '-1'
        elif ti == '':
            ti = '1'
        kCoeff = int(ti)
        kTerm = mK.group(2)
        if kCoeff == 1:
            return (unknown, kTerm)
        elif kCoeff == 1:
            return (unknown, -kTerm)
        else:
                return (unknown, kCoeff * kTerm)


def _findUValue(unknown, value):
    tt = unknown.split("_")
    unknownVar = tt[0]
    unknownExp = tt[1]
    list = { '1' : units, '2' : squares, '3' : cubes }[unknownExp]
    print "searching for value %d for var %s in list: " \
                            %(value,unknown),list
    if value in list:
        indexOfValue = list.index(value)
        print "%s = %d"%(unknownVar,indexOfValue)
        return (True, unknownVar, indexOfValue)
    else:
        return (False)

def SolveMatrix(raw_unknowns, unknowns, coeffs, sumTotal):

    print "Matrix solution"

    unknownsMatrix = _invertMatrix(unknowns, coeffs)

    print "unknowns matrix: \n", unknownsMatrix

    unknownTerms = _getTerms(unknownsMatrix, unknowns)
        
    knowns = {}
    iterable = {}

    for i in range(0, len(unknowns)):    
        ut = unknownTerms[i]
        print "dealing with term %s",ut

        if len(ut) == 1:
            # probably just a value of k... 
            # so this k directly equals a value a^[123]
            # and we are probably going to need to iterate over it        
            iterable.append(_getKterm())


        if len(ut) == 2:            
            # we have a great chance at solving this part. 
            # It should be in the form Ak[i], B. 
            # And will equal x^[123] where 0 <= x <= 9
            
            kTerm = ''
            kCoeff = 0
            scalar = 0
                
            for t in ut[1]:                                
                mK = re.match('(\-?[0-9]*)\*?(K\[[0-9]\])', t)
                mS = re.match('-?[0-9]+', t)
                
                if mK:                
                    kTerm = _getKterm()
                elif mS:
                    scalar = int(t)

                
            print "%d * %s + %d = %s"%(kCoeff, kTerm, scalar, unknowns[i])
          
            if kTerm in knowns:
                kTermValue = knowns[kTerm]
            else:
                kTermValue = scalar // kCoeff
                knowns[kTerm] = kTermValue
                
            uValue = abs(scalar - kCoeff * kTermValue )                                    
            
            temp = _findUValue(unknowns[i], uValue)
            if temp[0] == True:
                print "found something :",temp
            else:
                print "NOOOOOOOO!!! Could not find %d in expected list." \
                        " Try something else..."%uValue

    print "known things:\n",knowns
    solution = ''
    for c in string.ascii_lowercase:
        #st = '%c'%c
        if c in knowns:
               solution = solution + str(knowns[c])
    
    print "returning solution ",solution
    print
    print
    return solution
