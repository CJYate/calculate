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
    
def SolveMatrix(raw_unknowns, unknowns, coeffs, sumTotal):
    print "Matrix solution"
    
    # print "unknowns: ",unknowns
    # print "raw_unknowns: ",raw_unknowns
    # print "coeffs: ", coeffs
    
    a_t = sympy.Matrix(_sortedCoeffs(unknowns, coeffs))        
    a_tI = matrix.appendIdentity(a_t)
    # print "a_tI = \n",a_tI
        
    RT = matrix.unimod(a_tI)
    R = RT[:,0]        
    T = RT[:,1:]
    # print "T = \n",T
    R_t = R.transpose()
    T_t = T.transpose()
    #print "T_t = \n",T_t
            
    k_symbols = []
    for i in range(0, len(R)):
        k_symbols.append(sympy.Symbol('k_%d'%i))            
    K = sympy.Matrix(k_symbols)
    
    R_txK = R_t * K
    if R_txK.shape != (1,1):
        raise TypeError('expected 1x1')
    
    # # >?!    
    # if sumTotal < 0:
        # print " negtating negative sumTotal WARNING!"
        # sumTotal = -sumTotal
    K[0] = sumTotal   
    print "K[0] = %d"%(K[0])
    
    unknownsMatrix = T_t * K
    print "unknowns matrix: \n", unknownsMatrix

    unknownTerms = []
    
    assert(len(unknownsMatrix) == len(unknowns))
    
    for i in range(0, len(unknowns)):
        us = str(unknownsMatrix[i])
        us2 = us.replace(' - ', ' + -')
        us3 = re.sub(r'k_([0-9])', r'K[\1]', us2)
        us_split = us3.split(' + ')
        
        unknownTerms.append((unknowns[i], us_split))
            
    print unknownTerms
        
    knowns = {}
    
    for i in range(0, len(unknowns)):    
        ut = unknownTerms[i]
        print "dealing with term %s",ut

        if len(ut) == 2:            
            # we have a great chance at solving this part. It should be in the form Ak[i] , B. And will equal x^[123] where 0 <= x <= 9
            
            kTerm = ''
            kCoeff = 0
            scalar = 0
                
            nScalarTerms = 0
            nKterms = 0
            
            #if len(ut[1]) == 2:#we expect a k part and a scalar part 
            for t in ut[1]:                                
                mK = re.match('(\-?[0-9]*)\*?(K\[[0-9]\])', t)
                mS = re.match('-?[0-9]+', t)
                
                if mK:                
                    nKterms = nKterms + 1
                    
                    ti = mK.group(1)
                    if ti == '-':
                        ti = '-1'
                    elif ti == '':
                        ti = '1'
                    kCoeff = int(ti)
                    kTerm = mK.group(2)
                                     
                elif mS:
                    #print "is a scalar term"
                    nScalarTerms = nScalarTerms + 1
                    scalar = int(t)
                    #print "scalar = ",scalar
                        
              #  assert(nScalarTerms == 1)
               # assert(nKterms == 1)
                
            print "%d * %s + %d = %s"%(kCoeff, kTerm, scalar, unknowns[i])
          
            if kTerm in knowns:
                kTermValue = knowns[kTerm]
            else:
                kTermValue = scalar // kCoeff
                knowns[kTerm] = kTermValue
                
            #print "%s = %d"%(kTerm, kTermValue)
                        
            uValue = abs(scalar - kCoeff * kTermValue )                                    
            #print "%s = %d"%(unknowns[i], uValue)
                        
            tt = unknowns[i].split("_")
            unknownVar = tt[0]
            unknownExp = tt[1]
            #print "%s ^ %s..."%( unknownVar, unknownExp)
            list = {
                '1' : units,
                '2' : squares,
                '3' : cubes
            }[unknownExp]
            print "searching for value %d for var %s in list: "%(uValue,unknowns[i]),list
            if uValue in list:
                indexOfValue = list.index(uValue)
                print "%s = %d"%(unknownVar,indexOfValue)
                knowns[unknownVar] = indexOfValue                
            else:
                print "NOOOOOOOO!!! Could not find %d in expected list. Try something else..."%uValue
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
    
def FunctionForRref():
    
    def fn(K):
        # get unknowns bottom line
        t = str(unknownsMatrix[-1])
        print t
        # replace k_n with K[n] (the variable name)
        t2 = re.sub(r'k_([0-9])', r'K[\1]', t)
        print t2
        # make all terms additive and explicitly make coefficients negative
        t3 = t2.replace(' - ', ' + -')
        print t3
        
        terms = t3.split(' + ')
        print terms
        # find the denominator underneath each fraction
        greatestDenominator = 1        
        for tt in terms:
                s = tt.split('/')
                if len(s) == 2:
                    d = int(s[1])
                    if d > greatestDenominator:
                        greatestDenominator = d
        # recreate terms with this denominator multiplying through; also multiply through with the result of the equation 
        terms2 = []
        for tt in terms:
            terms2.append('%d*(%s)'%(greatestDenominator,tt)) 
        #K[0] = greatestDenominator * K[0]
        print terms2
        func = ''#'K[0] + '
        func = func + ' + '.join(terms2)
        # print "func = ",func
        return eval(func)    
    
    print "fn = :\n",fn(K)        
        