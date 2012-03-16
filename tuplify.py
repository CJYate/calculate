import re

def Tuplify(expression, negate = False):
# turn things like 224242*a**2 into a tuple (coeff, symbol, exponent)
    coeff = 0
    symbol = ''
    exponent = 0

    if "**" in expression: #(expected true apart from the scalar)
        t = expression.split("**")
        exponent = int(t[1])
        if "*" in t[0]:
            t2 = t[0].split("*")
            coeff = int(t2[0])
            symbol = t2[1]
        else:
            if t[0][0] == '-':
                coeff = -1
            else:
                coeff = 1
            symbol = t[0][1::]
    elif "*" in expression:
        t = expression.split("*")
        coeff = int(t[0])
        symbol = t[1]
        exponent = 1 
    else:
        if re.search("[a-z]", expression):
            if expression[0] == '-':
                coeff = -1
            else: 
                coeff = 1
            
            symbol = expression[0::]
            exponent = 1
        else:
            coeff = int(expression)

    if negate:
        return (-coeff, symbol, exponent) 
    else:
        return (coeff, symbol, exponent) 
