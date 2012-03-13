import fractions 

def getLhs(m, h, w):
    lhs = []
    for i in range(0, h):
        lhs.append(m[i][0])
    return lhs


def calculateGcd(lhs):
    l = len(lhs)
    if l == 0:
        return 0
    if l == 1: 
        return lhs[0]
    if l == 2:    
        return fractions.gcd(lhs[1], lhs[0])
    else:
        gcd = lhs[0]
        for i in range(1,l):
            gcd = fractions.gcd(gcd, lhs[i])
        return gcd


def isLhsJustGcd(gcd, m, h, w):
    lhs = getLhs(m, h, w)
    nonzeros = [x for x in  lhs if x != 0]
    if len(nonzeros) > 1:
        return False
    if len(nonzeros) == 0:
        return False
    return nonzeros[0] == gcd


def unimod(m, eps = 1.0/(10**10)):
    """ matrix to reduced row echelon
    """
    (h,w) = (len(m), len(m[0]))

    lhs = getLhs(m, h, w)
    gcd = calculateGcd(lhs)
    
    while not isLhsJustGcd(gcd, m,h,w):
        minrow = 0
        for y in range(1, h): 
            if m[y][0] != 0 and m[y][0] < m[minrow][0]:
                minrow = y
        (m[0], m[minrow]) = (m[minrow], m[0]) # swap
        
        for y2 in range(1, h): # eliminate y
            if m[0][0] == 0:
                continue
            c = int(m[y2][0] / m[0][0])
            for x in range(0,w):
                m[y2][x] = m[y2][x] - (m[0][x] * c)

        for y in range(0,h):
            if m[y][0] < 0:
                for x in range(0, w):
                    m[y][x] = -m[y][x]
    return True
