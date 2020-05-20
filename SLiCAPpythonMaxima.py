#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 13:57:02 2020

@author: anton
"""
from SLiCAPmatrices import *

def sympy2maximaMatrix(M):
    """
    Converts a sympy two-dimensional matrix into a Maxima matrix.
    """
    return(str(M).replace('Matrix([','matrix(').replace(']])','])'))
    
def maxEval(maxExpr):
    """
    Evaluates maxExpr in Maxima format with Maxima CAS and returns an
    expression in text format.
    
    expr: expression in Maxima format to be evaluated.
    
    The variable that needs to be output must be named: 'result'."""
    
    # LISP command for a  a single-line output in text format:
    maxStringConv = ":lisp (mfuncall '$string $result);"
    maxInput = maxExpr + maxStringConv
    output = subprocess.Popen(['maxima', '--very-quiet', '-batch-string', \
                               maxInput], stdout=subprocess.PIPE).stdout
    # The last line of the output stream is the result                              
    result = output.readlines()[-1]
    output.close()
    # Convert big float notation '12345b+123' to float notation '12345e+123':
    result = re.sub(r'(([+-]?)(\d+)(\.?)(\d*))b(([+-]?)(\d+))', r'\1e\6', result)
    # Convert complex number notation:
    result = re.sub(r'%j','j', result)
    # Convert 'e' (natural base) notation:
    result = re.sub(r'%e','e', result)
    # ToDo
    # Other conversions
    return(result)
    
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

def maxILT(Fs):
    """
    Calculates the inverse Laplace transform of  'Fs' using Maxima.
    """
    maxExpr = 'result:bfloat(ilt(' + str(Fs) + ',' + str(LAPLACE) + ',t));'
    result = sp.sympify(maxEval(maxExpr))
    return result

def maxDet(M):
    """
    Returns the determinant of matrix 'M' in Sympy format, calculated by Maxima.
    """
    M = sympy2maximaMatrix(M)
    maxExpr = 'm:' + M + ';result:bfloat(expand(newdet(m)));'
    result = sp.sympify(maxEval(maxExpr))
    return(result)

if __name__ == '__main__':
    t1=time()
    LIB = makeLibraries()
    
    t2=time()
    ########################
    fi = 'MOSamp.cir'
    ########################
    print "\nCheking:", fi
    myCir = checkCircuit('cir/' + fi )
    
    t3=time()
    (Iv, M, Vv) = makeMatrices(myCir, False)
    display.display(M)
    
    t4=time()
    #del myCir.parDefs[sp.Symbol('I_D')]
    (Iv, M, Vv) = makeMatrices(myCir, True)
    
    t5=time()
    #charPoly = M.determinant()
    #print '\nCharacteristic polynomial Sympy:\n', charPoly
    
    t6=time()
    charpolyM = maxDet(M)
    print '\nCharacteristic polynomial Maxima:\n', charpolyM
    
    t7=time()
    print '\nRoots:\n'
    roots = numRoots(charpolyM, LAPLACE)
    for i in range(len(roots)):
        print i, roots[i]
        
    t8=time()
    Fs = makeLaplaceRational(1, [], roots)
    #ft = sp.inverse_laplace_transform(Fs, LAPLACE, sp.Symbol('t'))
    #print '\ntime function:\n',ft
    
    t9=time()
    ft = maxILT(Fs)
    print '\ntime function:\n',ft
    
    t10=time()
    
    print "\nmakeLibraries                : %fs."%(t2-t1)
    print "checkCircuit                 : %fs."%(t3-t2)
    print "makeMatrices symbolic        : %fs."%(t4-t3)
    print "makeMatrices numeric         : %fs."%(t5-t4)
    #print "determinant Sympy            : %fs."%(t6-t5)
    print "determinant Maxima           : %fs."%(t7-t6)
    print "poles with numpy             : %fs."%(t8-t7)
    print "construct Fs                 : %fs."%(t9-t8)
    print "inverse Laplace with Maxima  : %fs.\n"%(t10-t9)
    print "Total time                   : %fs."%(t10-t1)