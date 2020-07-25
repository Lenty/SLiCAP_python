#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 13:57:02 2020

@author: anton
"""
from SLiCAPmatrices import *
    
def sympy2maximaMatrix(M):
    """
    Converts a sympy matrix object into a Maxima matrix definition.
    
    argument    : sympy matrix
    
    return value: str: sympy matrix converted to a Maxima matrix
    """
    return(str(M).replace('Matrix([','matrix(').replace(']])','])'))
    
def maxEval(maxExpr):
    """
    Starts a subprocess that evaluates maxExpr with Maxima CAS and returns the
    resulting expression in text format. The variable that needs to be output 
    must be named: 'result'.
    
    argument    : expression in Maxima format to be evaluated.
    return value: string that can be converted into a sympy expression
    
    In some cases Maxima CAS will ask for extra input.
    This will be ignored and in such cases a time out will kill the subprocess.
    
    In python 3 a time out argument can be passed with communicate().
    
    
    Example: 
        
    >>> result = maxEval(result:ilt(1/(s^2 + a^2), s, t);)
    
    """
    # LISP command for a  a single-line output in text format:
    maxStringConv = ":lisp (mfuncall '$string $result);"
    maxInput = maxExpr + maxStringConv 
    p = subprocess.Popen(['maxima', '--very-quiet', '-batch-string', \
                               maxInput], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Define a function for killing the process
    kill     = lambda process: process.kill()
    # Define the timer for killing the process
    maxTimer = Timer(ini.MaximaTimeOut, kill, [p])
    # Start the timer
    maxTimer.start()
    # Get the ouput from the subprocess
    stdout, stderr = p.communicate()
    # The last line of the output stream is the result   
    result = stdout.split('\n')[-1]
    # Cancel the timer because the process does not exsists after succesfully
    # reading its output
    maxTimer.cancel()
    # Convert the result such that it can be 'sympified'
    if result != '':
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
    
    This function first tries to calculate the ILT symbolically, if this fails
    it tries to create a factorized rational expression of the Laplace variable
    ini.laplace and then calculates the ILT form this rational expression. 
    
    arguments:
        
        numer  : numarator of the Laplace Transform
        denom  : denominator of the Laplace Transform
        numeric: True will force Maxima to use (big) floats for numeric
                 values
                 
    return value:
        
        sp.Symbol('ft') if the ILT failed
        sumpy expression of the time function if the ILT succeeded.
        
    Example:
        
       print maxILT(1, ini.Laplace**2 + sp.Symbol('a')**2, numeric = False)
    """
    Fs = numer/denom
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    # Try inverse laplace of symbolic function
    maxExpr = 'assume_pos:true$assume_pos_pred:symbolp$result:%s(ilt('%(numeric) + str(Fs)+',s,t));'
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
    elif result == '':
            print "Error: Maxima CAS processing error."
            return sp.Symbol('ft')
    return sp.sympify(result)

def maxDet(M, numeric = True):
    """
    Returns the determinant of matrix 'M' in Sympy format, calculated by Maxima.
    
    arguments:
        
        M       : matrix of which the determinant needs to be evaluated
        numeric : True will force Maxima to use (big) floats for numeric values
        
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
    detP :    position of positive detector in vector with dependent variables.
              This can be a nodal voltage or a current through a voltage source
              or None if the positive node is the ground node or a positive 
              current is not used.
    detN :    position of positive detector in vector with dependent variables
              This can be a nodal voltage or a current through a voltage source
              or None if the negative node is the ground node or a negative 
              current is not used.
    srcP    : Current source: position of positive node in vector with dependent 
                              variables.
              Voltage source: position of current through this source in the 
                              vector with dependent variables.
    srcN    : Current source: position of positive node in vector with dependent 
                              variables.
              Voltage source: None
        
    numeric : True will force Maxima to use (big) floats for numeric values
    
    Note:     In Sympy a minor is defined as the determinant of the minor 
              matrix. Use the attribute .minor_submatrix to get the matrix only.
          
              In Maxima a minor is the minor matrix itself.
          
    Calculation method:
        
              numer = + cofactor(srcP, detP) - cofactor(srcN, detP) 
                      - cofactor(srcP, detN) + cofactor(srcN, detN)
              cofactor(i,j) = (-1)^(i+j)*det(minor(i,j))
    
    The minor matrices and the multiplication factors are determined with Sympy,
    the determinants are calculated with Maxima.
    
    return value: sympy expression (numerator of a transfer function)
    """
    # Create a list of matrices of which the determinant needt to be calculated
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    # Create the Maxima instruction
    maxExpr = 'result:%s(expand('%(numeric)
    if detP != None:
        if srcP != None:
            if (detP+srcP)%2 == 0:
                maxExpr += '+newdet(' + sympy2maximaMatrix(M.minor_submatrix(srcP, detP)) + ')'
            else:
                maxExpr += '-newdet(' + sympy2maximaMatrix(M.minor_submatrix(srcP, detP)) + ')'
        if srcN != None:
            if (detP+srcN)%2 == 0:
                maxExpr += '-newdet(' + sympy2maximaMatrix(M.minor_submatrix(srcN, detP)) + ')'
            else:
                maxExpr += '+newdet(' + sympy2maximaMatrix(M.minor_submatrix(srcN, detP)) + ')'
    if detN != None:
        if srcP != None:
            if (detN+srcP)%2 == 0:
                maxExpr += '-newdet(' + sympy2maximaMatrix(M.minor_submatrix(srcP, detN)) + ')'
            else:
                maxExpr += '+newdet(' + sympy2maximaMatrix(M.minor_submatrix(srcP, detN)) + ')'
        if srcN != None:
            if (detN+srcN)%2 == 0:
                maxExpr += '+newdet(' + sympy2maximaMatrix(M.minor_submatrix(srcN, detN)) + ')'
            else:
                maxExpr += '-newdet(' + sympy2maximaMatrix(M.minor_submatrix(srcN, detN)) + ')'
    maxExpr += '));'
    return sp.sympify(maxEval(maxExpr))

def maxLimit(expr, var, val, pm, numeric = True):
    """
    Calculates the limit of an expression for 'var' approaches 'val' from 'pm'.
    
    arguments:
        
        expr    : sympy expression or string
        var     :  string representing the variable
        val     :  string representing the limit value of the variable
        pm      :   'plus' or 'minus'
        numeric : True will force Maxima to use (big) floats for numeric values
    
    return value: sympy expression
         
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
    
    arguments:   
        
    M    : MNA matrix (sympy matrix object)
    Iv   : Vector with independent variables (sympy matrix object)
    detP : (int or None) position of positive detector in vector with dependent
           variables.
           This can be a nodal voltage or a current through a voltage source or
           False if the positive node is the ground node or a positive current
           is not used.
    detN : (int or None) position of positive detector in vector with dependent 
           variables
           This can be a nodal voltage or a current through a voltage source or
           False if the negative node is the ground node or a negative current
           is not used.
        
    numeric : True will force Maxima to use (big) floats for numeric values
             
    Calculation method:
        
        numer = + determinant(subs(M, col(detP) = Iv))
                - determinant(subs(M, col(detN) = Iv))
    
    The subsititutions are made with Sympy,
    the determinants are calculated with Maxima.
    
    return value: sympy expression
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
    '2*%pi*%i*ini.frequency' for noise, or with 0, for noise or for dcVar 
    calculations, respectively.
    
    arguments:
        
        cir     : Circuit object
        M       : MNA matrix
        elID    : RefDes of an independent source of cir.elements
        detP    : (int) position of the positive detector in the vector with
                  independent variables, or None
        detN    : (int) position of the negative detector in the vector with
                  independent variables, or None
        dc      : If True the Laplace variable will be substituted with 0
        numeric : True will force Maxima to use (big) floats for numeric values
        
    return value:
        
        sympy expression
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
    
    arguments:

        M       : MNA matrix
        dc      : If True the Laplace variable will be substituted with 0
        numeric : True will force Maxima to use (big) floats for numeric values
        
    return value:
        
        sympy expression
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
    
    arguments:
        
        M       :  Matrix
        Iv      : Vector with independent variables
        numeric : True will force Maxima to use (big) floats for numeric values
        
    return value:
        
        sympy expression (matrix)
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
    """
    Calculated definite or indefinite integral of 'expr'.
    
    arguments:
        
        expr    : integrand
        var     : integration variable
        start   : lower limit of the integral: None, number or sympy expression
        stop    : upper limit of the integral: None, number or sympy expression
        numeric : True will force Maxima to use (big) floats for numeric values
        
    return value:
        
        sympy expression
    """
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
    Returns the solutions of the equation transferFunction = protoTypeFunction.
    Both transfer and prototype should be Laplace rational functions.
    Their numerators should be polynomials of the Laplace variable of equal 
    order and their denominators should be polynomials of the Laplace variable
    of equal order.
    
    arguments:
        
        protoType : Prototype rational expression of the Laplace variable
        transfer  : Transfer fucntion of which the parameters need to be
                    solved. The numerator and the denominator of this rational 
                    expression should be of the same order as those of the 
                    prototype.
        noSolve   : Variables that do not need to besolved. The will be 
                    symbolic variables in the solutions.
        numeric   : True will force Maxima to use (big) floats for numeric 
                    values
        
    return value: 
        
        dict with key-value pairs:
            
            key   : name of the parameter (sympy.Symbol)
            value : solution of this parameter: number of sympy expression
        
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
    Calculates the RMS (integrated) source-referred noise or detector-referred
    noise, or the contribution of a specific noise source to it.
    
    arguments:
        
        noiseResult : allResults object (execution result of a noise analysis)
        noise       : 'inoise' or 'onoise' for source-referred noise or 
                      detector-referred noise, respectively
        fmin        : lower limit of the frequency range in Hz
        fmax        : upper limit of the frequency range in Hz
        source      : 'all' or refDes of a noise source of which the 
                      contribution to the RMS noise needs to be evaluated
    return value:
        
        number of sympy expression if noiseResult is a single-run result
        numpy array if noiseResult is a multiple run execution result

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

if __name__ == '__main__':
    print maxILT(1, ini.Laplace**2 + sp.Symbol('a')**2, numeric = False)