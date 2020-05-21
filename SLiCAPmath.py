#!/usr/bin/python2.7
from SLiCAPyacc import *

class matrix(sp.Matrix):
    """SLiCAP matrix class for faster symbolic calculations.
    return types for matrices are <class 'sympy.matrices.matrices.Matrix'>."""
    def __init__(self, M):
        pass
    
    def minor(self, i, j):
        # Returns determinant of M after deleting row i and column j
        return matrix(self.minorMatrix(i, j)).determinant()

    def coFactor(self, i, j):
        # Returns cofactor C(i,j) 
        if (i + j)%2 == 0:
            return self.minor(i, j)
        else:
            return -self.minor(i, j)

    def determinant(self):
        # Returns determinant calculated by expansion of minors
        # No multiplication with zero
        d = 0
        """
        if self.shape[0] != self.shape[1]:
            print 'Non square matrix'
            return
        """
        if self.shape[0] == 2:
            if self[0,0] != 0 and self[1,1] != 0:
                d += self[0,0]*self[1,1]
            if self[1,0] != 0 and self[0,1] != 0:
                d -= self[0,1]*self[1,0]
            return d
        return sp.expand(self.expandByMinors())

    def expandByMinors(self):
        """ Calculates determinant by expansion of minors.
        No multiplications with zero"""
        d = 0
        for col in range(self.shape[1]):
            if self[0, col] != 0:                
                if col%2 == 0:
                    d += self[0,col]*self.minor(0 , col)
                else:
                    d -= self[0,col]*self.minor(0 , col)
        return d
                    
    def coFactorMatrix(self):
        # Returns cofactor matrix of M
        """
        if self.shape[0] != self.shape[1]:
            print 'Non square matrix'
            return
        """
        C = sp.zeros(self.shape[0])
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                C[i,j] = self.coFactor(i, j)
        return C

    def adjugate(self):
        # Returns adjugate matrix of M
        return self.coFactorMatrix().transpose()

    def inverse(self):
        # Returns inverse matrix of M
        return self.adjugate()/self.determinant()

    def dotV(self, Vr, Vc):
        """Returns inner product of row vector Vr and column vector Vc.
        No multiplications with zero or +/- unity."""
        s1 = Vr.shape
        result = 0
        for i in range(s1[1]):
            if Vr[i] == 0 or Vc[i] == 0:
                pass
            elif Vr[i] == 1:
                result += Vc[i]
            elif Vc[i] == 1:
                result += Vr[i]
            elif Vr[i] == -1:
                result += -Vc[i]
            elif Vc[i] == -1:
                result += -Vr[i]
            else:
                result += Vr[i]*Vc[i]
        return result

    def dot(self, M2):
        # Returns product of two matrices M1 and M2
        s1 = self.shape
        s2 = M2.shape
        if s1[1] == s2[0]:
            mult = sp.zeros(s1[0],s2[1])
            for i in range(s1[0]):
                for j in range(s2[1]):
                    mult[i,j] = self.dotV(self[i,:],M2[:,j])
            return mult
        else:
            print 'Incompatible matrix dimensions'
            
    def Cramer(self, colVector, colNumber):
        # Returns matrix with colVector substituted in column colNumber
        newMatrix = matrix(sp.zeros(self.rows))
        for i in range(self.rows):
            for j in range(self.cols):
                newMatrix[i,j] = self[i,j]
        newMatrix[:,colNumber] = colVector
        return newMatrix

def polyDict(expr ,var):
    """
    Returns a dictionary with coefficients of 's'. They keys represent the
    corresponding order of the coefficient. To be used for circuit expansion
    of polynomials.
    Two to 25 times faster than sympy's Poly(expr, var).as_dict().
    Should only be used with expressions that can be written as poly.
    """
    expr = sp.collect(expr, var)     # collect power terms
    terms = expr.as_coeff_add(var)   # write them as a sum of terms
    exprDict = {}
    exprDict[0] = terms[0]           # zero order coefficient
    coeffList = [0]                  # initialize list for coefficients
    expr = terms[1]                  # tuple with coefficients of nonzero order
    for coeff in expr:              
        coeff = coeff.as_independent(var)
        if coeff[1] == var:          # first order coefficient
            exprDict[1] = coeff[0]
            coeffList.append(1)
        else:                        # higher order coefficients
            order = int(str(coeff[1]).split(str(var)+'**')[1])
            exprDict[order] = coeff[0]
            coeffList.append(order)
        coeffList.sort()
    for i in range(coeffList[len(coeffList)-1]):
        if i not in coeffList:
            exprDict[i] = 0
    return exprDict
    
def numRoots(expr, var):
    """ 
    Using numpy for calculation of numeric roots is about 60 times faster than 
    using sympy.roots(expr, var)
    numpy.roots: 
        https://docs.scipy.org/doc/numpy/reference/generated/numpy.polynomial.polynomial.polyroots.html
        The root estimates are obtained as the eigenvalues of the companion matrix.
        Roots far from the origin of the complex plane may have large errors due to 
        the numerical instability of the power series for such values. Roots with 
        multiplicity greater than 1 will also show larger errors as the value of 
        the series near such points is relatively insensitive to errors in the roots. 
        Isolated roots near the origin can be improved by a few iterations of 
        Newton's method.
    """
    coeffs = []
    coeffDict = polyDict(expr, var)
    order = len(coeffDict.keys())
    for i in range(order):
        coeffs.append(coeffDict[order-1-i])
    coeffs = np.array(coeffs)
    roots = np.roots(coeffs)
    return np.flip(roots, 0)

if __name__ == "__main__":
    s = sp.Symbol('s')
    
    MNA = matrix([[5.0e-12*s + 0.01, 0, 0, -5.0e-12*s - 0.01, 0, 0, 0, 0, 1],
                  [0, 1.98e-11*s + 0.0001, -1.2e-11*s, -1.8e-12*s - 1.0e-5, 0, 0, 0, 0, 0],
                  [0, -1.2e-11*s, 2.8e-11*s + 0.001, 0, -1.0e-11*s - 0.001, 0, 0, -1, 0],
                  [-5.0e-12*s - 0.01, -1.8e-12*s - 1.0e-5, 0, 1.0068e-9*s + 0.01101, 0, 0, 1, 0, 0],
                  [0, 0, -1.0e-11*s - 0.001, 0, 1.0e-11*s + 0.001, 1, 0, 1, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0, -1.0e-6*s, -3.1623e-11*s, 0],
                  [0, 0, -1, 0, 1, 0, -3.1623e-11*s, -1.0e-9*s, 0],
                  [2.048e-20*s**3 + 2.688e-11*s**2 + 0.0016*s + 1, 0, 0, 0, 0, 0, 0, 0, 0]])
    
    DET = MNA.determinant()
    t1=time()
    roots = numRoots(DET,s)
    t2=time()
    print roots, t2-t1
    MOD = MNA.Cramer([0,0,0,1,0,-1,0,0,0],3)
    roots = sp.roots(DET,s)
    print roots

