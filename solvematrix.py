import re
from string import ascii_lowercase

import sympy

import matrix

UNITS = range(0, 10)
SQUARES = [x ** 2 for x in range(0, 10)]
CUBES = [x ** 3 for x in range(0, 10)]


def _sorted_coeffs(unknowns, coeffs):
    """ Sort coefficients by their terms, alphabetically
    """
    keys = unknowns
    print "ks = ", keys
    keys.sort()
    return map(coeffs.get, keys)


def _k_symbols(size):
    """ Create an array of sympy symbols for each k
    """
    
    k_symbols = []
    for i in range(0, size):
        k_symbols.append(sympy.Symbol('k_%d' % i))
    return k_symbols


def _invert_matrix(unknowns, coeffs, k_symbols):
    """ Invert the matrix by unimodular row reduction
    """

    a_transpose = sympy.Matrix(_sorted_coeffs(unknowns, coeffs))
    a_transpose_augmented = matrix.appendIdentity(a_transpose)

    r_t = matrix.unimod(a_transpose_augmented)
    r = r_t[:, 0]
    t = r_t[:, 1:]
    r_transpose = r.transpose()
    t_transpose = t.transpose()

    K = sympy.Matrix(k_symbols)

    r_transpose_K = r_transpose * K
    if r_transpose_K.shape != (1, 1):
        raise TypeError('expected 1x1')

    unknownsMatrix = t_transpose * K
    print "Unknowns:\n%s\nK:\n%s" % (unknownsMatrix, K)

    return unknownsMatrix


def _get_terms(unknownsMatrix, unknowns):
    """ Get all the 'k' terms in the input matrix    
    """
    
    unknownTerms = []
    assert(len(unknownsMatrix) == len(unknowns))

    for i in range(0, len(unknowns)):
        us = str(unknownsMatrix[i])
        us2 = us.replace(' - ', ' + -')
        us3 = re.sub(r'k_([0-9])', r'K[\1]', us2)
        us_split = us3.split(' + ')

        unknownTerms.append((unknowns[i], us_split))

    return unknownTerms


def _get_k_term(term):
    """ get the k term from a term with coeffecients
    """
    
    matches_for_k = re.match('(\-?[0-9]*)\*?(K\[[0-9]\])', term)
    if matches_for_k:
        temp_match1 = matches_for_k.group(1)
        if temp_match1 == '-':
            temp_match1 = '-1'
        elif temp_match1 == '':
            temp_match1 = '1'
        kCoeff = int(temp_match1)
        kTerm = matches_for_k.group(2)

        return (kCoeff, kTerm)


def _findUnknownValue(knowns, iterables, non_iterables):
    """ iterate through values etc to find a valid solution
    """
    
    
#    for unknown in non_iterables.keys():
#        split_temp = unknown.split("_")
#        unknown_var = split_temp[0]
#        unknown_exponential = split_temp[1]
#        values_list = {'1': UNITS, '2': SQUARES, '3': CUBES}[unknown_exponential]
#        print "searching for value %d for var %s in values_list: " \
#                                % (value, unknown), values_list
#        if value in values_list:
#            indexOfValue = values_list.index(value)
#            print "%s = %d" % (unknown_var, indexOfValue)
#            return (True, unknown_var, indexOfValue)
#        else:
#            return (False, unknown_var)


def SolveMatrix(raw_unknowns, unknowns, coeffs, sumTotal):
    print " ** Matrix solution ** "

    k_symbols = _k_symbols(len(unknowns))
    k_symbols[0] = sumTotal

    unknowns_matrix = _invert_matrix(unknowns, coeffs, k_symbols)

    unknown_terms = _get_terms(unknowns_matrix, unknowns)

    knowns = {}

    knowns['K[0]'] = sumTotal

    iterables = {}
    non_iterables = {}

    for i in range(0, len(unknowns)):
        unknown_term = unknown_terms[i]
        print "dealing with term", unknown_term
        unknown_part = unknown_term[0]
        value_parts = unknown_term[1]
        print "%s = %s" % (unknown_part, value_parts)
        n_unknown_value_terms = len(value_parts)

        if n_unknown_value_terms == 1:
            # probably just a value of k...
            # so this k directly equals a value a^[123]
            # and we are probably going to need to iterate over it
            k_term = _get_k_term(value_parts[0])
            iterables[unknown_part] = k_term[1]
            print "iterables = ", iterables

        else:
            # we have a great chance at solving this part.
            # It should be in the form Ak[i], B.
            # And will equal x^[123] where 0 <= x <= 9

            k_term = ''
            k_coeff = 0
            scalar = 0

            for term in unknown_term[1]:
                mK = re.match('(\-?[0-9]*)\*?(K\[[0-9]\])', term)
                mS = re.match('-?[0-9]+', term)

                if mK:
                    k_coeff, k_term = _get_k_term(term)
                elif mS:
                    scalar = int(term)

            print "%d * %s + %d = %s" % (k_coeff, k_term, scalar, unknowns[i])

#            if k_term in knowns:
#                k_term_value = knowns[k_term]
#                print "knew %s already, = %s" % (k_term, k_term_value)
#            else:
#                k_term_value = scalar // k_coeff
#                knowns[k_term] = k_term_value
#                print "saved new value %s = %s" % (k_term, k_term_value)
#             unknown_value = abs(scalar - k_coeff * k_term)
            non_iterables[unknown_part] = value_parts

#for unknown in unknowns:
#   temp =

    _findUnknownValue(knowns, iterables, non_iterables)

# if temp[0] == True:
            #print "found something :", temp
        #else:
            #print "NOOOOOOOO!!! Could not find %d in expected list." \
#" Try something else..." % unknown_value

    print "known things:\n", knowns
    solution = ''
    for char in ascii_lowercase:
        #st = '%char'%char
        if char in knowns:
            solution = solution + str(knowns[char])

    print "returning solution ", solution
    print
    print
    return solution
