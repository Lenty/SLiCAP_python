#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLiCAP module with symbolic math functions executed by maxima CAS.

Imported by the module **SLiCAPplots.py**.
"""
from SLiCAP.SLiCAPmatrices import *

def sympy2maximaMatrix(M):
    """
    Converts a sympy matrix object into a Maxima matrix definition.

    :param M: sympy matrix
    :type M: symPy.Matrix

    :return: sympy matrix converted to a Maxima matrix
    :rtype: str
    """
    return(str(M).replace('Matrix([','matrix(').replace(']])','])'))

def maxEval(maxExpr):
    """
    Evaluates the expression 'maxExpr' with Maxima CAS and returns the result.

    Starts a subprocess that evaluates maxExpr with Maxima CAS and returns the
    resulting expression in text format. The variable that needs to be output
    must be named: 'result'.

    In some cases Maxima CAS will ask for extra input.
    This will be ignored and a time out will kill the subprocess.

    :param maxExpr: Expression in Maxima format to be evaluated.
    :type maxExpr: str

    :return: String that can be converted into a sympy expression.
    :rtype: str

    Example:

    >>> maxEval("result:ilt(1/(s^2 + a^2), s, t);")
    'sin(a*t)/a'
    """
    # LISP command for a  a single-line output in text format:
    maxStringConv = ":lisp (mfuncall '$string $result);"
    maxAssume = "assume_pos:true$assume_pos_pred:symbolp$"
    maxInput = maxAssume + maxExpr + maxStringConv
    # Check system we are running on and read the output
    if platform.system() == 'Windows':
        # result = subprocess.run([ini.maxima, '--very-quiet', '-batch-string', maxInput], capture_output=True, timeout=ini.MaximaTimeOut, text=True).stdout.split('\n')[-1]
        result = subprocess.run([ini.maxima, '--very-quiet', '-batch-string', maxInput], capture_output=True, timeout=ini.MaximaTimeOut, text=True).stdout.split('\n')
    else:
        result = subprocess.run(['maxima', '--very-quiet', '-batch-string', maxInput], capture_output=True, timeout=ini.MaximaTimeOut, text=True).stdout.split('\n')
    # Convert the result such that it can be 'sympified' by sympy
    result = [i for i in result if i] # Added due to variability of trailing '\n'
    result = result[-1]
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
    Calculates the inverse Laplace transform of  'Fs' using Maxima CAS.

    This function first tries to calculate the ILT symbolically, if this fails
    it tries to create a factorized rational expression of the Laplace variable
    ini.laplace and then calculates the ILT of this rational expression.

    :param numer: Numarator of the Laplace Transform.
    :type numer: sympy.Expr

    :param denom : Denominator of the Laplace Transform.
    :type denom: sympy.Expr

    :param numeric: True will force Maxima to use (big) floats for numeric
                    values.
    :type numeric: bool

    :return: Sympy expression of the time function if the ILT succeeded, or
             sp.Symbol('ft') if the ILT failed.

    :Example:

    >>> maxILT(2, 3*ini.Laplace**2 + sp.Symbol('a')**2, numeric = False)
    2*sqrt(3)*sin(sqrt(3)*a*t/3)/(3*a)

    :Example:

    >>> maxILT(2, 3*ini.Laplace**2 + sp.Symbol('a')**2, numeric = True)
    1.154700538379252*sin(0.5773502691896258*a*t)/a
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
        if isinstance(Fs, sp.Basic):
            params = set(list(numer.atoms(sp.Symbol)) + list(denom.atoms(sp.Symbol)))
            try:
                params.remove(ini.Laplace)
                if len(params) != 0:
                    print("Error: symbolic variables found, cannot determine roots.")
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
                    print("Error: could not determine the inverse Laplace transform.")
                    return sp.Symbol('ft')

            except:
                print("Error: could not determine the inverse Laplace transform.")
                return sp.Symbol('ft')
    elif result == '':
            print("Error: Maxima CAS processing error.")
            return sp.Symbol('ft')
    return sp.sympify(result)

def detFunc():
    return "det(M):=block([D,dim,i],dim:length(M),if dim=2 then D:M[1,1]*M[2,2]-M[1,2]*M[2,1] else block(D:0,for i from 1 thru dim do if M[1,i]#0 then D:D+M[1,i]*(-1)^(i+1)*det(minor(M,1,i))),expand(D));compile(det);"

def maxDet(M, numeric = True):
    """
    Returns the determinant of matrix 'M' in Sympy format, calculated by Maxima CAS.

    Calculation of the determinant according to the GENTLEMAN-JOHNSON TREE-MINOR
    method. This is a fast version of expansion by minors. It it implemented in
    Maxima CAS for matrices up to 50 x 50.

    :param M: Matrix of which the determinant needs to be evaluated
    :type M: sympy.Matrix

    :param numeric: True will force Maxima to use (big) floats for numeric
                    values.
    :type numeric: bool
    """
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    maxMatrix = sympy2maximaMatrix(M)
    rows, cols = M.shape
    if M.shape[0] < ini.MaximaMatrixDim:
        maxExpr = 'm:' + maxMatrix + ';result:%s(expand(newdet(m)));'%(numeric)
    else:
        maxExpr = detFunc() + 'm:' + maxMatrix + ';result:%s(det(m));'%(numeric)
    result = maxEval(maxExpr)
    try:
        return sp.sympify(result)
    except:
        print('Maxima error:', result)

def maxNumer(M, detP, detN, srcP, srcN, numeric = True):
    """
    Returns the numerator of a transfer function.

    Calculation method:

    - numer = + cofactor(srcP, detP) - cofactor(srcN, detP) - cofactor(srcP, detN) + cofactor(srcN, detN)
    - cofactor(i,j) = (-1)^(i+j)*det(minor(i,j))

    The minor matrices and the multiplication factors are determined with Sympy,
    the determinants are calculated with Maxima.

    :Note: In Sympy a minor is defined as the determinant of the minor
           matrix. Use sympy.Matrix.minor_submatrix to get the matrix only.

           In Maxima a minor is the minor matrix itself.

    :param M: MNA matrix
    :type M: sympy.Matrix

    :param detP: Position of positive detector in vector with dependent variables.
                 This can be a nodal voltage or a current through a voltage source
                 or None if the positive node is the ground node or a positive
                 current is not used.
    :type detP: int, bool

    :param detN: Position of positive detector in vector with dependent variables.
                 This can be a nodal voltage or a current through a voltage source
                 or None if the negative node is the ground node or a negative
                 current is not used.
    :type detN: int, bool

    :param srcP: Current source: position of positive node in vector with
                 dependent variables.

                 Voltage source: position of current through this source in the
                 vector with dependent variables.
    :type srcP: int, bool
    :param srcN: Current source: position of positive node in vector with dependent
                 variables.

                 Voltage source: None
    :type srcN: int, bool

    :param numeric: True will force Maxima to use (big) floats for numeric
                    values.
    :type numeric: bool


    :return: Numerator of a transfer function
    :rtype: sympy.Expr
    """
    # Create a list of matrices of which the determinant needt to be calculated
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    rows, cols = M.shape
    if rows <= ini.MaximaMatrixDim:
        # Create the Maxima instruction
        maxExpr = 'result:%s(expand('%(numeric)
        func = 'newdet('
    else:
        maxExpr = detFunc() + 'result:%s(expand('%(numeric)
        func = 'det('
    if detP != None:
        if srcP != None:
            if (detP+srcP)%2 == 0:
                maxExpr += '+' + func + sympy2maximaMatrix(M.minor_submatrix(srcP, detP)) + ')'
            else:
                maxExpr += '-' + func + sympy2maximaMatrix(M.minor_submatrix(srcP, detP)) + ')'
        if srcN != None:
            if (detP+srcN)%2 == 0:
                maxExpr += '-' + func + sympy2maximaMatrix(M.minor_submatrix(srcN, detP)) + ')'
            else:
                maxExpr += '+' + func + sympy2maximaMatrix(M.minor_submatrix(srcN, detP)) + ')'
    if detN != None:
        if srcP != None:
            if (detN+srcP)%2 == 0:
                maxExpr += '-' + func + sympy2maximaMatrix(M.minor_submatrix(srcP, detN)) + ')'
            else:
                maxExpr += '+' + func + sympy2maximaMatrix(M.minor_submatrix(srcP, detN)) + ')'
        if srcN != None:
            if (detN+srcN)%2 == 0:
                maxExpr += '+' + func + sympy2maximaMatrix(M.minor_submatrix(srcN, detN)) + ')'
            else:
                maxExpr += '-' + func + sympy2maximaMatrix(M.minor_submatrix(srcN, detN)) + ')'
    maxExpr += '));'
    result = maxEval(maxExpr)
    try:
        return sp.sympify(result)
    except:
        print('Maxima error:', result)

def maxLimit(expr, var, val, pm, numeric = True):
    """
    Calculates the limit of an expression for 'var' approaches 'val' from 'pm'.

    :param expr: Expression of which the limit must be evaluated.
    :type expr: sympy.Expr, str
    :param var: Variable that should approach the limit value.
    :type var: sympy.Symbol, str
    :param val: Limit value of the variable.
    :type val:  sympy.Symbol, str, sp.Expr, int, float
    :param pm: Direction: 'plus' or 'minus'
    :type pm: str
    :param numeric: True will force Maxima to use (big) floats for numeric
                    values.
    :type numeric: bool

    :return: Calculated limit
    :rtype: sympy.Expr
    """
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    maxExpr = 'result:%s(limit(' + str(expr) + ',' + str(var) + ',' + str(val) + ',' + pm +' ));'%(numeric)
    result = maxEval(maxExpr)
    try:
        return sp.sympify(result)
    except:
        print('Maxima error:', result)

def maxCramerNumer(M, Iv, detP, detN, numeric = True):
    """
    Returns the numerator of the response at the detector as a result of
    excitations from one or more sources.

    Calculation method:

    - numer = + determinant(subs(M, col(detP) = Iv)) - determinant(subs(M, col(detN) = Iv))

    The subsititutions are made with Sympy. The determinants are calculated with Maxima CAS.

    :param M: MNA matrix
    :type M: sympy.Matrix

    :param Iv: Vector with independent variables
    :type Iv: sympy.Matrix

    :param detP: Position of positive detector in vector with dependent variables.
                 This can be a nodal voltage or a current through a voltage source
                 or None if the positive node is the ground node or a positive
                 current is not used.
    :type detP: int, bool

    :param detN: Position of positive detector in vector with dependent variables.
                 This can be a nodal voltage or a current through a voltage source
                 or None if the negative node is the ground node or a negative
                 current is not used.
    :type detN: int, bool

    :param numeric: True will force Maxima to use (big) floats for numeric
                    values.
    :type numeric: bool

    :return: Numerator of a response
    :rtype: sympy.Expr
    """
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    rows, cols = M.shape
    if rows <= ini.MaximaMatrixDim:
        # Create the Maxima instruction
        maxExpr = 'result:%s(expand('%(numeric)
        func = 'newdet('
    else:
        maxExpr = detFunc() + 'result:%s(expand('%(numeric)
        func = 'det('
    if detP != None:
        maxExpr += '+' + func + sympy2maximaMatrix(M.Cramer(Iv, detP)) + ')'
    if detN != None:
        maxExpr += '-' + func + sympy2maximaMatrix(M.Cramer(Iv, detN)) + ')'
    maxExpr += '));'
    result = maxEval(maxExpr)
    try:
        return sp.sympify(result)
    except:
        print('Maxima error:', result)

def maxSolve(M, Iv, numeric = True):
    """
    Calculates M^(-1).Iv

    :param M: MNA matrix
    :type M: sympy.Matrix

    :param Iv: Vector with independent variables
    :type Iv: sympy.Matrix

    :param numeric: True will force Maxima to use (big) floats for numeric
                    values.
    :type numeric: bool

    :return: Network solution.
    :rtype: sympy.Matrix
    """
    if numeric:
        numeric = 'bfloat'
    else:
        numeric = ''
    maxExpr = 'M:' + sympy2maximaMatrix(M) + ';'
    maxExpr += 'Iv:' + sympy2maximaMatrix(Iv) + ';'
    maxExpr += 'result:%s(invert(M).Iv);'%(numeric)
    result = maxEval(maxExpr)
    try:
        return sp.sympify(result)
    except:
        print('Maxima error:', result)

def maxIntegrate(expr, var, start = None, stop = None, numeric = True):
    """
    Calculated definite or indefinite integral of 'expr'.

    :param expr: Integrand
    :type expr: sympy.Expr

    :param var: Integration variable
    :type var: sympy.Symbol, str

    :param start: Lower limit of the integral.
    :type start: Bool, int float, sympy.Expr

    :param stop: Upper limit of the integral.
    :type stop: Bool, int float, sympy.Expr

    :param numeric: True will force Maxima to use (big) floats for numeric
                    values.
    :type numeric: bool

    :return: Integral
    :rtype: sympy.Expr
    """
    if numeric:
        numeric = 'bfloat'
        expr=sp.N(expr)
    else:
        numeric = ''
    
    if start != None and stop != None:
        maxExpr = 'result:%s(integrate(%s, %s, %s, %s));'%(numeric, str(expr), str(var), str(start), str(stop))
    else:
        maxExpr = 'result:%s(integrate(%s, %s));'%(numeric, str(expr), str(var))
    result = maxEval(maxExpr)
    try:
        result = sp.sympify(result)
    except:
        print("Error: could not integrate expression: '{0}'.".format(str(expr)))
        result = sp.sympify('Error')
    return result

def equateCoeffs(protoType, transfer, noSolve = [], numeric=True):
    """
    Returns the solutions of the equation transferFunction = protoTypeFunction.

    Both transfer and prototype should be Laplace rational functions.
    Their numerators should be polynomials of the Laplace variable of equal
    order and their denominators should be polynomials of the Laplace variable
    of equal order.
    :note: if ini.maxSolve == True: Maxima CAS will be used as solver, else: sympy.
    :param protoType: Prototype rational expression of the Laplace variable
    :type protoType: sympy.Expr
    :param transfer:

    Transfer fucntion of which the parameters need to be
    solved. The numerator and the denominator of this rational
    expression should be of the same order as those of the
    prototype.

    :type transfer: sympy.Expr

    :param noSolve: List with variables (*str, sympy.Symbol*) that do not need
                    to be solved. These parameters will remain symbolic in the
                    solutions.

    :type noSolve: list

    :param numeric: True will force Maxima to use (big) floats for numeric
                    values.

    :type numeric: bool

    :return: Dictionary with key-value pairs:

             - key: name of the parameter (*sympy.Symbol*)
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
        eqn = sp.Eq(gainP, gainT)
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
            print('Error: could not solve equations.')
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

def rmsNoise(noiseResult, noise, fmin, fmax, source = None):
    """
    Calculates the RMS source-referred noise or detector-referred noise,
    or the contribution of a specific noise source to it.

    :param noiseResult: Results of the execution of an instruction with data type 'noise'.
    :type noiseResult: SLiCAPprotos.allResults

    :param noise: 'inoise' or 'onoise' for source-referred noise or detector-
                  referred noise, respectively.
    :type noise': str

    :param fmin: Lower limit of the frequency range in Hz.
    :type fmin: str, int, float, sp.Symbol

    :param fmax: Upper limit of the frequency range in Hz.
    :type fmax: str, int, float, sp.Symbol

    :param source: 'all' or refDes (ID) of a noise source of which the
                   contribution to the RMS noise needs to be evaluated.
    :return: RMS noise over the frequency interval.

             - An expression or value if parameter stepping of the instruction is disabled.
             - A list with expressions or values if parameter stepping of the instruction is enabled.
    :rtype: int, float, sympy.Expr, list
    """
    if fmin == None or fmax == None:
        print("Error in frequency range specification.")
        return None
    fMi = checkNumber(fmin)
    fMa = checkNumber(fmax)
    if fMi != None:
        fmin = fMi
    if fMa != None:
        fmax = fMa
    if fmin != None and fmax != None:
        if fMi != None and  fMa != None and fmin >= fmax:
            print("Error in frequency range specification.")
            return None
    if noiseResult.dataType != 'noise':
        print("Error: expected dataType noise, got: '{0}'.".format(noiseResult.dataType))
        rms = None
    keys = list(noiseResult.onoiseTerms.keys())
    if noise == 'inoise':
        if source == None:
            noiseData = noiseResult.inoise
        elif source in keys:
            noiseData = noiseResult.inoiseTerms[source]
        else:
            print("Error: unknown noise source: '{0}'.".format(source))
            rms = None
    elif noise == 'onoise':
        if source == None:
            noiseData = noiseResult.onoise
        elif source in keys:
            noiseData = noiseResult.onoiseTerms[source]
        else:
            print("Error: unknown noise source: '{0}'.".format(source))
            rms = None
    else:
        print("Error: unknown noise type: '{0}'.".format(noise))
        rms = None
    if type(noiseData) != list:
        noiseData = [noiseData]
    rms =  np.array([sp.N(sp.sqrt(maxIntegrate(noiseData[i], ini.frequency, start=fmin, stop=fmax, numeric=noiseResult.simType))) for i in range(len(noiseData))])
    if len(rms) == 1:
        rms = rms[0]
    return rms

if __name__ == '__main__':
    print(maxILT(1, ini.Laplace**2 + sp.Symbol('a')**2, numeric = False))
    proto_transfer = sp.sympify('0.3*(1/(1+s*0.6))')
    circuit_transfer = sp.sympify('R_1/(R_1 + R_2)/(1 + s*R_1*R_2/(R_1 + R_2)*10e-6)')
    circuit_component_values = equateCoeffs(proto_transfer, circuit_transfer)
    print(circuit_component_values)
    proto_transfer = sp.sympify('A/(1+s*tau)')
    circuit_component_values = equateCoeffs(proto_transfer, circuit_transfer, noSolve=['A','tau'], numeric=False)
    print(circuit_component_values)
