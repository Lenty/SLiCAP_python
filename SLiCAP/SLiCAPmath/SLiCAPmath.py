#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLiCAP module with math functions.

Imported by the module **SLiCAPprotos.py**.
"""
from SLiCAP.SLiCAPlex import *

def det(M):
    """
    Returns the determinant of a square matrix 'M' calculated using recursive 
    minor expansion (Laplace expansion).
    For large matrices with symbolic entries, this is faster than the built-in
    sympy.Matrix.det() method. 
    
    :param M: Sympy matrix
    :type M: sympy.Matrix
    
    :return: Determinant of 'M'
    :rtype:  sympy.Expr
    
    :Example:
        
    >>> dim = 6
    >>> M = sp.zeros(dim, dim)
    >>> for i in range(dim):
    >>>     for j in range(dim):
    >>>         M[i,j] = sp.Symbol('m_' + str(i) + str(j))
    >>> t1 = time()
    >>> D1 = M.det()
    >>> t2=time()
    >>> D2 = determinant(M)
    >>> t3=time()
    >>> print('M.det :', t2-t1, 's')
    >>> print('det(M):', t3-t2, 's')
    >>> print(sp.expand(D1-D2))
    M.det : 150.64841532707214 s
    det(M): 0.4860818386077881 s
    0
    0
    """
    dim = M.shape[0]
    if dim == 2:
        D = sp.expand(M[0,0]*M[1,1]-M[1,0]*M[0,1])
    else:
        D = 0
        for i in range(dim):
            if M[0,i] != 0:
                newM = M.copy()
                newM.row_del(0)
                newM.col_del(i)
                D += M[0,i] * (-1)**(i)*det(newM)
    return sp.expand(D)

def polyCoeffs(expr, var):
    """
    Returns a list with coefficients of 'var' in descending order.

    :param expr: Sympy expression
    :type expr: sympy.Expr

    :param var: Indeterminate of the polynomial.
    :type var: sympy.Symbol

    :return: List with coefficients (*sympy.Expr*) in descending order.
    :rtype: list
    """
    coeffs = []
    if isinstance(expr, sp.Basic) and isinstance(var, sp.Basic):
        coeffs = sp.Poly(expr, var).all_coeffs()
    return coeffs

def numRoots(expr, var):
    """
    Returns the roots of the polynomial 'expr' with indeterminate 'var'.

    This function uses numpy for calculation of numeric roots.

    :note:

    See: https://docs.scipy.org/doc/numpy/reference/generated/numpy.polynomial.polynomial.polyroots.html

    :param expr: Univariate function.
    :type expr: sympy.Expr

    :param var: Indeterminate of 'expr'.
    :type var: sympy.Symbol
    """
    roots = []
    if isinstance(expr, sp.Basic) and isinstance(var, sp.Basic):
        params = list(expr.atoms(sp.Symbol))
        if var in params:
            if len(params) == 1:
                try:
                    coeffs = polyCoeffs(expr, ini.Laplace)
                    roots = np.flip(np.roots(np.array(coeffs)),0)
                except:
                    print("Error: cannot determine the roots of:", str(expr))
            else:
                print("Error: symbolic variables found, cannot determine the numeric roots of:", str(expr))
    return roots

def coeffsTransfer(rational, variable=ini.Laplace):
    """
    Returns a nested list with the coefficients of the variable of the
    numerator and of the denominator of 'rational'.

    The coefficients are in ascending order.

    :param rational: Rational function of the variable.
    :type rational: sympy.Expr
    
    :param variable: Variable of the rational function
    :type variable: sympy.Symbol

    :return: Tuple with gain and two lists: [gain, numerCoeffs, denomCoeffs]

             #. gain (*sympy.Expr*): ratio of the nonzero coefficient of the
                lowest order of the numerator and the coefficient of the
                nonzero coefficient of the lowest order of the denominator.
             #. numerCoeffs  (*list*): List with all coeffcients of the
                numerator in ascending order.
             #. denomCoeffs  (*list*): List with all coeffcients of the
                denominator in ascending order.

    :rtype: tuple
    """
    rational = sp.simplify(rational)
    numer, denom = rational.as_numer_denom()
    coeffsNumer = polyCoeffs(numer, variable)
    coeffsDenom = polyCoeffs(denom, variable)
    # find index coefficient of the lowsest order of the numerator
    idxN = 0
    while idxN > -len(coeffsNumer):
        idxN -= 1
        if coeffsNumer[idxN] != 0:
            break
    # find index coefficient of the lowsest order of the denominator
    idxD = 0
    while idxD > -len(coeffsDenom):
        idxD -= 1
        if coeffsDenom[idxD] != 0:
            break
    gain = sp.simplify(coeffsNumer[idxN]/coeffsDenom[idxD])
    coeffsNumer = [coeffsNumer[i]/coeffsNumer[idxN] for i in range(len(coeffsNumer))]
    coeffsDenom = [coeffsDenom[i]/coeffsDenom[idxD] for i in range(len(coeffsDenom))]
    coeffsNumer.reverse()
    coeffsDenom.reverse()
    return (gain, coeffsNumer, coeffsDenom)

def normalizeRational(rational, variable=ini.Laplace):
    """
    Normalizes a rational expression to:

    .. math::

        F(s) = gain\,s^{\ell}  \\frac{1+b_1s + ... + b_ms^m}{1+a_1s + ... + a_ns^n}

    :param Rational: Rational function of the variable.
    :type Rational: sympy.Expr
    
    :param variable: Variable of the rational function
    :type variable: sympy.Symbol

    :return:  Normalized rational function of the variable.
    :rtype: sympy.Expr
    """
    if variable in list(sp.N(rational).atoms(sp.Symbol)):
        # Exception will be raised of non positive integer powers of variable.
        # Then, we just pass the rational without normaling it.
        try:
            gain, coeffsNumer, coeffsDenom = coeffsTransfer(rational, variable)
            coeffsNumer.reverse()
            coeffsDenom.reverse()
            rational = gain*(sp.Poly(coeffsNumer, variable)/sp.Poly(coeffsDenom, variable))
        except:
            pass
    return rational

def cancelPZ(poles, zeros):
    """
    Cancels poles and zeros that coincide within the displayed accuracy.

    :note:

    The display accuracy (number of digits) is defined by ini.disp.

    :param poles: List with poles (*float*) of a Laplace rational function.
    :type poles: list

    :param zeros: List with zeros (*float*) of a Laplace rational function.
    :type zeros: list

    :return: Tuple with a list with poles (*float*) and a list with zeros (*float*).
    :rtype: Tuple with two lists,
    """
    newPoles = []
    newZeros = []
    # make a copy of the lists of poles and zeros, this one will be modified
    newPoles = [poles[i] for i in range(len(poles))]
    newZeros = [zeros[i] for i in range(len(zeros))]
    for j in range(len(zeros)):
        for i in range(len(poles)):
            # Check if zero coincides with pole
            if abs(poles[i] - zeros[j]) <= 10**(-ini.disp)*abs(poles[i] + zeros[j])/2:
                # if the pole and the zero exist in newPoles and newZeros, respectively
                # then remove the pair
                if poles[i] in newPoles and zeros[j] in newZeros:
                    newPoles.remove(poles[i])
                    newZeros.remove(zeros[j])
    return(newPoles, newZeros)

def gainValue(numer, denom):
    """
    Returns the zero frequency (s=0) value of numer/denom.
    
    :param numer: Numerator of a rational function of the Laplace variable
    :type numer:  sympy.Expr
    
    :param denom: Denominator of a rational function of the Laplace variable
    :type denom:  sympy.Expr
    
    :return:      zero frequency (s=0) value of numer/denom.
    :rtype:       sympy.Expr
    """    
    numer = sp.simplify(numer)
    denom = sp.simplify(denom)
    numerValue = numer.subs(ini.Laplace, 0)
    denomValue = denom.subs(ini.Laplace, 0)
    if numerValue == 0 and denomValue == 0:
        gain = sp.sympify("undefined")
    elif numerValue == 0:
        gain = sp.simplify(0)
    elif denomValue == 0:
        gain = sp.oo
    else:
        gain = sp.simplify(numerValue/denomValue)
    return gain

def findServoBandwidth(loopgainRational):
    """
    Determines the intersection points of the asymptotes of the magnitude of
    the loopgain with unity.

    :param loopgainRational: Rational function of the Laplace variable, that
           represents the loop gain of a circuit.
    :type LoopgainRational: sympy.Expr

    :return: Dictionary with key-value pairs:

             - hpf: frequency of high-pass intersection
             - hpo: order at high-pass intersection
             - lpf: frequency of low-pass intersection
             - lpo: order at low-pass intersection
             - mbv: mid-band value of the loopgain (highest value at order = zero)
             - mbf: lowest freqency of mbv
    :rtype: dict
    """    
    try:
        LaplaceRational = sp.simplify(LaplaceRational)
        numer, denom    = loopgainRational.as_numer_denom()
    except:
        numer, denom    = loopgainRational.as_numer_denom()
        numer           = sp.expand(sp.collect(numer.evalf(), ini.Laplace))
        denom           = sp.expand(sp.collect(denom.evalf(), ini.Laplace))
    poles           = numRoots(denom, ini.Laplace)
    zeros           = numRoots(numer, ini.Laplace)
    poles, zeros = cancelPZ(poles, zeros)
    numPoles        = len(poles)
    numZeros        = len(zeros)
    numCornerFreqs  = numPoles + numZeros
    gain, coeffsN,coeffsD = coeffsTransfer(loopgainRational)
    coeffsN         = np.array(coeffsN)
    coeffsD         = np.array(coeffsD)
    firstNonZeroN   = np.argmax(coeffsN != 0)
    firstNonZeroD   = np.argmax(coeffsD != 0)
    startOrder      = firstNonZeroN - firstNonZeroD
    startValue      = np.abs(gain)
    """ array columns
        1. Corner frequency in rad/s
        2. Order change at that corner +n: n zeros, -n: n poles
        3. Cumulative order from corner frequency
        4. Cumulative LP product
        5. Asymptotic servo cut-off frequency in rad/s (can be low-pass or high-pass)
    """
    freqsOrders     = np.zeros((numCornerFreqs, 6))
    result = {}
    result['mbv'] = startValue # Needs improvement
    result['mbf'] = 0          # Needs improvement
    result['lpf'] = 0
    result['lpo'] = 0
    result['hpf'] = None
    result['hpo'] = 0
    for i in range(numZeros):
        freqsOrders[i, 0] = np.abs(zeros[i])
        freqsOrders[i, 1] = 1
    for i in range(numPoles):
        freqsOrders[numZeros + i, 0] = np.abs(poles[i])
        freqsOrders[numZeros + i, 1] = -1
    # sort the rows with increasing corner frequencies
    freqsOrders = freqsOrders[freqsOrders[:,0].argsort()]
    for i in range(numCornerFreqs):
        if i == 0:
            freqsOrders[i, 2] = startOrder
            if freqsOrders[i, 0] == 0:
                freqsOrders[i, 3] = startValue
                freqsOrders[i, 4] = startValue
                freqsOrders[i, 5] = 0
            else:
                freqsOrders[i, 2] = freqsOrders[i, 1] + freqsOrders[i-1, 2]
                freqsOrders[i, 3] = startValue*freqsOrders[i, 0]** -freqsOrders[i, 1]
                freqsOrders[i, 4] = startValue
        else:
            freqsOrders[i, 2] = freqsOrders[i, 1] + freqsOrders[i-1, 2]
            freqsOrders[i, 3] = freqsOrders[i-1, 3]*freqsOrders[i, 0]**-freqsOrders[i, 1]
            if freqsOrders[i-1, 0] == 0:
                freqsOrders[i, 4] = freqsOrders[i-1, 4] * freqsOrders[i, 0]**freqsOrders[i, 2]
            else:
                freqsOrders[i, 4] = freqsOrders[i-1, 4] * (freqsOrders[i, 0]/freqsOrders[i-1, 0])** freqsOrders[i-1, 2]
        if freqsOrders[i, 2] != 0:
            freqsOrders[i, 5] = freqsOrders[i, 3]**(-1/freqsOrders[i, 2])
            if freqsOrders[i, 5] > freqsOrders[i, 0]:
                if freqsOrders[i, 2] > 0:
                    result['hpf'] = freqsOrders[i, 5]
                    result['hpo'] = freqsOrders[i, 2]
                else:
                    result['lpf'] = freqsOrders[i, 5]
                    result['lpo'] = freqsOrders[i, 2]
        if freqsOrders[i, 4] > result['mbv'] and freqsOrders[i, 0] != 0:
            result['mbv'] = freqsOrders[i, 4]
            result['mbf'] = freqsOrders[i, 0]
    if result['mbf'] == 0:
        result['mbv'] = np.abs(loopgainRational.subs(ini.Laplace, 0))
    if ini.Hz:
        try:
            result['hpf'] = result['hpf']/np.pi/2
        except:
            pass
        try:
            result['lpf'] = result['lpf']/np.pi/2
        except:
            pass
        try:
            result['mbf'] = result['mbf']/np.pi/2
        except:
            pass
    return result

def checkNumber(var):
    """
    Returns a number with its value represented by var, or the symbolic 
    expression if var does not represent a number.

    :param var: Variable that may represent a number.
    :type var: str, sympy object, int, float

    :return: Numeric value (*int, float*) or None
    :rtype: int, float
    """
    if type(var) == str:
        var = replaceScaleFactors(var)
    else:
        var = str(var)
    try:
        number = eval(var)
    except:
        number = sp.sympify(var)
    return number

def fullSubs(valExpr, parDefs):
    """
    Returns 'valExpr' after all parameters of 'parDefs' have been substituted
    into it recursively until no changes occur or until the maximum number of
    substitutions is achieved.

    The maximum number opf recursive substitutions is set by ini.maxRexSubst.

    :param valExpr: Eympy expression in which the parameters should be substituted.
    :type valExpr: sympy.Expr, sympy.Symbol, int, float

    :param parDefs: Dictionary with key-value pairs:

                    - key (*sympy.Symbol*): parameter name
                    - value (*sympy object, int, float*): value of the parameter

    :return: Expression or value obtained from recursive substitutions of
             parameter definitions into 'valExpr'.
    :rtype: sympy object, int, float
    """

    strValExpr = str(valExpr)
    i = 0
    newvalExpr = 0
    while valExpr != newvalExpr and i < ini.maxRecSubst and isinstance(valExpr, sp.Basic):
        # create a substitution dictionary with the smallest number of entries (this speeds up the substitution)
        substDict = {}
        params = list(valExpr.atoms(sp.Symbol))
        for param in params:
            if param in list(parDefs.keys()):
                substDict[param] = parDefs[param]
        # perform the substitution
        newvalExpr = valExpr
        valExpr = newvalExpr.xreplace(substDict)
        i += 1
    if i == ini.maxRecSubst:
        print("Warning: reached maximum number of substitutions for expression '{0}'".format(strValExpr))
    return valExpr

def assumeRealParams(expr, params = 'all'):
    """
    Returns the sympy expression 'expr' in which variables, except the
    Laplace variable, have been redefined as real.

    :param expr: Sympy expression
    :type expr: sympy.Expr, sympy.Symbol

    :param params: List with variable names (*str*), or 'all' or a variable name (*str*).
    :type params: list, str

    :return: Expression with redefined variables.
    :rtype: sympy.Expr, sympy.Symbol
    """

    if type(params) == list:
        for i in range(len(params)):
            expr = expr.xreplace({sp.Symbol(params[i]): sp.Symbol(params[i], real = True)})
    elif type(params) == str:
        if params == 'all':
            params = list(expr.atoms(sp.Symbol))
            try:
                params.remove(ini.Laplace)
            except:
                pass
            for i in range(len(params)):
                expr = expr.xreplace({sp.Symbol(str(params[i])): sp.Symbol(str(params[i]), real = True)})
        else:
            expr = expr.xreplace({sp.Symbol(params): sp.Symbol(params, real = True)})
    else:
        print("Error: expected type 'str' or 'lst', got '{0}'.".format(type(params)))
    return expr

def assumePosParams(expr, params = 'all'):
    """
    Returns the sympy expression 'expr' in which  variables, except the
    Laplace variable, have been redefined as real.

    :param expr: Sympy expression
    :type expr: sympy.Expr, sympy.Symbol

    :param params: List with variable names (*str*), or 'all' or a variable name (*str*).
    :type params: list, str

    :return: Expression with redefined variables.
    :rtype: sympy.Expr, sympy.Symbol
    """

    if type(params) == list:
        for i in range(len(params)):
            expr = expr.xreplace({sp.Symbol(params[i]): sp.Symbol(params[i], positive = True)})
    elif type(params) == str:
        if params == 'all':
            params = list(expr.atoms(sp.Symbol))
            try:
                params.remove(ini.Laplace)
            except:
                pass
            for i in range(len(params)):
                expr = expr.xreplace({sp.Symbol(str(params[i])): sp.Symbol(str(params[i]), positive = True)})
        else:
            expr = expr.xreplace({sp.Symbol(params): sp.Symbol(params, positive = True)})
    else:
        print("Error: expected type 'str' or 'lst', got '{0}'.".format(type(params)))
    return expr

def clearAssumptions(expr, params = 'all'):
    """
    Returns the sympy expression 'expr' in which  the assumtions 'Real' and
    'Positive' have been deleted.

    :param expr: Sympy expression
    :type expr: sympy.Expr, sympy.Symbol

    :param params: List with variable names (*str*), or 'all' or a variable name (*str*).
    :type params: list, str

    :return: Expression with redefined variables.
    :rtype: sympy.Expr, sympy.Symbol
    """
    
    if type(params) == list:
        for i in range(len(params)):
            expr = expr.xreplace({sp.Symbol(params[i], positive = True): sp.Symbol(params[i])})
            expr = expr.xreplace({sp.Symbol(params[i], real = True): sp.Symbol(params[i])})
    elif type(params) == str:
        if params == 'all':
            params = list(expr.atoms(sp.Symbol))
            try:
                params.remove(ini.Laplace)
            except:
                pass
            for i in range(len(params)):
                expr = expr.xreplace({sp.Symbol(str(params[i]), positive = True): sp.Symbol(str(params[i]))})
                expr = expr.xreplace({sp.Symbol(str(params[i]), real = True): sp.Symbol(str(params[i]))})
        else:
            expr = expr.xreplace({sp.Symbol(params, positive = True): sp.Symbol(params)})
            expr = expr.xreplace({sp.Symbol(params, real = True): sp.Symbol(params)})
    else:
        print("Error: expected type 'str' or 'lst', got '{0}'.".format(type(params)))
    return expr

def phaseMargin(LaplaceExpr):
    """
    Calculates the phase margin assuming a loop gain definition according to
    the asymptotic gain model.

    This function uses **scipy.newton()** for determination of the the
    unity-gain frequency. It uses the function **SLiCAPmath.findServoBandwidth()**
    for the initial guess, and ini.disp for the relative accuracy.

    if ini.Hz == True, the units will be degrees and Hz, else radians and
    radians per seconds.

    :param LaplaceExpr: Univariate function (sympy.Expr*) or list with
                        univariate functions (sympy.Expr*) of the Laplace
                        variable.
    :type LaplaceExpr: sympy.Expr, list

    :return: Tuple with phase margin (*float*) and unity-gain frequency
             (*float*), or Tuple with lists with phase margins (*float*) and
             unity-gain frequencies (*float*).

    :rtype: tuple
    """
    freqs = []
    mrgns = []
    if type(LaplaceExpr) != list:
        LaplaceExpr = [LaplaceExpr]
    for expr in LaplaceExpr:
        expr = normalizeRational(sp.N(expr))
        if ini.Hz == True:
            data = expr.xreplace({ini.Laplace: 2*sp.pi*sp.I*ini.frequency})
        else:
            data = expr.xreplace({ini.Laplace: sp.I*ini.frequency})
        func = sp.lambdify(ini.frequency, sp.Abs(data)-1, "numpy")
        guess = findServoBandwidth(expr)['lpf']
        try:
            #freq = newton(func, guess, tol = 10**(-ini.disp), maxiter = 50)
            freq = fsolve(func, guess)[0]
            mrgn = phaseFunc_f(expr, freq)
        except:
            print("Error: could not determine unity-gain frequency for phase margin.")
            freq = None
            mrgn = None
        freqs.append(freq)
        mrgns.append(mrgn)
    if len(freqs) == 1:
        mrgns = mrgns[0]
        freqs = freqs[0]
    return (mrgns, freqs)

def makeYdata(yFunc, xVar, x, lmbdfy=True):
    """
    Returns a list of values y, where y[i] = yFunc(x[i]).
    
    :param yFunc: Function
    :type yFunc: sympy.Expr
    
    :param xVar: Variable that needs to be substituted in *yFunc*
    :type xVar: sympy.Symbol
    
    :param x: List with values of x
    :type x: list
    
    :param lmbdfy: Setting for calculation method of the output y
    
                   - True: Converts the symbolic expression *yFunc* into a
                     numeric single-variable function using sympy.lambdify
                   - False: Subsitutes the x values in the yFunc with sympy.
                   
    :return: list with y values: y[i] = yFunc(x[i]).
    :rtype:  list
    """
    yFunc = sp.N(sp.simplify(yFunc))
    try:
        if xVar in list(yFunc.atoms(sp.Symbol)):
            if lmbdfy == True:
                try:
                    func = sp.lambdify(xVar, yFunc, "numpy")
                    y = func(x)
                except:
                    y = [sp.N(yFunc.subs(xVar, x[i])) for i in range(len(x))]
            else:
                y = [sp.N(yFunc.subs(xVar, x[i])) for i in range(len(x))]
        else:
            y = [yFunc for i in range(len(x))]
    except:
         y = [yFunc for i in range(len(x))]
    return y

def magFunc_f(LaplaceExpr, f):
    """
    Calculates the magnitude at the real frequency f (Fourier) from the
    univariate function 'LaplaceExpr' of the Laplace variable.

    If ini.Hz == true, the Laplace variable will be replaced with
    2*sp.pi*sp.I*ini.frequency.

    If ini.Hz == False, the Laplace variable will be replaced with
    sp.I*ini.frequency.

    :param LaplaceExpr: Univariate function of the Laplace variable.
    :type LaplaceExpr: sympy.Expr

    :param f: Frequency value (*float*), or a numpy array with frequency values
              (*float*).

    :return: Magnitude at the specified frequency, or list with magnitudes at
             the specified frequencies.

    :rtype: float, numpy.array
    """

    if type(f) == list:
        # Convert lists into numpy arrays
        f = np.array(f)
    # Obtain the Fourier transform from the Laplace transform
    if ini.Hz == True:
        data = LaplaceExpr.xreplace({ini.Laplace: 2*sp.pi*sp.I*ini.frequency})
    else:
        data = LaplaceExpr.xreplace({ini.Laplace: sp.I*ini.frequency})
    result = makeYdata(sp.Abs(sp.N(data)), ini.frequency, f, lmbdfy=True)
    return result

def dBmagFunc_f(LaplaceExpr, f):
    """
    Calculates the dB magnitude at the real frequency f (Fourier) from the
    univariate function 'LaplaceExpr' of the Laplace variable.

    If ini.Hz == true, the Laplace variable will be replaced with
    2*sp.pi*sp.I*ini.frequency.

    If ini.Hz == False, the Laplace variable will be replaced with
    sp.I*ini.frequency.

    :param LaplaceExpr: Univariate function of the Laplace variable.
    :type LaplaceExpr: sympy.Expr

    :param f: Frequency value (*float*), or a numpy array with frequency values
              (*float*).

    :return: dB Magnitude at the specified frequency, or list with dB magnitudes
             at the specified frequencies.

    :rtype: float, numpy.array
    """

    if type(f) == list:
        f = np.array(f)
    if ini.Hz == True:
        data = LaplaceExpr.xreplace({ini.Laplace: 2*sp.pi*sp.I*ini.frequency})
    else:
        data = LaplaceExpr.xreplace({ini.Laplace: sp.I*ini.frequency})
    result = makeYdata(20*sp.log(sp.Abs(sp.N(data)), 10), ini.frequency, f, lmbdfy=True)
    return result
    
def phaseFunc_f(LaplaceExpr, f, lmbdfy=True):
    """
    Calculates the phase angle at the real frequency f (Fourier) from the
    univariate function 'LaplaceExpr' of the Laplace variable.

    If ini.Hz == true, the Laplace variable will be replaced with
    2*sp.pi*sp.I*ini.frequency.

    If ini.Hz == False, the Laplace variable will be replaced with
    sp.I*ini.frequency.

    :param LaplaceExpr: Univariate function of the Laplace variable.
    :type LaplaceExpr: sympy.Expr

    :param f: Frequency value (*float*), or a numpy array with frequency values
              (*float*).

    :return: Angle at the specified frequency, or list with angles at
             the specified frequencies.

    :rtype: float, numpy.array
    """
    if type(f) == list:
        f = np.array(f)
    if ini.Hz == True:
        data = sp.N(LaplaceExpr.xreplace({ini.Laplace: 2*sp.pi*sp.I*ini.frequency}))
    else:
        data = sp.N(LaplaceExpr.xreplace({ini.Laplace: sp.I*ini.frequency}))
    if ini.frequency in list(data.atoms(sp.Symbol)):
        if lmbdfy == True:
            func = sp.lambdify(ini.frequency, sp.N(data), "numpy")
            phase = np.angle(func(f))
        else:
            phase = [np.angle(sp.N(data.subs(ini.frequency, f[i]))) for i in range(len(f))]
    elif data >= 0:
        phase = [0 for i in range(len(f))]
    elif data < 0:
        phase = [np.pi for i in range(len(f))]
    try:
        phase = np.unwrap(phase)
    except:
        pass
    if ini.Hz:
        phase = phase * 180/np.pi
    return phase

def delayFunc_f(LaplaceExpr, f, delta=10**(-ini.disp), lmbdfy=True):
    """
    Calculates the group delay at the real frequency f (Fourier) from the
    univariate function 'LaplaceExpr' of the Laplace variable.

    If ini.Hz == true, the Laplace variable will be replaced with
    2*sp.pi*sp.I*ini.frequency.

    If ini.Hz == False, the Laplace variable will be replaced with
    sp.I*ini.frequency.

    :param LaplaceExpr: Univariate function of the Laplace variable.
    :type LaplaceExpr: sympy.Expr

    :param f: Frequency value (*float*), or a numpy array with frequency values
              (*float*).

    :return: Group delay at the specified frequency, or list with group delays
             at the specified frequencies.

    :rtype: float, numpy.array
    """

    if type(f) == list:
        f = np.array(f)
    if ini.Hz == True:
        data = LaplaceExpr.xreplace({ini.Laplace: 2*sp.pi*sp.I*ini.frequency})
    else:
        data = LaplaceExpr.xreplace({ini.Laplace: sp.I*ini.frequency})
    if ini.frequency in list(data.atoms(sp.Symbol)):
        if lmbdfy == True:
            func = sp.lambdify(ini.frequency, sp.N(data), "numpy")
            angle1 = np.angle(func(f))
            angle2 = np.angle(func(f*(1+delta)))
        else:
            angle1 = np.array([np.angle(sp.N(data.subs(ini.frequency, f[i]) for i in range(len(f))))])
            angle2 = np.array([np.angle(sp.N(data.subs(ini.frequency, f[i]*(1+delta)) for i in range(len(f))))])
        try:
            angle1 = np.unwrap(angle1)
            angle2 = np.unwrap(angle2)
        except:
            pass
        delay  = (angle1 - angle2)/delta/f
        if ini.Hz == True:
            delay = delay/2/np.pi
    else:
        delay = [0 for i in range(len(f))]
    return delay

def mag_f(LaplaceExpr):
    """
    Returns the magnitude as a function of the real frequency f (Fourier)
    from the Laplace function 'LaplaceExpr'.

    If ini.Hz == true, the Laplace variable will be replaced with
    2*sp.pi*sp.I*ini.frequency.

    If ini.Hz == False, the Laplace variable will be replaced with
    sp.I*ini.frequency.

    :param LaplaceExpr: Univariate function of the Laplace variable.
    :type LaplaceExpr: sympy.Expr

    :param f: Frequency value (*float*), or a numpy array with frequency values
              (*float*).

    :return: Sympy expression representing the magnitude of the Fourier Transform.
    :rtype: sympy.Expr
    """

    if ini.Hz == True:
        data = LaplaceExpr.xreplace({ini.Laplace: 2*sp.pi*sp.I*ini.frequency})
    else:
        data = LaplaceExpr.xreplace({ini.Laplace: sp.I*ini.frequency})
    return sp.Abs(sp.N(data))

def phase_f(LaplaceExpr):
    """
    Calculates the magnitude as a function of the real frequency f (Fourier)
    from the Laplace function 'LaplaceExpr'.

    If ini.Hz == true, the Laplace variable will be replaced with
    2*sp.pi*sp.I*ini.frequency.

    If ini.Hz == False, the Laplace variable will be replaced with
    sp.I*ini.frequency.

    :param LaplaceExpr: Univariate function of the Laplace variable.
    :type LaplaceExpr: sympy.Expr

    :param f: Frequency value (*float*), or a numpy array with frequency values
              (*float*).

    :return: Sympy expression representing the phase of the Fourier Transform.
    :rtype: sympy.Expr
    """
    if ini.Hz == True:
        data = LaplaceExpr.xreplace({ini.Laplace: 2*sp.pi*sp.I*ini.frequency})
        phase = 180 * sp.arg(data) / sp.N(sp.pi)
    else:
        data = LaplaceExpr.xreplace({ini.Laplace: sp.I*ini.frequency})
        phase = sp.arg(sp.N(data))
    return phase
    
def doCDSint(noiseResult, tau, f_min, f_max):
    """
    Returns the integral from ini.frequency = f_min to ini.frequency = f_max, 
    of a noise spectrum after multiplying it with (2*sin(pi*ini.frequency*tau))^2
    
    :param noiseResult: sympy expression of a noise density spectrum in V^2/Hz or A^2/Hz
    :type noiseResult: sympy.Expr, sympy.Symbol, int or float
    :param tau: Time between two samples
    :type tau: sympy.Expr, sympy.Symbol, int or float    
    :param f_min: Lower limit of the integral
    :type f_min: sympy.Expr, sympy.Symbol, int or float   
    :param f_max: Upper limit of the integral
    :type f_max: sympy.Expr, sympy.Symbol, int or float
    
    :return: integral of the spectrum from f_min to f_max after corelated double sampling
    :rtype: sympy.Expr, sympy.Symbol, int or float
    """
    _phi = sp.Symbol('_phi')
    noiseResult *= ((2*sp.sin(sp.pi*ini.frequency*tau)))**2
    noiseResult = noiseResult.subs(ini.frequency, _phi/tau/sp.pi)
    noiseResultCDSint = sp.integrate(noiseResult/sp.pi/tau, (_phi, f_min*tau*sp.pi, f_max*tau*sp.pi))
    return sp.simplify(noiseResultCDSint)

def doCDS(noiseResult, tau):
    """
    Returns noiseResult after multiplying it with (2*sin(pi*ini.frequency*tau))^2
    
    :param noiseResult: sympy expression of a noise density spectrum in V^2/Hz or A^2/Hz
    :type noiseResult: sympy.Expr, sympy.Symbol, int or float
    :param tau: Time between two samples
    :type tau: sympy.Expr, sympy.Symbol, int or float
    
    :return: noiseResult*(2*sin(pi*ini.frequency*tau))^2
    :rtype: sympy.Expr, sympy.Symbol, int or float
    """
    return noiseResult*((2*sp.sin(sp.pi*ini.frequency*tau)))**2

def routh(charPoly, eps):
    """
    Returns the Routh array of a polynomial of the Laplace variable (ini.Laplace).
    
    :param charPoly: Expression that can be written as a polynomial of the Laplace variable (ini.Laplace).
    :type charPoly:  sympy.Expr
    :param eps:      Symbolic variable used to indicate marginal stability. Use a symbol that is not present in *charPoly*.
    :type eps:       sympy.Symbol
    
    :return: Routh array
    :rtype:  sympy.Matrix
    
    :Example:

    >>> # ini.Laplace = sp.Symbol('s')
    >>> s, eps = sp.symbols('s, epsilon')
    >>> charPoly = s**4+2*s**3+(3+k)*s**2+(1+k)*s+(1+k)
    >>> M = routh(charPoly, eps)
    >>> print(M.col(0)) # Number of roots in the right half plane is equal to
    >>>                 # the number of sign changes in the first column of the
    >>>                 # Routh array
    Matrix([[1], [2], [k/2 + 5/2], [(k**2 + 2*k + 1)/(k + 5)], [k + 1]])
    """
    coeffs = sp.Poly(charPoly, ini.Laplace).all_coeffs()
    orders = len(coeffs)
    dim = int(np.ceil(orders/2))
    M  = [[0 for i in range(dim)] for i in range(orders)]
    M = sp.Matrix(M)
    # Fill the first two rows of the matrix
    for i in range(dim):
        # First row with even orders
        M[0,i] = coeffs[2*i]
        # Second row with odd orders 
        # Zero at the last position if the highest order is even
        if 2*i+1 < orders:
            M[1,i] = coeffs[2*i+1]
        else:
            M[1,i] = 0
    # Calculate all other coefficients of the matrix
    for i in range(2, orders):
        #print(M.row(i-1))
        if M.row(i-1) == sp.Matrix(sp.zeros(1, dim)):
            # Calculate the auxiliary polynomial
            for j in range(dim):
                M[i-1, j] = M[i-2,j]*(orders-i+1-2*j)
        for j in range(dim):
            if M[i-1,0] == 0:
                M[i-1, 0] = eps
            if j + 1 >= dim:
                subMatrix = sp.Matrix([[M[i-2,0], 0],[M[i-1, 0], 0]])
            else:
                subMatrix = sp.Matrix([[M[i-2,0], M[i-2, j+1]],[M[i-1, 0], M[i-1, j+1]]])
            M[i,j] = sp.simplify(-1/M[i-1,0]*subMatrix.det())
    return M

def equateCoeffs(protoType, transfer, noSolve = [], numeric=True):
    """
    Returns the solutions of the equation transferFunction = protoTypeFunction.

    Both transfer and prototype should be Laplace rational functions.
    Their numerators should be polynomials of the Laplace variable of equal
    order and their denominators should be polynomials of the Laplace variable
    of equal order.
    
    :param protoType: Prototype rational expression of the Laplace variable
    :type protoType: sympy.Expr
    :param transfer:

    Transfer fucntion of which the parameters need to be
    solved. The numerator and the denominator of this rational
    expression should be of the same order as those of the
    prototype.

    :type transfer: sympy.Expr

    :param noSolve: List with variables (*str, sympy.core.symbol.Symbol*) that do not need
                    to be solved. These parameters will remain symbolic in the
                    solutions.

    :type noSolve: list

    :param numeric: True will force Maxima to use (big) floats for numeric
                    values.

    :type numeric: bool

    :return: Dictionary with key-value pairs:

             - key: name of the parameter (*sympy.core.symbol.Symbol*)
             - value: solution of this parameter: (*sympy.Expr, int, float*)

    :rtype: dict
    """
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    pars = list(set(list(protoType.atoms(sp.Symbol)) + list(transfer.atoms(sp.Symbol))))
    for i in range(len(noSolve)):
        noSolve[i] = sp.Symbol(str(noSolve[i]))
    params = []
    for par in pars:
        if par != ini.Laplace and par not in noSolve:
            params.append(par)
    gainP, pN, pD = coeffsTransfer(protoType)
    gainT, tN, tD = coeffsTransfer(transfer)
    if len(pN) != len(tN) or len(pD) != len(tD):
        print('Error: unequal orders of prototype and target.')
        return values
    values = {}
    equations = []
    for i in range(len(pN)):
        eqn = sp.Eq(sp.N(pN[i]),sp.N(tN[i]))
        if eqn != True:
            equations.append(eqn)
    for i in range(len(pD)):
        eqn = sp.Eq(sp.N(pD[i]),sp.N(tD[i]))
        if eqn != True:
            equations.append(eqn)
    eqn = sp.Eq(gainP, gainT)
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
        print('Error: could not solve equations.')
    return values

if __name__ == "__main__":
    s = ini.Laplace
    loopgain_numer   = sp.sympify('-s*(1 + s/20)*(1 + s/40)/2')
    loopgain_denom   = sp.sympify('(s + 1)^2*(1 + s/4e3)*(1 + s/50e3)*(1 + s/1e6)')
    loopgain         = loopgain_numer/loopgain_denom
    servo_info       = findServoBandwidth(loopgain)
    print(servo_info)
    
    k = sp.Symbol('k')
    charPoly = s**4+2*s**3+(3+k)*s**2+(1+k)*s+(1+k)
    #charPoly = 10 + 11*s +4*s**2 + 2*s**3 + 2*s**4 + s**5
    #charPoly = s**4-1
    #charPoly = s**5+s**4+2*s**3+2*s**2+s+1
    #roots = numRoots(charPoly, ini.Laplace)
    eps = sp.Symbol('epsilon')
    print(routh(charPoly, eps))
    
    numer    = sp.sympify('f+b*s+c*s^2')
    denom    = sp.sympify('a+b*s+c*s^2+d*s^3')
    rational = normalizeRational(numer/denom)
    gain     = gainValue(numer, denom)   
    print(gain)