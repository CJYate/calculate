import sys

UNITS = range(0, 10)
SQUARES = [x**2 for x in range(0, 10)]
CUBES = [x**3 for x in range(0, 10)]


def _sorted_coeffs(unknowns, coeffs):
    """ Sort coefficients by their terms, alphabetically
    """
    keys = unknowns    
    keys.sort()
    return map(coeffs.get, keys)

def _calc(size, functions, soln, expected):
    temp = 0
    for i in range(0, size):
        index = chr(ord('a') + i)
        print "calculating for index %s " % index
        lambdas = functions[index]
        
        for lam in lambdas:
            res = lam(soln[i])
            print "result = %s" % res
            temp = temp + res
       
    print "%s -> %s" % (soln, temp)
    diff = abs(expected - temp)
#    print "diff between exp = %i and value %i = %i" % (expected, temp, diff)
    return diff

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
                new_diff = _calc(size, functions, soln, expected)
#                print "diff = %i new_diff = %i" % (diff, new_diff)
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
    return soln



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
    def __init__(self, coeff, expo):
        self.coeff = coeff
        self.expo = expo

    def __call__(self, x):
        return self.coeff * x ** self.expo

def SolveGrind(raw_unknowns, unknowns, coeffs, negTotal):        

    sumTotal = -negTotal
    
    print "solve brute force - raw unknow = %s\n unknonw = %s\n coeffs = %s, sum = %s " \
            % (raw_unknowns, unknowns, coeffs, sumTotal)

    problem_size = len(raw_unknowns)

    functions = {}

    expressions_by_unknown = {}
     
    for raw in raw_unknowns:
        expressions_by_unknown[raw] = [];

    for k,v in coeffs.iteritems():        
#        print k, v
        unknown = k[0]
        exponential = k[1]
        multiplier = v

        expressions_by_unknown[unknown].append((multiplier, exponential))

#         if exponential == 1:
#             expressions_by_unknown[unknown].append('%i * x' % (multiplier))
#         elif exponential == 2:
#             expressions_by_unknown[unknown].append('%i * x * x' % (multiplier))
#         elif exponential == 3:
#             expressions_by_unknown[unknown].append('%i * x * x * x' % (multiplier))                    
# 
#    full_expressions_by_unknown = {}

    for raw in raw_unknowns:
        print "defining function for %s: " % raw

        expressions = expressions_by_unknown[raw]

#        lambdas = [] 
        funcs = []

        for expr in expressions:
            print "creating lambda for %i * x^%i " % (expr[0], expr[1])
            f = func(expr[0], expr[1])
            funcs.append(f)
#            lambdas.append(lambda x = soln[i]: expr[0] * x ** expr[1])
#            lambdas.append(lambda x : sys.stdout.write('%s: %i * x^%i ' \
#                    % (raw, expr[0], expr[1])))
            

        functions[raw] = funcs 
    
    count = _try(functions, negTotal)
    stringResult = str(count).zfill(problem_size)
    print "result from grind = ", stringResult
    return stringResult
