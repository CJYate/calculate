import sys
import itertools
import timeit

UNITS = range(0, 10)
SQUARES = [x**2 for x in range(0, 10)]
CUBES = [x**3 for x in range(0, 10)]


def _sorted_coeffs(unknowns, coeffs):
    """ Sort coefficients by their terms, alphabetically
    """
    keys = unknowns    
    keys.sort()
    return map(coeffs.get, keys)

def _calc(size, functions, soln):
    temp = 0
    for i in range(0, size):
        index = chr(ord('a') + i)
        
        func = functions[index]
        
        #for func in funcs:
        res = func(soln[i])
       
        temp = temp + res
       
    return temp

    
def _try_all(functions, expected):
    size = len(functions)
    
    ans = ''
    p = itertools.product(range(10), repeat = size)
    
    for soln in list(p):
    
        result = _calc(size, functions, soln)
        #print "soln %s res %s, exp %s " % ( soln, result, expected )
        if expected == result:
            #print "solution found at %s" % 
            ans = ''.join(map(str, soln))
            break        
    return ans

    
def _try(functions, expected):
    size = len(functions)
    soln = [5] * size
    
#    print "initial soln = ",soln
    diff = expected
    while diff > 0:
        for i in range(0, size):
            best = soln[i]
            for x in range(0, 10):
                soln[i] = x
                trial_sum = _calc(size, functions, soln)
                new_diff = abs(expected - trial_sum)
                #print "diff = %i new_diff = %i" % (diff, new_diff)
                if new_diff < diff:                    
#                    print "new best value for pos %i = %i " % (i, x)
                    diff = new_diff
                    best = x

#                print "diff = ", diff
#                print "current soln = ",soln
            soln[i] = best

#             if soln[i] > 0 and soln[i] < 9:
#                 soln[i] = soln[i] - 1
#                 down_diff = _calc(size, functions, soln, expected)
#                 soln[i] = soln[i] + 2
#                 up_diff = _calc(size, functions, soln, expected)
#                 soln[i] = soln[i] - 1
#         
#                 if up_diff < diff:
#                     soln[i] = soln[i] + 1
#                     diff = up_diff
#                 elif down_diff < diff: 
#                     soln[i] = soln[i] - 1
#                     diff = down_diff
# 
#             elif soln[i] == 0:
#                 soln[i] = soln[i] + 1
#                 new_diff = _calc(size, functions, soln, expected)
#                 soln[i] = soln[i] - 1
#                 if new_diff < diff:
#                     soln[i] = soln[i] + 1
#                     diff = new_diff
#             elif soln[i] == 9:
#                 soln[i] = soln[i] - 1
#                 new_diff = _calc(size, functions, soln, expected)
#                 soln[i] = soln[i] + 1
#                 if new_diff < diff:
#                     soln[i] = soln[i] - 1
#                     diff = new_diff
#                 
#        print "diff = ", diff
#        print "current soln = ",soln
    return ''.join(map(str, soln))


def _try_best(functions, expected):
    size = len(functions)
    soln = [0] * size
    
    diff = expected
    while diff > 0:
        for i in range(0, size):
            best_i = soln[i]
            # try to improve i
            for x in range(0, 10):
                soln[i] = x
                
                print "diff = ", diff
                print "current soln = ",soln

                trial_sum = _calc(size, functions, soln)                
                new_diff = abs(expected - trial_sum)    
                                
                print "new_diff = ", new_diff
                if new_diff < diff:                    
                    diff = new_diff
                    best_i = x
                    print "new best_i = ", best_i

#                print "diff = ", diff
#                print "current soln = ",soln
            soln[i] = best_i

#             if soln[i] > 0 and soln[i] < 9:
#                 soln[i] = soln[i] - 1
#                 down_diff = _calc(size, functions, soln, expected)
#                 soln[i] = soln[i] + 2
#                 up_diff = _calc(size, functions, soln, expected)
#                 soln[i] = soln[i] - 1
#         
#                 if up_diff < diff:
#                     soln[i] = soln[i] + 1
#                     diff = up_diff
#                 elif down_diff < diff: 
#                     soln[i] = soln[i] - 1
#                     diff = down_diff
# 
#             elif soln[i] == 0:
#                 soln[i] = soln[i] + 1
#                 new_diff = _calc(size, functions, soln, expected)
#                 soln[i] = soln[i] - 1
#                 if new_diff < diff:
#                     soln[i] = soln[i] + 1
#                     diff = new_diff
#             elif soln[i] == 9:
#                 soln[i] = soln[i] - 1
#                 new_diff = _calc(size, functions, soln, expected)
#                 soln[i] = soln[i] + 1
#                 if new_diff < diff:
#                     soln[i] = soln[i] - 1
#                     diff = new_diff
#                 
        print "diff = ", diff
        print "current soln = ",soln
    return ''.join(map(str, soln))



def _trial(functions, trial_value, expTotal):
    assert(len(functions) == len(trial_value))
    value = 0
    for i in range(0, len(functions)):
        value = value + functions[i](trial_value[i])
    #print "expected %i value = %i" % (expTotal, value)
    return expTotal == value
    #print "functions=\n%s\ntrial value = %s" % (functions, trial_value)

#    return eval(expression) 

class func(object):
    def __init__(self, coeffs, expos):
        self.coeffs = coeffs
        self.expos = expos
        self.size = len(coeffs)
        assert(len(coeffs) == len(expos))
        
    def __call__(self, x):
        val = 0
        for i in range(0, self.size):
            val = val + self.coeffs[i] * x ** self.expos[i]
        return val
        

def SolveGrind(raw_unknowns, unknowns, coeffs, sumTotal):        

    timer = timeit.Timer()
    
    print "solve brute force - raw unknow = %s\n unknonw = %s\n coeffs = %s, sum = %s " \
            % (raw_unknowns, unknowns, coeffs, sumTotal)
    
    problem_size = len(raw_unknowns)

    functions = {}

    expressions_by_unknown = {}
     
    for raw in raw_unknowns:
        expressions_by_unknown[raw] = [];

    for k,v in coeffs.iteritems():        
        unknown = k[0]
        exponential = k[1]
        multiplier = v

        expressions_by_unknown[unknown].append((multiplier, exponential))

    for raw in raw_unknowns:

        expressions = expressions_by_unknown[raw]

        coeffs = [expr[0] for expr in expressions]
        expos = [expr[1] for expr in expressions]

        functions[raw] = func(coeffs, expos)        

    negTotal = -sumTotal    
    count = _try_all(functions, negTotal)
    stringResult = str(count).zfill(problem_size)
    print "result from grind = ", stringResult
    print timer.timeit()
    return stringResult
