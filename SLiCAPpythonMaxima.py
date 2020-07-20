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
                               maxInput], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
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
    # Convert Maxima matrix to sympy matrix:
    result = result.replace('matrix(', 'Matrix([')
    result = result.replace('])', ']])')
    # ToDo
    # Other conversions
    return result

def maxILT(numer, denom, numeric = True):
    """
    Calculates the inverse Laplace transform of  'Fs' using Maxima.
    Tricky to use because Maxima can ask for assumtions.
    """
    Fs = numer/denom
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    # Try inverse laplace of symbolic function
    maxExpr = 'result:%s(ilt('%(numeric) + str(Fs)+',s,t));'
    result = maxEval(maxExpr)
    if len(result) > 3 and result[1:5] == 'ilt(':
        if isinstance(Fs, tuple(sp.core.all_classes)):
            params = set(list(numer.atoms(sp.Symbol)) + list(denom.atoms(sp.Symbol)))
            try:
                params.remove(ini.Laplace)
                if len(params) != 0:
                    print "Error: symbolic variables found, cannot determine roots."
                    return sp.Symbol('ft')
                else:
                    ncoeffs = polyCoeffs(numer, ini.Laplace)
                    zeros = np.roots(np.array(ncoeffs))
                    dcoeffs = polyCoeffs(denom, ini.Laplace)
                    poles = np.roots(np.array(dcoeffs))
                    Fs = makeLaplaceRational(ncoeffs[0]/dcoeffs[0], zeros, poles)
                    maxExpr = 'result:bfloat(ilt('+ str(Fs)+',s,t));'
                    result = maxEval(maxExpr)
                if len(result) > 3 and result[1:5] == 'ilt(':
                    print "Error: could not determine the inverse Laplace transform."
                    return sp.Symbol('ft')
            except:
                print "Error: could not determine the inverse Laplace transform."
                return sp.Symbol('ft')
    return sp.sympify(result)
                    

def maxDet(M, numeric = True):
    """
    Returns the determinant of matrix 'M' in Sympy format, calculated by Maxima.
    """
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    M = sympy2maximaMatrix(M)
    maxExpr = 'm:' + M + ';result:%s(expand(newdet(m)));'%(numeric)
    return sp.sympify(maxEval(maxExpr))
    
def maxNumer(M, detP, detN, srcP, srcN, numeric = True):
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
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
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
    maxExpr = 'result:%s(expand('%(numeric)
    for M in matrices:
        maxExpr += 'newdet(' + sympy2maximaMatrix(M) + ') +'
    maxExpr += '0));'
    return sp.sympify(maxEval(maxExpr))

def maxLimit(expr, var, val, pm, numeric = True):
    """
    Calculates the limit of an expression for 'var' approaches 'val' from 'pm'.
    expr: sympy expression or string
    var:  string representing the variable
    val:  string representing the limit value of the variable
    pm:   'plus' or 'minus'
    """
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    maxExpr = 'result:%s(limit(' + str(expr) + ',' + var + ',' + val + ',' + pm +' ));'%(numeric)
    return sp.sympify(maxEval(maxExpr))

def maxCramerNumer(M, Iv, detP, detN, numeric = True):
    """    
    Returns the numerator of the response at the detector as a result of
    excitations from one or more sources.
        
    M = MNA matrix
    detP = position of positive detector in vector with dependent variables.
           This can be a nodal voltage or a current through a voltage source or
           False if the positive node is the ground node or a positive current
           is not used.
    detN = position of positive detector in vector with dependent variables
           This can be a nodal voltage or a current through a voltage source or
           False if the negative node is the ground node or a negative current
           is not used.
             
    Calculation method:
        
        numer = + determinant(subs(M, col(detP) = Iv))
                - determinant(subs(M, col(detN) = Iv))
    
    The subsititutions are made with Sympy,
    the determinants are calculated with Maxima.
    """
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    maxExpr = 'result:%s(expand('%(numeric)
    if detP != None:
        maxExpr += 'newdet(' + sympy2maximaMatrix(M.Cramer(Iv, detP)) + ')'
    if detN != None:
        maxExpr += '-newdet(' + sympy2maximaMatrix(M.Cramer(Iv, detN)) + ')'
    maxExpr += '));'
    return sp.sympify(maxEval(maxExpr))

def maxCramerCoeff2(cir, M, elID, detP, detN, dc = False, numeric = True):
    """    
    Returns the numerator of the squared transfer from a source to the detector
    in Sympy format, with the Laplace variable replaced with
    '2*%pi*%i* + ini.frequency', or with 0, for noise or for dcVar calculations, 
    respectively.
    """
    if numeric:
        numeric = 'bfloat'
        num = True
    else:
        numeric = ''
        num = False
    subst = False
    if ini.Laplace in M.atoms(sp.Symbol):
        if dc:
            M = M.subs(ini.Laplace, 0)
        else:
            M = M.subs(ini.Laplace, sp.Symbol('__freq__'))
            subst = True
    Iv = makeSrcVector(cir, cir.parDefs, elID, value = 'id', numeric = num)
    maxExpr = 'result:%s(cabs(expand('%(numeric)
    if detP != None:
        maxExpr += 'newdet(' + sympy2maximaMatrix(M.Cramer(Iv, detP)) + ')/' + elID
    if detN != None:
        maxExpr += '-newdet(' + sympy2maximaMatrix(M.Cramer(Iv, detN)) + ')/' + elID
    maxExpr += '))^2);'
    if subst:
        maxExpr = maxExpr.replace('__freq__', '2*%pi*%i*' + str(ini.frequency))
    return sp.sympify(maxEval(maxExpr))

def maxDet2(M, dc = False, numeric = True):
    """
    Returns the squared magnitude of the determinant of matrix 'M' in Sympy 
    format, with the Laplace variable replaced with
    '2*%pi*%i* + ini.frequency', or with 0, for noise or for dcVar calculations, 
    respectively.
    """
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    subst = False
    if ini.Laplace in M.atoms(sp.Symbol):
        if dc:
            M = M.subs(ini.Laplace, 0)
        else:
            M = M .subs(ini.Laplace, sp.Symbol('__freq__'))
            subst = True
    M = sympy2maximaMatrix(M)
    if subst:
        M = M.replace('__freq__', '2*%pi*%i*' + str(ini.frequency))
    maxExpr = 'm:' + M + ';result:%s(cabs(expand(newdet(m)))^2);'%(numeric)
    return sp.sympify(maxEval(maxExpr))

def maxSolve(M, Iv, numeric = True):
    """
    Calculates M^(-1).Iv
    
    M:  Matrix
    Iv: Vector with independent variables
    """
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    maxExpr = 'M:' + sympy2maximaMatrix(M) + ';'
    maxExpr += 'Iv:' + sympy2maximaMatrix(Iv) + ';'
    maxExpr += 'result:%s(invert(M).Iv);'%(numeric)
    return sp.sympify(maxEval(maxExpr))

def maxIntegrate(expr, var, start = None, stop = None, numeric = True):
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    if start != None and stop != None:
        maxExpr = 'assume_pos:true$assume_pos_pred:symbolp$result:%s(integrate(%s, %s, %s, %s));'%(numeric, str(expr), str(var), str(start), str(stop))
    else:
        maxExpr = 'assume_pos:true$assume_pos_pred:symbolp$result:%s(integrate(%s, %s));'%(numeric, str(expr), str(var))
    result = maxEval(maxExpr)
    try:
        result = sp.sympify(result)
    except:
        print 'Error: could not integrate expression: %s.'%(str(expr))
        result = sp.sympify('Error')
    return result

def equateCoeffs(protoType, transfer, noSolve = [], numeric=True):
    """
    Returns the solutions of transfer = protoType.
    Both transfer and prototype should be Laplace rational functions.
    Their numerators should be polynomials of the Laplace variable of equal 
    order and their denominators should be polynomials of the Laplace variable
    of equal order.
    """
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    params = list(set(list(protoType.atoms(sp.Symbol)) + list(transfer.atoms(sp.Symbol))))
    noSolve.append(ini.Laplace)
    for param in noSolve:
        if param in params:
            params.remove(param)
        
    gainP, pN, pD = coeffsTransfer(protoType)
    gainT, tN, tD = coeffsTransfer(transfer)
    if len(pN) != len(tN) or len(pD) != len(tD):
        print 'Error: unequal orders of prototype and target.'
        return values
    values = {}
    if ini.maxSolve:
        equations = ''
        for i in range(len(pN)):
            eqn = sp.Eq(sp.N(pN[i]),sp.N(tN[i]))
            if eqn != True:
                equations += str(pN[i]) + '=' + str(tN[i]) + ','
        for i in range(len(pD)):
            eqn = sp.Eq(sp.N(pD[i]),sp.N(tD[i]))
            if eqn != True:
                equations += str(pD[i]) + '=' + str(tD[i]) + ','
        eqn = sp.Eq(sp.N(gainP, gainT))
        if eqn != True:
            equations += str(gainP) + '=' + str(gainT) + ','
        equations = '[' + equations[0:-1] + ']'
        params = str(params)
        maxExpr = 'result:(%s(solve('%(numeric) + equations + ',' + params + ')))[1];'
        result = maxEval(maxExpr)
        result = result[1:-1].split(',')
        try:
            for i in range(len(result)):
                name, value = result[i].split('=')
                name = sp.Symbol(name.strip())
                values[name] = sp.N(sp.sympify(value))
        except:
            print 'Error: could not solve equations.'
    else:
        equations = []
        for i in range(len(pN)):
            eqn = sp.Eq(sp.N(pN[i]),sp.N(tN[i]))
            if eqn != True:
                equations.append(eqn)
        for i in range(len(pD)):
            eqn = sp.Eq(sp.N(pD[i]),sp.N(tD[i]))
            if eqn != True:
                equations.append(eqn)
        eqn = sp.Eq(sp.N(gainP, gainT))
        if eqn != True:
            equations.append(eqn)
        try:
            solution = sp.solve(equations, (params))[0]
            if type(solution) == dict:
                values = solution
            else:
                values = {}
                for i in range(len(params)):
                    values[params[i]] = solution[i]
        except:
            print 'Error: could not solve equations.'
    return values

def rmsNoise(noiseResult, noise, fmin, fmax, source = None):
    """
    """
    if fmin == None or fmax == None:
        print "Error in frequency range specification."
        return None
    if fmin != None and fmax != None:
        if checkNumber(fmin) != None and  checkNumber(fmin) != None and fmin >= fmax:
            print "Error in frequency range specification."
            return None
    if noiseResult.dataType != 'noise':
        print "Error: expected dataType noise, got: '%s'."%(noiseResult.dataType)
        rms = None
    keys = noiseResult.onoiseTerms.keys()
    if noise == 'inoise':
        if source == None:
            noiseData = noiseResult.inoise
        elif source in keys:
            noiseData = noiseResult.inoiseTerms[source]
        else:
            print "Error: unknown noise source: '%s'."%(source)
            rms = None
    elif noise == 'onoise':
        if source == None:
            noiseData = noiseResult.onoise
        elif source in keys:
            noiseData = noiseResult.onoiseTerms[source]
        else:
            print "Error: unknown noise source: '%s'."%(source)
            rms = None
    else:
        print "Error: unknown noise type: '%s'."%(noise)
        rms = None
    if type(noiseData) != list:
        noiseData = [noiseData]    
    rms =  np.array([sp.N(sp.sqrt(maxIntegrate(noiseData[i], ini.frequency, start=fmin, stop=fmax, numeric=noiseResult.simType))) for i in range(len(noiseData))])
    if len(rms) == 1:
        rms = rms[0]
    return rms