#!/usr/bin/python2.7
from SLiCAPprotos import *

class matrix(sp.Matrix):
    """SLiCAP matrix class for faster symbolic calculations.
    return types for matrices are <class 'sympy.matrices.matrices.Matrix'>."""
    def __init__(self, M):
        pass
    
    def minor(self, i, j):
        # Returns determinant of M after deleting row i and column j
        return matrix(self.minor_submatrix(i, j)).determinant()

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
        newMatrix = matrix(sp.zeros(self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                newMatrix[i,j] = self[i,j]
        newMatrix[:,colNumber] = colVector
        return newMatrix

def polyCoeffs(expr, var):
    """
    Returns a list with coefficients of 'var' in descending order.
    """
    if isinstance(expr, tuple(sp.core.all_classes)) and isinstance(var, tuple(sp.core.all_classes)):
        #print expr.expand(basic = True)
        return sp.poly(expr, LAPLACE).all_coeffs()
    return []

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
    if isinstance(expr, tuple(sp.core.all_classes)) and isinstance(var, tuple(sp.core.all_classes)):
        params = list(expr.free_symbols)
        try:
            params.remove(var)
            if len(params) != 0:
                print "Error: symbolic variables found, cannot determine roots."
                return []
        except:
            return []
        roots = np.roots(np.array(sp.Poly(expr, LAPLACE).all_coeffs()))
        return np.flip(roots, 0)
    return []
    
def makeLaplaceRational(gain, zeros, poles):
    """
    Creates a Laplace rational from a gain factor, a list of zeros and a list
    of poles:
        
        F(s) = gain * product_j(s-z_j) / product_i(s-p_i)
        
    Terms with complex conjugated poles or zeros will be combined into 
    quadratic terms.
    
    The gain factor should be taken as the ratio of the coefficients of the 
    highest order of the Laplace variable of the numerator and the denominator.
    """
    Fs = gain
    for z in zeros:
        if sp.im(z) == 0:
            Fs *= (LAPLACE-z)
        elif sp.im(z) > 0:
            Fs *= (LAPLACE**2 - 2*sp.re(z) + sp.re(z)**2 + sp.im(z)**2)
    for p in poles:
        if sp.im(p) == 0:
            Fs /= (LAPLACE-p)
        elif sp.im(p) > 0:
            Fs /= (LAPLACE**2 - 2*sp.re(p)*LAPLACE + sp.re(p)**2 + sp.im(p)**2)
    return(Fs)

def coeffsTransfer(LaplaceRational):
    """
    Returns a nested list with the coefficients of the Laplace variable of the 
    numerator and of the denominator of LpalaceRational.
    The coefficients are in ascending order.
    """
    (numer, denom) = sp.fraction(sp.simplify(LaplaceRational))
    coeffsNumer = polyCoeffs(numer, LAPLACE)
    coeffsDenom = polyCoeffs(denom, LAPLACE)
    coeffsNumer.reverse()
    coeffsDenom.reverse()
    return (coeffsNumer, coeffsDenom)

def normalizeLaplaceRational(numer, denom):
    """
    Normalizes a Laplace rational:
        
        F(s) = gain * s^l (1+b_1*s + ... + b_m*s^m)/ (1+a_1*s + ... + a_n*s^n)

        with l zero if there is a finite nonzero zero-frequency value, else
        positive or negative
        
    """
    coeffsNumer = polyCoeffs(numer, LAPLACE)
    nNumer = len(coeffsNumer)
    coeffsDenom = polyCoeffs(denom, LAPLACE)
    nDenom = len(coeffsDenom)
    # find coefficient of LAPLACE of the lowest order of the denominator:
    i = 0
    coeffD = 1 # Just a nonzero startvalue
    while coeffD != 0.:
        coeffD = coeffsDenom[i]
        i += 1
        if i == nDenom:
            break
    i = 0
    coeffN = 1 # Just a nonzero startvalue
    while coeffN != 0.:
        coeffN = coeffsNumer[i]
        i += 1
        if i == nNumer:
            break
    numer = 0
    denom = 0
    # normalize coefficients and construct the rational
    gain = sp.simplify(coeffN/coeffD)
    for j in range(len(coeffsNumer)):
        numer += sp.simplify(coeffsNumer[j]/coeffD/gain)*LAPLACE**(nNumer-j-1)
    for j in range(len(coeffsDenom)):
        denom += sp.simplify(coeffsDenom[j]/coeffD)*LAPLACE**(nDenom-j-1)
    return gain*(numer/denom)

def cancelPZ(poles,zeros):
    """
    Cancels poles and zeros that coincide within the displayed accuracy.
    """
    newPoles = []
    newZeros = []
    # make a copy of the lists of poles and zeros, this one will be modified
    for i in range(len(poles)):
        newPoles.append(poles[i])
    for i in range(len(zeros)):
        newZeros.append(zeros[i])
    for i in range(len(poles)):
        for j in range(len(zeros)):
            if abs(sp.re(poles[i]) - sp.re(zeros[j])) <= 10**(-DISP)*abs(sp.re(poles[i]) + sp.re(zeros[j]))/2 \
            and abs(sp.im(poles[i]) - sp.im(zeros[j])) <= 10**(-DISP)*abs(sp.im(poles[i]) + sp.im(zeros[j]))/2:
                newPoles.remove(poles[i])
                newZeros.remove(zeros[j])             
    return(newPoles, newZeros)
    
def checkNumber(var):
    """
    Returns a number with its value represented by var, or None if var
    does not represent a number.
    """
    if type(var) == str:
        var = replaceScaleFactors(var)
    else:
        var = str(var)
    try:
        number = eval(var)
        return number
    except:
        return None

def fullSubs(valExpr, parDefs):
    """
    Returns the valExpr after all parameters of parDefs have been substituted
    recursively into valExpr.
    parDefs is a dictionary in which the keys are sympy symbols. The type of 
    the value fields may be any sympy type, integer or float.
    """
    strValExpr = str(valExpr)
    i = 0
    newvalExpr = 0
    while valExpr != newvalExpr and i < MAXRECSUBST and isinstance(valExpr, tuple(sp.core.all_classes)):
        # create a substitution dictionary with the smallest number of entries (this speeds up the substitution)
        substDict = {}
        params = list(valExpr.free_symbols)
        for param in params:
            if param in parDefs.keys():
                substDict[param] = parDefs[param]
        # perform the substitution
        newvalExpr = valExpr
        valExpr = newvalExpr.subs(substDict)
        i += 1
    if i == MAXRECSUBST:
        print "Warning: reached maximum number of substitutions for expression '%s'"%(strValExpr)
    return valExpr

def invLaplace(numer, denom):
    """
    Calculates the Inverse Laplace Transform of a numerical rational expression
    of which the sympy polynomials of the numerator and the denominator are 
    passed as arguments, respecively.
    """
    numer = np.poly1d(polyCoeffs(numer, LAPLACE))
    numerCoeffs = [np.float(coeff) for coeff in numer.c]
    denom = np.poly1d(polyCoeffs(denom, LAPLACE))
    denomCoeffs = [np.float(coeff) for coeff in denom.c]
    (r, p, k) = residue(numerCoeffs, denomCoeffs, tol=10**(-DISP))
    t = sp.Symbol('t', real=True)
    ft = 0
    m = 1
    for i in range(len(r)):
        if i > 0:
            if abs(p[i] - p[i - 1]) < 10**(-DISP) * abs(p[i]):
                m += 1
            else:
                m = 1
        ft += (t**(m - 1)/sp.factorial(m - 1))*r[i]*sp.E**(p[i]*t)
    return ft
 
if __name__ == "__main__":
    s = LAPLACE
    
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
    roots1 = numRoots(DET,s)
    t2=time()
    print roots1, t2-t1
    MOD = MNA.Cramer([0,0,0,1,0,-1,0,0,0],3)
    DET = MOD.determinant()
    roots2 = numRoots(DET,s)
    print roots2