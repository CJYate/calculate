import fractions 
import sympy 

def getLhs(matrix):
    return matrix[:,0]    
    
def calculateGcd(matrix):
    lhs = getLhs(matrix)
    l = len(lhs)    
    if l == 0:
        return 0
    if l == 1: 
        return abs(lhs[0])
    if l == 2:	
        return fractions.gcd(abs(lhs[1]), abs(lhs[0]))
    else:
        gcd = fractions.gcd(abs(lhs[1]), abs(lhs[0]))
        for i in range(2, l):
            gcd = fractions.gcd(gcd, abs(lhs[i]))
        return gcd

        
def isLhsJustGcd(gcd, matrix):
    lhs = getLhs(matrix)
    print lhs
    nonzeros = [x for x in lhs if x != 0]    
    if len(nonzeros) > 1:        
        return False
    if len(nonzeros) == 0:        
        return False
    return nonzeros[0] == gcd
    
    
def appendIdentity(matrix):
    s = matrix.shape
    matrixT = matrix
    size = max(s[0], s[1])
    if s[0] < s[1]:
        matrixT = matrix.transpose()
    return matrixT.row_join(sympy.eye(size))

def findMinRow(matrix):            
    lhs = getLhs(matrix)
    
    minRow = 0
    minRowVal = 0
    for i in range(0, len(lhs)):
        if lhs[i] != 0:
            if minRowVal == 0:
                minRowVal = lhs[i]
                minRow = i
            else:
                if lhs[i] < minRowVal:
                    minRow = i
    
    return minRow

def sort(matrix):
    # sort    
    (h,w) = matrix.shape

    for t in range(1,h):        
        for y in range(1,h):            
            for x in range(0, w):
                if matrix[y-1,x] > matrix[y,x]:
                    #   already correct
                    break;
                if matrix[y-1,x] < matrix[y,x]:
                    matrix.row_swap(y-1,y)    
                    break;
                     
    return matrix

def unimod(matrix, eps = 1.0/(10**10)):
    """ matrix to reduced row echelon
    """
    (h,w) = matrix.shape
    
    lhs = getLhs(matrix)
    gcd = calculateGcd(lhs)

    while not isLhsJustGcd(gcd, matrix):        
        print "top of loop\n",matrix
        
        for y in range(0,h):
            # if the leftmost item is negative, negate the whole row
            if matrix[y,0] < 0:
                matrix[y,:] = -matrix[y,:]
        print "removed negatives"                              
         
        minRow = findMinRow(matrix)
        
        for y2 in range(0, h): # eliminate y           
            if y2 == minRow:
                continue
            print "reducing row ",y2
            if matrix[y2,0] == 0:
                continue
                
            c = int(matrix[y2,0] / matrix[minRow,0])
            print "row(%d) -> row(%d) - %d * row(%d)"%(y2, y2, c, minRow)
            matrix.row(y2, lambda v, x: v-c*matrix[minRow, x])               
        print matrix

        matrix = sort(matrix)
        
        print "end of loop\n",matrix    
    return matrix
