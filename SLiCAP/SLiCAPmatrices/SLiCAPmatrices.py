#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLiCAP module for building the MNA matrix and the associated vectors.

Imported by the module **SLiCAPpythonMaxima.py**
"""

from SLiCAP.SLiCAPprotos import *

def getValues(elmt, param, numeric, parDefs):
    """
    Returns the symbolic or numeric value of numerator and the denominator
    of a parameter of an element. This function is called by makeMatrices().

    :parm elmt: element object
    :type elmt: SLiCAPprotos.element

    :param param: parameter of interest ('value', 'noise', 'dc' or 'dcvar')
    :type param: str

    :param numeric: If True is uses full substitution and sp.N for converting
                    parameters to sympy floats
    :type numeric: bool

    :param parDefs: Dict with key value pairs:

                    - key  : parameter name (sympy.Symbol)
                    - value: numeric value of sympy expression
    :type parDefs: dict

    :return: Tuple with sympy expresssions or numeric values of the numerator
             and the denominator of the element parameter.
    :return type: tuple
    """
    if numeric == True:
        value = sp.N(fullSubs(elmt.params[param], parDefs))
    else:
        value = elmt.params[param]
    try:
        if ini.Laplace in value.atoms(sp.Symbol):
            (numer, denom) = value.as_numer_denom()
        else:
            numer = value
            denom = 1
    except:
        numer = value
        denom = 1
    return (numer, denom)

def getValue(elmt, param, numeric, parDefs):
    """
    Returns the symbolic or numeric value of a parameter of an element.

    This function is called by makeMatrices().

    :parm elmt: element object
    :type elmt: SLiCAPprotos.element

    :param param: parameter of interest ('value', 'noise', 'dc' or 'dcvar')
    :type param: str

    :param numeric: If True is uses full substitution and sympy.N for converting
                    parameters to sympy floats
    :type numeric: bool

    :param parDefs: Dict with key value pairs:

                    - key  : parameter name (sympy.Symbol)
                    - value: numeric value of sympy expression
    :type parDefs: dict

    :return: value: sympy expresssion or numeric value of the element parameter
    :return type: sympy.Expr, int, float, sympy.Float
    """
    if param not in list(elmt.params.keys()):
        return 0
    if numeric == True:
        value = sp.N(fullSubs(elmt.params[param], parDefs))
    else:
        value = elmt.params[param]
    return value

def makeMatrices(cir, parDefs, numeric, gainType, lgRef):
    """
    Returns the MNA matrix and the vector with dependent variables of a circuit.

    Modifications in the circuit object, necessary for calculation of different
    gain types are temporary. The circuit data before and after
    running 'makeMatrices' is the same:

    #. If gainType == 'asymptotic':

       - store the model of lgRef
       - modify the model of lgRef to 'N'
       - update depVars and varIndex
       - create the matrices
       - restore the model of lgRef
       - update depVars and varIndex

    #. If gainType == 'direct', 'loopgain' or 'servo':

       - store value of lgRef
       - set value of lgRef element to zero
       - create the matrices
       - restore the value of lgRef

       - loopgain and servo will be calculated with the output of lgRef
         as source and the input of lgRef as detector.

    #. If gainType == 'vi' or 'gain':

       - no alterations of the circuit need to be made

    :param cir: Circuit of which the matrices need to be returned.
    :type cir: SLiCAPprotos.circuit

    :param parDefs: Dict with key value pairs:

                    - key  : parameter name (sympy.Symbol)
                    - value: numeric value of sympy expression
    :type parDefs: dict


    :param numeric: If True is uses full substitution and sympy.N for converting
                    parameters to sympy floats
    :type numeric: bool

    :param gainType: Gain type of the instruction
    :type gainType: str

    :param lgRef: ID of the loop gain reference of the instruction
    :type lgRef: str

    :return: tuple with two sympy matrices:

             #. MNA matrix M
             #. Vector with dependent variables Dv
    :return type: tuple
    """
    if gainType == 'vi' or gainType == 'gain':
        pass
    elif gainType == 'direct' or gainType == 'loopgain' or gainType == 'servo':
        lgValue = cir.elements[lgRef].params['value']
        cir.elements[lgRef].params['value'] = 0
    varIndex = cir.varIndex
    dim = len(list(cir.varIndex.keys()))
    Dv = [0 for i in range(dim)]
    M  = [[0 for i in range(dim)] for i in range(dim)]
    for i in range(len(cir.depVars)):
        Dv[i] = sp.Symbol(cir.depVars[i])
    for el in list(cir.elements.keys()):
        elmt = cir.elements[el]
        if elmt.model == 'C':
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            value = getValue(elmt, 'value', numeric, parDefs)
            M[pos0][pos0] += value * ini.Laplace
            M[pos0][pos1] -= value * ini.Laplace
            M[pos1][pos0] -= value * ini.Laplace
            M[pos1][pos1] += value * ini.Laplace
        elif elmt.model == 'L':
            dVarPos = varIndex['I_'+ elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            value = getValue(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos0] += 1
            M[dVarPos][pos1] -= 1
            M[dVarPos][dVarPos] -= value * ini.Laplace
        elif elmt.model == 'R':
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            value = 1/getValue(elmt, 'value', numeric, parDefs)
            M[pos0][pos0] += value
            M[pos0][pos1] -= value
            M[pos1][pos0] -= value
            M[pos1][pos1] += value
        elif elmt.model == 'r':
            dVarPos = varIndex['I_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            value = getValue(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos0] += 1
            M[dVarPos][pos1] -= 1
            M[dVarPos][dVarPos] -= value
        elif elmt.model == 'E':
            dVarPos = varIndex['Io_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            (numer, denom) = getValues(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos0] += denom
            M[dVarPos][pos1] -= denom
            M[dVarPos][pos2] -= numer
            M[dVarPos][pos3] += numer
        elif elmt.model == 'EZ':
            dVarPos = varIndex['Io_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            (numer, denom) = getValues(elmt, 'value', numeric, parDefs)
            (zoN, zoD) = getValues(elmt, 'zo', numeric, parDefs)
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos0] += denom * zoD
            M[dVarPos][pos1] -= denom * zoD
            M[dVarPos][pos2] -= numer * zoD
            M[dVarPos][pos3] += numer * zoD
            M[dVarPos][dVarPos] -= zoN * denom
        elif elmt.model == 'F':
            dVarPos = varIndex['Ii_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            (numer, denom) = getValues(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPos] += numer
            M[pos1][dVarPos] -= numer
            M[pos2][dVarPos] += denom
            M[pos3][dVarPos] -= denom
            M[dVarPos][pos2] += 1
            M[dVarPos][pos3] -= 1
        elif elmt.model == 'g':
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            value = getValue(elmt, 'value', numeric, parDefs)
            M[pos0][pos2] += value
            M[pos0][pos3] -= value
            M[pos1][pos2] -= value
            M[pos1][pos3] += value
        elif elmt.model == 'G':
            dVarPos = varIndex['Io_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            (numer, denom) = getValues(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos2] += numer
            M[dVarPos][pos3] -= numer
            M[dVarPos][dVarPos] -= denom
        elif elmt.model == 'H':
            dVarPosO = varIndex['Io_' + elmt.refDes]
            dVarPosI = varIndex['Ii_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            (numer, denom) = getValues(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPosO] += 1
            M[pos1][dVarPosO] -= 1
            M[pos2][dVarPosI] += 1
            M[pos3][dVarPosI] -= 1
            M[dVarPosI][pos2] += 1
            M[dVarPosI][pos3] -= 1
            M[dVarPosO][pos0] += denom
            M[dVarPosO][pos1] -= denom
            M[dVarPosO][dVarPosI] -= numer
        elif elmt.model == 'HZ':
            dVarPosO = varIndex['Io_' + elmt.refDes]
            dVarPosI = varIndex['Ii_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            (numer, denom) = getValues(elmt, 'value', numeric, parDefs)
            (zoN, zoD) = getValues(elmt, 'zo', numeric, parDefs)
            M[pos0][dVarPosO] += 1
            M[pos1][dVarPosO] -= 1
            M[pos2][dVarPosI] += 1
            M[pos3][dVarPosI] -= 1
            M[dVarPosI][pos2] += 1
            M[dVarPosI][pos3] -= 1
            M[dVarPosO][pos0] += denom * zoD
            M[dVarPosO][pos1] -= denom * zoD
            M[dVarPosO][dVarPosI] -= numer * zoD
            M[dVarPosO][dVarPosO] -= zoN * denom
        elif elmt.model == 'N':
            dVarPos = varIndex['Io_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos2] += 1
            M[dVarPos][pos3] -= 1
        elif elmt.model == 'T':
            dVarPos = varIndex['Io_' + elmt.refDes]
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            value = getValue(elmt, 'value', numeric, parDefs)
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[pos2][dVarPos] -= value
            M[pos3][dVarPos] += value
            M[dVarPos][pos0] += 1
            M[dVarPos][pos1] -= 1
            M[dVarPos][pos2] -= value
            M[dVarPos][pos3] += value
        elif elmt.model == 'V':
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            dVarPos = varIndex['I_' + elmt.refDes]
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos0] += 1
            M[dVarPos][pos1] -= 1
        elif elmt.model == 'VZ':
            (zoN, zoD) = getValues(elmt, 'zo', numeric, parDefs)
            pos1 = varIndex[elmt.nodes[1]]
            pos0 = varIndex[elmt.nodes[0]]
            M[pos0][dVarPos] += 1
            M[pos1][dVarPos] -= 1
            M[dVarPos][pos0] += zoD
            M[dVarPos][pos1] -= zoD
            M[dVarPos][dVarPos] -= zoN
        elif elmt.model == 'W':
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            pos2 = varIndex[elmt.nodes[2]]
            pos3 = varIndex[elmt.nodes[3]]
            value = getValue(elmt, 'value', numeric, parDefs)
            M[pos0][pos2] += value
            M[pos0][pos3] -= value
            M[pos1][pos2] -= value
            M[pos1][pos3] += value
            M[pos2][pos0] -= value
            M[pos2][pos1] += value
            M[pos3][pos0] += value
            M[pos3][pos1] -= value
        elif elmt.model == 'K':
            refPos1 = varIndex['I_' + elmt.refs[0]]
            refPos0 = varIndex['I_' + elmt.refs[1]]
            ind0    = getValue(cir.elements[elmt.refs[0]].params['value'])
            ind1    = getValue(cir.elements[elmt.refs[1]].params['value'])
            value = getValue(elmt, 'value', numeric, parDefs)
            value = value * ini.Laplace * sqrt(ind0 * ind1)
    M = matrix(M)
    gndPos = varIndex['0']
    M.row_del(gndPos)
    M.col_del(gndPos)
    Dv = matrix(Dv)
    Dv.row_del(gndPos)
    # Restore circuit data
    if gainType == 'direct' or gainType == 'loopgain' or gainType == 'servo':
        cir.elements[lgRef].params['value'] = lgValue
    return (M, Dv)

def makeSrcVector(cir, parDefs, elid, value = 'id', numeric = True):
    """
    Creates the vector with independent variables.
    The vector can be created for a single independent variable or for all.

    This can be used for determination of a transfer using Cramer's rule.

    If a single variable is used, this vector and Cramer's rule can be used as
    an alternative for calculation cofactors:

    The refDes of the independent variable (source) is substituted in the vecor
    with independent variables (value = 'id'). This vector is then substituted
    in the detector col, of the MNA matrix.  After calculation of the
    determinant of this modified matrix, the result is divided by refDes.

    This method is used for determination of gain factors for noise sources
    and for DC variance sources.

    :param cir: Circuit of which the matrices need to be returned.
    :type cir: SLiCAPprotos.circuit

    :param parDefs: Dict with key value pairs:

                    - key  : parameter name (sympy.Symbol)
                    - value: numeric value of sympy expression
    :type parDefs: dict

    :param elid: Refdes (ID) of a source to be included in this vector; 'all'
                 for all sources.
    :type elid: str

    :param numeric: If True is uses full substitution and sympy.N for converting
                    parameters to sympy floats
    :type numeric: bool

    :return: Iv: vector with in dependent variables
    :return type: sympy.Matrix
    """
    # varIndex holds the position of dependent variables in the matrix.
    varIndex = cir.varIndex
    dim = len(list(cir.varIndex.keys()))
    # Define the vector
    Iv = [0 for i in range(dim)]
    # Select the elements of interest
    if elid == 'all':
        elements = [cir.elements[key] for key in list(cir.elements.keys())]
    elif elid in list(cir.elements.keys()):
        elements = [cir.elements[elid]]
    for elmt in elements:
        # subsititute the element parameters of interest in the vecor Iv
        if value == 'id':
            if elid == 'all':
                val = sp.Symbol(elmt.refDes)
            else:
                val = 1
        elif value == 'value':
            val = getValue(elmt, 'value', numeric, parDefs)
        elif value == 'noise':
            val = getValue(elmt, 'noise', numeric, parDefs)
        elif value == 'dc':
            val = getValue(elmt, 'dc', numeric, parDefs)
        elif value == 'dcvar':
            val = getValue(elmt, 'dcvar', numeric, parDefs)
        if elmt.model == 'I':
            pos0 = varIndex[elmt.nodes[0]]
            pos1 = varIndex[elmt.nodes[1]]
            Iv[pos0] -= val
            Iv[pos1] += val
        elif elmt.model == 'V':
            dVarPos = varIndex['I_' + elmt.refDes]
            Iv[dVarPos] += val
    gndPos = varIndex['0']
    Iv = matrix(Iv)
    Iv.row_del(gndPos)
    return Iv

if __name__ == "__main__":
    s = ini.Laplace

    MNA = matrix([[5.0e-12*s + 0.01, 0, 0, -5.0e-12*s - 0.01, 0, 0, 0, 0, 1],
                  [0, 1.98e-11*s + 0.0001, -1.2e-11*s, -1.8e-12*s - 1.0e-5, 0, 0, 0, 0, 0],
                  [0, -1.2e-11*s, 2.8e-11*s + 0.001, 0, -1.0e-11*s - 0.001, 0, 0, -1, 0],
                  [-5.0e-12*s - 0.01, -1.8e-12*s - 1.0e-5, 0, 1.0068e-9*s + 0.01101, 0, 0, 1, 0, 0],
                  [0, 0, -1.0e-11*s - 0.001, 0, 1.0e-11*s + 0.001, 1, 0, 1, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0, -1.0e-6*s, -3.1623e-11*s, 0],
                  [0, 0, -1, 0, 1, 0, -3.1623e-11*s, -1.0e-9*s, 0],
                  [2.048e-20*s**3 + 2.688e-11*s**2 + 0.0016*s + 1, 0, 0, 0, 0, 0, 0, 0, 0]])

    print(MNA.determinant())