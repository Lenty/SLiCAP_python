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
    result = re.sub(r'%e','exp(1)', result)
    # Convert 'pi' notation:
    result = re.sub(r'%pi','pi', result)
    # ToDo
    # Other conversions
    # Display the result (for debug purposes, e.g. studying assumptions)
    if ini.dispMaxResult:
        print result
    return(result)

def maxILT(Fs):
    """
    Calculates the inverse Laplace transform of  'Fs' using Maxima.
    Tricky to use because Maxima can ask for assumtions.
    """
    if isinstance(Fs, tuple(sp.core.all_classes)):
        if LAPLACE in list(Fs.free_symbols):
            maxExpr = 'result:bfloat(ilt(' + str(Fs) + ',' + str(LAPLACE) + ',t));'
            result = sp.sympify(maxEval(maxExpr))
            return result
    return 'ft'

def maxDet(M):
    """
    Returns the determinant of matrix 'M' in Sympy format, calculated by Maxima.
    """
    M = sympy2maximaMatrix(M)
    maxExpr = 'm:' + M + ';result:bfloat(expand(newdet(m)));'
    result = sp.sympify(maxEval(maxExpr))
    return(result)
    
def maxNumer(M, detP, detN, srcP, srcN):
    """
    Returns the numerator of a transfer function:
        
    M = MNA matrix
    detP = position of positive detector in vector with dependent variables.
           This can be a nodal voltage or a current through a voltage source or
           False if the positive node is the ground node or a positive current
           is not used.
    detN = position of positive detector in vector with dependent variables
           This can be a nodal voltage or a current through a voltage source or
           False if the negative node is the ground node or a negative current
           is not used.
    srcP:
        Current source:
            = position of positive node in vector with dependent variables.
        Voltage source:
            = position of current through this source in the vector with
              dependent variables.
    srcN:
        Current source:
            = position of positive node in vector with dependent variables.
        Voltage source:
            = False
    
    Note: In Sympy a minor is defined as the determinant of the minor matrix;
          use .minor_submatrix to get the matrix only.
          
          In Maxima a minor is the minor matrix itself.
          
    GCalculation method:
        
        numer = + cofactor(srcP, detP) - cofactor(srcN, detP) 
                - cofactor(srcP, detN) + cofactor(srcN, detN)
    cofactor(i,j) = (-1)^(i+j)*det(minor(i,j))
    
    The minor matrices and the multiplication factors are determined with Sympy,
    the determinants are calculated with Maxima.
    """
    # Create a list of matrices of which the determinant needt to be calculated
    matrices = []
    if detP != None:
        if srcP != None:
            if (detP + srcP)%2 == 0:
                matrices.append(M.minor_submatrix(srcP, detP))
            else:
                matrices.append(-M.minor_submatrix(srcP, detP))
        if srcN != None:
            if (detP + srcN)%2 == 0:
                matrices.append(-M.minor_submatrix(srcN, detP))
            else:
                matrices.append(M.minor_submatrix(srcN, detP))
    if detN != None:
        if srcP != None:
            if (detN + srcP)%2 == 0:
                matrices.append(-M.minor_submatrix(srcP, detN))
            else:
                matrices.append(M.minor_submatrix(srcP, detN))
        if srcN != None:
            if (detN + srcN)%2 == 0:
                matrices.append(M.minor_submatrix(srcN, detN))
            else:
                matrices.append(-M.minor_submatrix(srcN, detN))
    # Create the Maxima instruction
    maxExpr = 'result:bfloat(expand('
    for M in matrices:
        maxExpr += 'newdet(' + sympy2maximaMatrix(M) + ') +'
    maxExpr += '0));'
    return sp.sympify(maxEval(maxExpr))
    
def maxLimit(expr, var, val, pm):
    """
    Calculated the limit of an expression for 'var' approaches 'val' from 'pm'.
    expr: sympy expression or string
    var:  string representing the variable
    val:  string representing the limit value of the variable
    pm:   'plus' or 'minus'
    """
    maxExpr = 'result:bfloat(limit(' + str(expr) + ',' + var + ',' + val + ',' + pm +' ));'
    return sp.sympify(maxEval(maxExpr))

def maxCramer():
    """
    ToDo
    """
    return