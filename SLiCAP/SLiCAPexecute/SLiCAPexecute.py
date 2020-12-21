#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLiCAP module with functions for execution of instructions.

Imported by the module **SLiCAPinstruction.py**.

Execution **instruction.execute()** proceeds as follows:

#. The instruction settings will be checked for completeness and consistency
#. If no errors are found **doInstruction(<allResults obj>)** performs the
   actual execution of the instruction
"""

from SLiCAP.SLiCAPyacc import *

def doInstruction(instObj):
    """
    Executes the instruction with or without parameter stepping.

    Called by **instruction.execute()**. This function should not be called
    directly by the user.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`

    :return: **allResults()** object that holds instruction data.
    :return type: **allResults()** object
    """
    if instObj.gainType == 'asymptotic':
        # The reference variable needs to replaced with a nullor and both the 
        # self.circuit.depVars and self.varIndex need to be changed accordingly.
        # Old values need to be restored after execution of the instruction.
        oldLGrefElement = instObj.circuit.elements[instObj.lgRef]
        newLGrefElement = element()
        newLGrefElement.nodes = oldLGrefElement.nodes
        newLGrefElement.model = 'N'
        newLGrefElement.type = 'N'
        newLGrefElement.refDes = oldLGrefElement.refDes
        instObj.circuit.elements[instObj.lgRef] = newLGrefElement
        instObj.circuit = updateCirData(instObj.circuit)
    if instObj.step:
        if ini.stepFunction:
            # Create a substitution dictionary that does not contain step parameters
            subsDict = {}
            if instObj.stepMethod == 'array':
                for key in list(instObj.circuit.parDefs.keys()):
                    if key not in instObj.stepVars:
                        subsDict[key] = instObj.circuit.parDefs[key]
            else:
                for key in list(instObj.circuit.parDefs.keys()):
                    if key != instObj.stepVar:
                        subsDict[key] = instObj.circuit.parDefs[key]
            instObj.parDefs = subsDict
            # Do the instruction
            instObj.M, instObj.Dv = makeMatrices(instObj.circuit, instObj.parDefs, instObj.numeric, instObj.gainType, instObj.lgRef)
            # Do stepping by means of substitution in the numerator and denominator
            if instObj.dataType == 'poles':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                # pz analysis is numeric so better lambdify!
                for poly in denoms:
                    instObj.poles.append(numRoots(poly, ini.Laplace))
                instObj.zeros = []
            elif instObj.dataType == 'zeros':
                numer = doNumer(instObj)
                numers = stepFunctions(instObj, numer)
                for poly in numers:
                    instObj.zeros.append(numRoots(poly, ini.Laplace))
                instObj.poles = []
            elif instObj.dataType == 'pz':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                numer = doNumer(instObj)
                numers = stepFunctions(instObj, numer)
                instObj.poles = []
                instObj.zeros = []
                instObj.DCvalue = []
                for i in range(len(denoms)):
                    poles = numRoots(denoms[i], ini.Laplace)
                    zeros = numRoots(numers[i], ini.Laplace)
                    (poles, zeros) = cancelPZ(poles, zeros)
                    instObj.poles.append(poles)
                    instObj.zeros.append(zeros)
                    try:
                        # Lets try a real limit with Maxima CAS
                        instObj.DCvalue.append(maxLimit(numers[i]/denoms[i], str(ini.Laplace), '0', 'plus'))
                    except:
                        # If not just substitute s=0 with Sympy
                        instObj.DCvalue.append(sp.N(sp.Subs(numers[i]/denoms[i], ini.Laplace, 0)))
            elif instObj.dataType == 'step':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                numer = doNumer(instObj)
                numers = stepFunctions(instObj, numer)
                for i in range(len(denoms)):
                    instObj.stepResp.append(maxILT(numers[i], denoms[i]*ini.Laplace, numeric = instObj.numeric))
            elif instObj.dataType == 'impulse' or instObj.dataType == 'time':
                denom = doDenom(instObj)
                numer = doNumer(instObj)
                if instObj.gainType == 'vi':
                    nNum, nDen = sp.fraction(numer)
                    numer = nNum
                    denom = denom*nDen
                denoms = stepFunctions(instObj, denom)
                numers = stepFunctions(instObj, numer)
                for i in range(len(denoms)):
                    try:
                        instObj.stepResp.append(maxILT(numers[i], denoms[i], numeric = instObj.numeric))
                    except:
                        print("Warning: could not calculate the unit impulse response.")
            elif instObj.dataType == 'numer':
                numer = doNumer(instObj)
                instObj.numer = stepFunctions(instObj, numer)
            elif instObj.dataType == 'denom':
                denom = doDenom(instObj)
                instObj.denom = stepFunctions(instObj, denom)
            elif instObj.dataType == 'laplace':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                numer = doNumer(instObj) # works for all gain types
                numers = stepFunctions(instObj, numer)
                instObj.laplace = []
                for i in range(len(denoms)):
                    if ini.normalize == True:
                        instObj.laplace.append(simplify(numers[i]/denoms[i], method = 'normalize'))
                    elif ini.factor == True:
                        instObj.laplace.append(simplify(numers[i]/denoms[i], method = 'factor'))
                    elif ini.simplify == True:
                        instObj.laplace.append(simplify(numers[i]/denoms[i], method = 'fraction'))
                    else:
                        instObj.laplace.append(numers[i]/denoms[i])
            elif instObj.dataType == 'solve':
                sol = doSolve(instObj)
                instObj.solve = stepFunctions(instObj, sol)
                for i in range(len(instObj.solve)):
                    if ini.normalize == True:
                        instObj.solve[i] = simplify(instObj.solve[i], method = 'normalize')
                    elif ini.factor == True:
                        instObj.solve[i] = simplify(instObj.solve[i], method = 'factor')
                    elif ini.simplify == True:
                        instObj.solve[i] = simplify(instObj.solve[i], method = 'fraction')
                    else:
                        instObj.laplace.append(numers[i]/denoms[i])
            elif instObj.dataType == 'noise':
                detP, detN, srcP, srcN = makeSrcDetPos(instObj)
                if instObj.source != None:
                    # Calculate the squared gain from source to detector as a
                    # function of ini.frequency
                    numer = maxNumer(instObj.M, detP, detN, srcP, srcN, numeric = instObj.numeric)
                    numer = assumeRealParams(numer.subs(ini.Laplace, 2*sp.pi*sp.I*ini.frequency))
                    nR, nI = numer.as_real_imag()
                    numer2 = nR**2 + nI**2
                    #numer2 = sp.Abs(numer)**2
                    denom = maxDet(instObj.M, numeric=instObj.numeric)
                    denom = assumeRealParams(denom.subs(ini.Laplace, 2*sp.pi*sp.I*ini.frequency))
                    dR, dI = denom.as_real_imag()
                    denom2 = dR**2 + dI**2
                    gain2 = numer2/denom2
                    #denom2 = sp.Abs(denom)**2
                    gain2 = clearAssumptions(simplify(numer2/denom2, method = 'fraction'))
                # Calculate the contributions of each noise source to the
                # spectral density of the total output noise
                onoiseTerms = doNoise(instObj, detP, detN, denom2)
                # apply function stepping
                for elID in list(onoiseTerms.keys()):
                    if instObj.source != None:
                        instObj.inoiseTerms[elID] = stepFunctions(instObj, onoiseTerms[elID]/gain2)
                    instObj.onoiseTerms[elID] = stepFunctions(instObj, onoiseTerms[elID])
                    instObj.snoiseTerms[elID] = stepFunctions(instObj, instObj.circuit.elements[elID].params['noise'])
                numRuns = len(instObj.onoiseTerms[elID])
                for i in range(numRuns):
                    # calcuate onoise and inoise for each run
                    onoise = 0
                    inoise = 0
                    for elID in list(onoiseTerms.keys()):
                        onoise += instObj.onoiseTerms[elID][i]
                        if instObj.source != None:
                            inoise += instObj.inoiseTerms[elID][i]
                    instObj.onoise.append(simplify(onoise, method = 'fraction'))
                    if instObj.source != None:
                        instObj.inoise.append(simplify(inoise, method = 'fraction'))
            elif instObj.dataType == 'dc':
                detP, detN, srcP, srcN = makeSrcDetPos(instObj)
                dc = doDC(instObj, detP, detN)
                instObj.dc = stepFunctions(instObj, dc)
            elif instObj.dataType == 'dcsolve':
                dcSolve = doSolveDC(instObj)
                instObj.dcSolve = stepFunctions(instObj, dcSolve)
            elif instObj.dataType == 'dcvar':
                detP, detN, srcP, srcN = makeSrcDetPos(instObj)
                if instObj.source != None:
                    # Calculate the squared DC gain from source to detector
                    M = instObj.M.subs(ini.Laplace, 0)
                    numer = maxNumer(M, detP, detN, srcP, srcN, numeric = instObj.numeric)
                    denom = maxDet(M, numeric = instObj.numeric)
                    gain2 = simplify((numer/denom)**2, method = 'fraction')
                # Calculate the contributions of each variance source to the
                # variance at the detector
                ovarTerms, dcSol = doDCvar(instObj, detP, detN)
                # apply function stepping
                for elID in list(ovarTerms.keys()):
                    if instObj.source != None:
                        instObj.ivarTerms[elID] = stepFunctions(instObj, simplify(ovarTerms[elID]/gain2, method = 'fraction'))
                    instObj.ovarTerms[elID] = stepFunctions(instObj, ovarTerms[elID])
                    instObj.svarTerms[elID] = stepFunctions(instObj, instObj.circuit.elements[elID].params['dcvar'])
                numRuns = len(instObj.ovarTerms[elID])
                for i in range(numRuns):
                    # calcuate the total ovar and the total ivar for each run
                    ovar = 0
                    ivar = 0
                    for elID in list(ovarTerms.keys()):
                        ovar += instObj.ovarTerms[elID][i]
                        if instObj.source != None:
                            ivar += instObj.ivarTerms[elID][i]
                    instObj.ovar.append(simplify(ovar, method = 'fraction'))
                    if instObj.source != None:
                        instObj.ivar.append(simplify(ivar, method = 'fraction'))
        else:
            # Create a deep copy of the substitution dictionary
            subsDict = {}
            for key in list(instObj.circuit.parDefs.keys()):
                subsDict[key] = instObj.circuit.parDefs[key]
            instObj.parDefs = subsDict
            # For each set of step variable create the numeric substitution
            # dictionary, make the matrices and do the non-stepped instruction.
            if instObj.stepMethod != 'array':
                for stepVal in instObj.stepList:
                    instObj.parDefs[instObj.stepVar] = stepVal
                    doDataType(instObj)
            else:
                # array stepping, number of steps is length of lists in stepArray
                for i in range(len(instObj.stepArray[0])):
                    # substitute the i-th value for each step variable in the
                    # .parDefs dictionary.
                    for j in range(len(instObj.stepVars)):
                        instObj.parDefs[instObj.stepVars[j]] = instObj.stepArray[j][i]
                    doDataType(instObj)
    else:
        # Create a deep copy of de circuit parameter definitions and do the 
        # non-stepped instruction.
        instObj.parDefs = {}
        for key in list(instObj.circuit.parDefs.keys()):
            instObj.parDefs[key] = instObj.circuit.parDefs[key]
        doDataType(instObj)
    if instObj.gainType == 'asymptotic':
        # Restore the original loop gain reference element
        instObj.circuit.elements[instObj.lgRef] = oldLGrefElement
        instObj.circuit = updateCirData(instObj.circuit)
    return instObj

def stepFunctions(instObj, function):
    """
    Substitutes values for step parameters in functions and returns a list
    of functions with these substitutions.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`
    :param function:
    :type function: sympy.Expr

    :return: List with functions (*sympy.Expr*). The number of
             functions equals the number of steps. Function i equals
             the input function in which the step variable has been
             replaced with its i-th step value.
    :return type: list
    """
    if instObj.stepMethod == 'array':
        functions = []
        for i in range(len(instObj.stepArray[0])):
            subsList = []
            for j in range(len(instObj.stepVars)):
                subsList.append((instObj.stepVars[j], instObj.stepArray[j][i]))
            functions.append(function.subs(subsList))
    else:
        functions = [function.xreplace({instObj.stepVar: instObj.stepList[i]}) for i in range(len(instObj.stepList))]
    return functions

def doDataType(instObj):
    """
    Executes the instruction without parameter stepping.

    #. It builds the matrices in accordance with the specified gain type
    #. It executes instruction for the specified dataype

    :param instObj: **allResults()** objectthat holds instruction data.
    :type instObj: :class:`allResult()`

    :return: **allResults()** object that holds instruction data
    :return type: **allResults()** object
    """
    instObj.M, instObj.Dv = makeMatrices(instObj.circuit, instObj.parDefs, instObj.numeric, instObj.gainType, instObj.lgRef)
    if instObj.dataType == 'matrix':
        instObj.Iv = makeSrcVector(instObj.circuit, instObj.parDefs, 'all', value = 'value', numeric=instObj.numeric)
    elif instObj.dataType == 'poles':
        if instObj.step:
            instObj.poles.append(doPoles(instObj))
        else:
            instObj.poles = doPoles(instObj)
            instObj.DCvalue = None
    elif instObj.dataType == 'zeros':
        if instObj.step:
            instObj.zeros.append(doZeros(instObj))
        else:
            instObj.zeros = doZeros(instObj)
            instObj.DCvalue = None
    elif instObj.dataType == 'pz':
        (poles, zeros, DCvalue) = doPZ(instObj)
        if instObj.step:
            instObj.poles.append(poles)
            instObj.zeros.append(zeros)
            instObj.DCvalue.append(DCvalue)
        else:
            instObj.poles = poles
            instObj.zeros = zeros
            instObj.DCvalue = DCvalue
    elif instObj.dataType == 'denom':
        if instObj.step:
            instObj.denom.append(doDenom(instObj))
        else:
            instObj.denom = doDenom(instObj)
    elif instObj.dataType == 'numer':
        if instObj.step:
            instObj.numer.append(doNumer(instObj))
        else:
            instObj.numer = doNumer(instObj)
    elif instObj.dataType == 'laplace':
        if instObj.step:
            instObj.laplace.append(doLaplace(instObj))
        else:
            instObj.laplace = doLaplace(instObj)         
    elif instObj.dataType == 'step':
        instObj.stepResp = maxILT(doNumer(instObj), doDenom(instObj)*ini.Laplace, numeric = instObj.numeric)
    elif instObj.dataType == 'impulse' or instObj.dataType == 'time':
        numer = doNumer(instObj)
        denom = doDenom(instObj)
        if instObj.gainType == 'vi':
            nNum, nDen = sp.fraction(numer)
            numer = nNum
            denom = sp.expand(denom*nDen)
        if instObj.dataType == 'impulse':
            try:
                instObj.impulse = maxILT(numer, denom, numeric = instObj.numeric)
            except:
                print("Warning: could not calculate the unit impulse response.")
        elif instObj.dataType == 'time':
            try:
                instObj.time = maxILT(numer, denom, numeric = instObj.numeric)
            except:
                print("Warning: could not calculate the time response.")
    elif instObj.dataType == 'solve':
        if instObj.step:
            instObj.solve.append(doSolve(instObj))
        else:
            instObj.solve = doSolve(instObj)
    elif instObj.dataType == 'noise':
        # Calculate the contributions of each noise source to the
        # spectral density of the total output noise
        detP, detN, srcP, srcN = makeSrcDetPos(instObj)
        onoiseTerms = doNoise(instObj, detP, detN, None)
        inoiseTerms = {}
        snoiseTerms = {}
        onoise      = 0
        alreadyKeys = list(instObj.onoiseTerms.keys())
        if instObj.source != None:
            # Calculate the squared gain from source to detector as a
            # function of ini.frequency
            numer = assumeRealParams(maxNumer(instObj.M, detP, detN, srcP, srcN).subs(ini.Laplace, ini.frequency*2*sp.pi*sp.I))
            denom = assumeRealParams(maxDet(instObj.M).subs(ini.Laplace, ini.frequency*2*sp.pi*sp.I))
            nR, nI = numer.as_real_imag()
            numer2 = nR**2 + nI**2
            dR, dI = denom.as_real_imag()
            denom2 = dR**2 + dI**2
            gain2 = numer2/denom2
            gain2 = clearAssumptions(gain2)
            inoise = 0
        for key in list(onoiseTerms.keys()):
            onoise += onoiseTerms[key]
            snoiseTerms[key] = instObj.circuit.elements[key].params['noise']
            if instObj.source != None:
                inoiseTerms[key] = simplify(onoiseTerms[key]/gain2, method = 'fraction')
                inoise += inoiseTerms[key]
            if instObj.step:
                if key in alreadyKeys:
                    instObj.onoiseTerms[key].append(onoiseTerms[key])
                    instObj.snoiseTerms[key].append(snoiseTerms[key])
                    if instObj.source != None:
                        instObj.inoiseTerms[key].append(inoiseTerms[key])
                else:
                    instObj.onoiseTerms[key] = [onoiseTerms[key]]
                    instObj.snoiseTerms[key] = [snoiseTerms[key]]
                    if instObj.source != None:
                        instObj.inoiseTerms[key] = [inoiseTerms[key]]
            else:
                instObj.onoiseTerms[key] = onoiseTerms[key]
                instObj.snoiseTerms[key] = snoiseTerms[key]
                if instObj.source != None:
                    instObj.inoiseTerms[key] = inoiseTerms[key]
        if instObj.step:
            instObj.onoise.append(simplify(onoise, method = 'fraction'))
            if instObj.source != None:
                instObj.inoise.append(simplify(inoise, method = 'fraction'))
        else:
            instObj.onoise = onoise
            if instObj.source != None:
                instObj.inoise = inoise
    elif instObj.dataType == 'dc':
        (detP, detN, srcP, srcN) = makeSrcDetPos(instObj)
        if instObj.step:
            instObj.dc.append(doDC(instObj, detP, detN))
        else:
            detP, detN, srcP, srcN = makeSrcDetPos(instObj)
            instObj.dc= doDC(instObj, detP, detN)
    elif instObj.dataType == 'dcsolve':
        if instObj.step:
            instObj.dcSolve.append(doSolveDC(instObj))
        else:
            instObj.dcSolve = doSolveDC(instObj)
    elif instObj.dataType == 'dcvar':
        # Calculate the contributions of each dcvar source to the
        # variance at the detector
        detP, detN, srcP, srcN = makeSrcDetPos(instObj)
        ovarTerms, dcSol = doDCvar(instObj, detP, detN)
        ivarTerms = {}
        svarTerms = {}
        ovar      = 0
        alreadyKeys = list(instObj.ovarTerms.keys())
        if instObj.source != None:
            # Calculate the squared DC gain from source to detector
            M = instObj.M.subs(ini.Laplace, 0)
            numer2 = (maxNumer(M, detP, detN, srcP, srcN, numeric = instObj.numeric))**2
            denom2 = (maxDet(M, numeric = instObj.numeric))**2
            gain2 = simplify(numer2/denom2, method = 'fraction')
            ivar = 0
        for key in list(ovarTerms.keys()):
            ovar += ovarTerms[key]
            svarTerms[key] = instObj.circuit.elements[key].params['dcvar']
            if instObj.source != None:
                ivarTerms[key] = simplify(ovarTerms[key]/gain2, method = 'fraction')
                ivar += ivarTerms[key]
            if instObj.step:
                if key in alreadyKeys:
                    instObj.ovarTerms[key].append(ovarTerms[key])
                    instObj.svarTerms[key].append(svarTerms[key])
                    if instObj.source != None:
                        instObj.ivarTerms[key].append(ivarTerms[key])
                else:
                    instObj.ovarTerms[key] = [ovarTerms[key]]
                    instObj.svarTerms[key] = [svarTerms[key]]
                    if instObj.source != None:
                        instObj.ivarTerms[key] = [ivarTerms[key]]
            else:
                instObj.ovarTerms[key] = ovarTerms[key]
                instObj.svarTerms[key] = svarTerms[key]
                if instObj.source != None:
                    instObj.ivarTerms[key] = ivarTerms[key]
        if instObj.step:
            instObj.ovar.append(simplify(ovar, method = 'fraction'))
            if instObj.source != None:
                instObj.ivar.append(simplify(ivar, method = 'fraction'))
            instObj.dcSolve.append(dcSol)
        else:
            instObj.ovar = ovar
            if instObj.source != None:
                instObj.ivar = simplify(ivar, method = 'fraction')
            instObj.dcSolve = dcSol
    return instObj

def doDenom(instObj):
    """
    Calculates the denominator of a transfer by evaluating the determinant
    of the MNA matrix.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`

    :return: denominator of a transfer or a detector voltage or current:

             - gain type = 'vi', 'gain', 'direct', 'asymptotic':

               dDeterminant of the MNA matrix for that gain type

             - gain type = 'loopgain':

               Determinant of the MNA matrix for gain type 'loopgain' multiplied
               with the denominator of the gain of the loop gain reference.

             - gain type = 'servo':

               Determinant of the MNA matrix for gain type 'loopgain' multiplied
               with the denominator of the gain of the loop gain reference, plus
               the numerator of the loop gain. The latter one is calculated as
               the product of the sum of cofactors of the MNA matrix for gain
               type 'loopgain' and the numerator of the gain of the loop gain
               reference.

    :return type: sympy.Expr
    """
    denom = maxDet(instObj.M)
    if instObj.gainType == 'servo':
        (detP, detN, srcP, srcN) = makeSrcDetPos(instObj)
        numer = maxNumer(instObj.M, detP, detN, srcP, srcN)
        (lgNumer, lgDenom) = sp.fraction(sp.together(lgValue(instObj)))
        numer = numer * -lgNumer
        denom = denom * lgDenom + numer
    elif instObj.gainType == 'loopgain':
        (lgNumer, lgDenom) = sp.fraction(sp.together(lgValue(instObj)))
        denom = denom * lgDenom
    return sp.collect(denom, ini.Laplace)

def doPoles(instObj):
    """
    Calculates the numeric roots of the denominator of a transfer.

    It first calls **execute.doDenom()** to calculate the denominator of the
    transfer defined by the gain type. It then calculates the numerical roots
    by calling **SLiCAPmath.numRoots()**.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`

    :return: list with numerical roots of the denominator of a transfer
    :return type: list
    """
    denom = sp.expand(sp.collect(doDenom(instObj).evalf(), ini.Laplace))
    return numRoots(denom, ini.Laplace)

def lgValue(instObj):
    """
    Calculates the corrected gain of the loop gain reference.

    In case of a loop gain reference of the type EZ and HZ the calculation of
    the loop gain is performed as if a current source was placed in parallel
    with the output impedance (zo) of this controlled source (Norton equivalent
    representation). The value of this current source is that of the loop gain
    reference divided by the output impedance of the device.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`

    :return: Gain of the loop gain reference, modified in a Norton equivalent
             in cases in which the model of the loop gain reference is 'EZ' or
             'HZ'.

    :return type: sympy.
    """
    lgRef = instObj.circuit.elements[instObj.lgRef]
    if lgRef.model == 'g':
        value = lgRef.params['value']
    elif lgRef.model == 'E':
        value = lgRef.params['value']
    elif lgRef.model == 'EZ':
        if lgRef.params['zo'] != 0:
            value = lgRef.params['value']/lgRef.params['zo']
        else:
            value = lgRef.params['value']
    elif lgRef.model == 'HZ':
        if lgRef.params['zo'] != 0:
            value = lgRef.params['value']/lgRef.params['zo']
        else:
            value = lgRef.params['value']
    elif lgRef.model == 'H':
        value = lgRef.params['value']
    elif lgRef.model == 'F':
        value = lgRef.params['value']
    elif lgRef.model == 'G':
        value = lgRef.params['value']
    if instObj.simType == 'numeric':
        value = fullSubs(value, instObj.parDefs)
    return value

def makeSrcDetPos(instObj):
    """
    Returns the number of the source row(s) and detector colum(s) for
    calculation of cofactors or for application of Cramer's rule.

    If the gain type is 'loopgain' or 'servo', the source and the detector are
    taken at the input and the output of the loop gain reference.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`

    :return: tuple: (detP, detN, srcP, srcN):

            - detP (*None, int*): number of the row of the vector with dependent
              variables that corresponds with the positive detector
            - detN (*None, int*): number of the row of the vector with dependent
              variables that corresponds with the negative detector
            - srcP (*None, int*): number of the row of the vector with dependent
              variables that corresponds with the positive source
            - srcN (*None, int*): number of the row of the vector with dependent
              variables that corresponds with the negative source

    :return type: tuple
    """
    detectors = []
    for var in instObj.circuit.depVars:
        if var != 'V_0':
            detectors.append(var)
    if instObj.gainType == 'loopgain' or instObj.gainType == 'servo':
        lgRef = instObj.circuit.elements[instObj.lgRef]
        if lgRef.model == 'E':
            # The detector nodes are the inP and inN nodes of the VCVS
            srcP = detectors.index('Io_' + instObj.lgRef)
            srcN = None
            # The source row is that of the current through the controlled
            # voltage source
            if lgRef.nodes[2] == '0':
                detP = None
            else:
                detP = detectors.index('V_' + lgRef.nodes[2])
            if lgRef.nodes[3] == '0':
                detN = None
            else:
                detN = detectors.index('V_' + lgRef.nodes[3])
        elif lgRef.model == 'EZ':
            # The detector nodes are the inP and inN nodes of the VCVS
            if lgRef.nodes[2] == '0':
                detP = None
            else:
                detP = detectors.index('V_' + lgRef.nodes[2])
            if lgRef.nodes[3] == '0':
                detN = None
            else:
                detN = detectors.index('V_' + lgRef.nodes[3])
            if lgRef.params['zo'] != 0:
                # A current source in parallel with Zo, hence flowing from the
                # outN node to the outP node of the device is the new source.
                # The gain of the reference variable needs to be divided by the
                # value of Zo.
                if lgRef.nodes[0] == '0':
                    srcP = None
                else:
                    srcP = detectors.index('V_' + lgRef.nodes[0])
                if lgRef.nodes[1] == '0':
                    srcN = None
                else:
                    srcN = detectors.index('V_' + lgRef.nodes[1])
            else:
                # If Zo is zero the method for model 'E' must be applied.
                srcP = detectors.index('Io_' + instObj.lgRef)
                srcN = None
        elif lgRef.model == 'F':
            # The detector row is that of the input current of the CCCS
            detP = detectors.index('Ii_' + instObj.lgRef)
            detN = None
            # The source rows correspond with those of the nodes of the
            # controlled current source at the output of the device.
            if lgRef.nodes[1] == '0':
                srcP = None
            else:
                srcP = detectors.index('V_' + lgRef.nodes[1])
            if lgRef.nodes[0] == '0':
                srcN = None
            else:
                srcN = detectors.index('V_' + lgRef.nodes[0])
        elif lgRef.model == 'G':
            # The detector rows correspond with those of the input nodes
            # of the VCCS.
            if lgRef.nodes[2] == '0':
                detP = None
            else:
                detP = detectors.index('V_' + lgRef.nodes[2])
            if lgRef.nodes[3] == '0':
                detN = None
            else:
                detN = detectors.index('V_' + lgRef.nodes[3])
            # The source current source flows from the outN node to the
            # outP node of the device.
            if lgRef.nodes[0] == '0':
                srcN = None
            else:
                srcN = detectors.index('V_' + lgRef.nodes[0])
            if lgRef.nodes[1] == '0':
                srcP = None
            else:
                srcP = detectors.index('V_' + lgRef.nodes[1])
        elif lgRef.model == 'g':
            # The detector rows correspond with those of the input nodes
            # of the VCCS.
            if lgRef.nodes[2] == '0':
                detP = None
            else:
                detP = detectors.index('V_' + lgRef.nodes[2])
            if lgRef.nodes[3] == '0':
                detN = None
            else:
                detN = detectors.index('V_' + lgRef.nodes[3])
            # The source current source flows from the outN node to the
            # outP node of the device.
            if lgRef.nodes[1] == '0':
                srcP = None
            else:
                srcP = detectors.index('V_' + lgRef.nodes[1])
            if lgRef.nodes[0] == '0':
                srcN = None
            else:
                srcN = detectors.index('V_' + lgRef.nodes[0])
        elif lgRef.model == 'H':
            # The detector row is that of the input current of the CCVS
            detP = detectors.index('Ii_' + instObj.lgRef)
            detN = None
            # The source row is that of the output current of the CCVS
            srcP = detectors.index('Io_' + instObj.lgRef)
            srcN = None
        elif lgRef.model == 'HZ':
            # The detector row is that of the input current of the CCVS
            detP = detectors.index('Ii_' + instObj.lgRef)
            detN = None
            if lgRef.params['zo'] != 0:
                # A current source in parallel with Zo, hence flowing from the
                # outN node to the outP node of the device is the new source.
                # The gain of the reference variable needs to be divided by the
                # value of Zo.
                if lgRef.nodes[0] == '0':
                    srcP = None
                else:
                    srcP = detectors.index('V_' + lgRef.nodes[0])
                if lgRef.nodes[1] == '0':
                    srcN = None
                else:
                    srcN = detectors.index('V_' + lgRef.nodes[1])
            else:
                # If Zo equals zero the method for model 'H' must be applied.
                srcP = detectors.index('Io_' + instObj.lgRef)
                srcN = None
    else:
        # For all other gain types:
        # The detector rows are those that correspond with the dependent
        # variables of the detector.
        (detP, detN) = instObj.detector
        if detP != None:
            detP = detectors.index(detP)
        if detN != None:
            detN = detectors.index(detN)
        if instObj.source != None:
            # If there is s source defined:
            if instObj.source[0].upper() == 'V':
                # The source row corresponds with that of the current through
                # the voltage source
                srcP = detectors.index('I_' + instObj.source)
                srcN = None
            elif instObj.source[0].upper() == 'I':
                # The source rows correspond with those of the nodal voltages
                # of the source nodes
                nodes = instObj.circuit.elements[instObj.source].nodes
                if nodes[0] != '0':
                    srcN = detectors.index('V_' + nodes[0])
                else:
                    srcN = None
                if nodes[1] != '0':
                    srcP = detectors.index('V_' + nodes[1])
                else:
                    srcP = None
        else:
            # If there is no source defines, srcP and srcN are set to 'None'
            srcP = None
            srcN = None
    return(detP, detN, srcP, srcN)

def doNumer(instObj):
    """
    Calculates the numerator of a transfer by evaluating cofactors or by using
    Cramer's rule.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`

    :return: numerator of a transfer or a detector voltage or current:

             - gain type = 'vi':

               Application of Cramer's rule

             - gain type = 'gain', 'direct', 'asymptotic':

               Sum of cofactors of the MNA matrix for that gain type

             - gain type = 'loopgain':

               Sum of cofactors of the MNA matrix for gain type 'loopgain'
               multiplied with the numerator of the gain of the loop gain
               reference.

             - gain type = 'servo':

               Sum of cofactors of the MNA matrix for gain type 'loopgain'
               multiplied with the the negative value of the numerator of the
               gain of the loop gain reference.

    :return type: sympy.Expr
    """
    (detP, detN, srcP, srcN) = makeSrcDetPos(instObj)
    if instObj.gainType == 'vi':
        # Todo:
        # Iv can have Laplace rationals in it, check if this works with ILT
        Iv = makeSrcVector(instObj.circuit, instObj.parDefs, 'all', value = 'value', numeric = instObj.numeric)
        return maxCramerNumer(instObj.M, Iv, detP, detN)
    else:
        numer = maxNumer(instObj.M, detP, detN, srcP, srcN)
        if instObj.gainType == 'loopgain' or instObj.gainType == 'servo':
            (lgNumer, lgDenom) = sp.fraction(sp.together(lgValue(instObj)))
            numer *= lgNumer
        elif instObj.gainType == 'servo':
            numer *= -lgNumer
        return sp.collect(numer, ini.Laplace)

def doZeros(instObj):
    """
    Calculates the numeric roots of numerator of a transfer.

    It first calls **execute.doNumer()** to calculate the numerator of the
    transfer defined by the gain type. It then calculates the numerical roots
    by calling **SLiCAPmath.numRoots()**.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`

    :return: list with numerical roots of the numerator of a transfer
    :return type: list
    """
    numer = sp.expand(sp.collect(doNumer(instObj).evalf(), ini.Laplace))
    return numRoots(numer, ini.Laplace)

def doPZ(instObj):
    """
    Calculates the DC gain, and the numric roots of the numerator and the
    denominator of a transfer.

    - Calculate the numerator and the denominator
    - Calculate the poles and the zeros
    - Calculate the DC gain
    - Cancel poles and zeros that coincide within a relative tolerance of
      :math:`10^{-\mathrm{ini.disp}}`.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`

    :return: tuple: (poles, zeros, DCvalue)
    :return type: tuple
    """
    numer = sp.expand(sp.collect(doNumer(instObj).evalf(), ini.Laplace))
    denom = sp.expand(sp.collect(doDenom(instObj).evalf(), ini.Laplace))
    poles = numRoots(denom, ini.Laplace)
    zeros = numRoots(numer, ini.Laplace)
    (poles, zeros) = cancelPZ(poles, zeros)
    try:
        # Lets try a real limit with maxima
        DCvalue = maxLimit(numer/denom, str(ini.Laplace), '0', 'plus')
    except:
        # If not just substitute s=0
        DCvalue = sp.Subs(numer/denom, ini.Laplace, 0)
    return(poles, zeros, DCvalue)

def doLaplace(instObj):
    """
    Calculates the numerator and the denominator of the transfer and normalizes
    the result to:

    - :math:`F(s) = G s^{\ell} \\frac{1+b_1s + ... + b_ms^m}{1+a_1s + ... + a_ns^n}`,

      with :math:`\ell` equal zero if there is a finite nonzero zero-frequency
      value, else a positive or negative integer.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`

    :return: Laplace transform of a transfer or detector voltage or current
    :return type: sympy.Expr
    """
    numer = doNumer(instObj)
    denom = doDenom(instObj)
    result = numer/denom
    if ini.normalize == True:
        return simplify(result, method = 'normalize')
    elif ini.factor == True:
        return simplify(result, method = 'factor')
    elif ini.simplify == True:
        return simplify(result, method = 'fraction')
    else:
        return result

def doSolve(instObj):
    """
    Calculates the symbolic or numeric solution of a network.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`

    :return: Network solution (vector)
    :return type: sympy.Matrix
    """
    Iv = makeSrcVector(instObj.circuit, instObj.parDefs, 'all', value = 'value', numeric = instObj.numeric)
    return maxSolve(instObj.M, Iv, numeric = instObj.numeric)

def doNoise(instObj, detP, detN, denom2):
    """
    Calculates the contributions of all noise sources to the noise spectral
    density at the detector.

    Returns a dictionary with key-value pairs:

    - key = ID of the noise source
    - value = contribution to the noise spectral density th the detector in
      :math:`\\frac{V^2}{Hz}` or in :math:`\\frac{A^2}{Hz}`.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`

    :return: onoiseTerms
    :return type: dict
    """
    onoiseTerms = {}
    if denom2 == None:
        denom = maxDet(instObj.M, numeric = instObj.numeric)
        denom = assumeRealParams(denom.subs(ini.Laplace, 2*sp.pi*sp.I*ini.frequency))
        dR, dI = denom.as_real_imag()
        denom2 = dR**2 + dI**2
    denom2 = sp.factor(denom2)
    Iv = makeSrcVector(instObj.circuit, instObj.circuit.parDefs, 'all', value = 'id', numeric = instObj.numeric)
    allTerms =  maxCramerNumer(instObj.M, Iv, detP, detN, numeric = instObj.numeric)
    for src in instObj.circuit.indepVars:
        if 'noise' in list(instObj.circuit.elements[src].params.keys()) and instObj.circuit.elements[src].params['noise'] != 0:
            if instObj.numeric:
                value = fullSubs(instObj.circuit.elements[src].params['noise'], instObj.parDefs)
            else:
                value = instObj.circuit.elements[src].params['noise']
            coeff = sp.Poly(allTerms, sp.Symbol(src)).coeffs()[0]
            coeff = coeff.subs(ini.Laplace, ini.frequency*2*sp.pi*sp.I)
            coeff = assumeRealParams(coeff, params = 'all')
            cR, cI = coeff.as_real_imag()
            coeff2 = cR**2 + cI**2
            term = value * coeff2 / denom2
            onoiseTerms[src] = clearAssumptions(term, params = 'all')
    return onoiseTerms

def doDC(instObj, detP, detN):
    """
    Calculates the DC voltage or current at the detector.

    It uses the dc value field of independent sources and replaces the Laplace
    variable in the MNA matrix with 0.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`
    :param detP: position of the positive detector quantity in the vector with
                 dependent variables
    :type detP: int
    :param detN: position of the negative detector quantity in the vector with
                 dependent variables
    :type detN: int
    """
    Iv = makeSrcVector(instObj.circuit, instObj.parDefs, 'all', value = 'dc', numeric = instObj.numeric)
    M = instObj.M.subs(ini.Laplace, 0)
    numer = maxCramerNumer(M, Iv, detP, detN, numeric = instObj.numeric)
    denom = maxDet(M, numeric = instObj.numeric)
    result = numer/denom
    if ini.factor == True:
        return simplify(result, method = 'factor')
    elif ini.simplify == True:
        return simplify(result, method = 'fraction')
    else:
        return result

def doSolveDC(instObj):
    """
    Calculates the DC solution of a network.

    It uses the dc value field of independent sources and replaces the Laplace
    variable in the MNA matrix with 0.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`
    :return: DC solution of the network
    :return type: sympy.Matrix
    """
    Iv = makeSrcVector(instObj.circuit, instObj.parDefs, 'all', value = 'dc', numeric = instObj.numeric)
    M = instObj.M.subs(ini.Laplace, 0)
    return maxSolve(M, Iv, numeric = instObj.numeric)

def doDCvar(instObj, detP, detN):
    """
    Calculates the contributions of variances of DC sources and resistors to
    detector-referred variance.

    After execution of this function the circuit is modified: dc variance
    current sources have been added in parallel with resistors that have a
    nonzero value of their dcvar parameter.

    The names of these sources are those of the currents through these
    resistors. These names have been added to the list circuit.indepVars.

    If these elements already existed because of an earlier DCvar analysis,
    they will be removed, as well as the references in to them the list
    circuit.indepVars.

    :param instObj: **allResults()** object that holds instruction data.
    :type instObj: :class:`allResult()`
    :return: Tuple with a dictionary ovarTerms and the dc solution of
             the network.

             - ovarTerms (*dict*):

               - key (*str*): ID of the dc variance source
               - value (*sympy.Expr*) contribution of this source to the dc
                 variance at the detector in :math:`V^2` or in :math:`A^2`.

             - dcSolution(*sympy.Matrix*): DC solution of the network
    """
    # Calculate the DC solution, we need it for the calculation of error currents
    dcSolution = doSolveDC(instObj)
    # Add error sources
    for variable in instObj.Dv:
        variable = str(variable)
        varType = variable[0]
        refDes  = variable[2:]
        if varType.upper() == 'I' and refDes[0].upper() == 'R' and 'dcvar' in list(instObj.circuit.elements[refDes].params.keys()):
            # Delete DC variance sources added by a previous dcVar analysis
            if variable in list(instObj.circuit.elements.keys()):
                del(instObj.circuit.elements[variable])
                instObj.circuit.depVars.remove(variable)
            # Calculate the error current
            errorCurrentVariance = instObj.circuit.elements[refDes].params['dcvar']/ instObj.circuit.elements[refDes].params['value']**2 * dcSolution[instObj.circuit.varIndex[variable]]**2
            # Add a current source to the sicuit elements
            newCurrentSource = element()
            newCurrentSource.refDes          = variable
            newCurrentSource.params['dcvar'] = simplify(errorCurrentVariance, method = 'fraction')
            newCurrentSource.params['noise'] = 0
            newCurrentSource.params['dc']    = 0
            newCurrentSource.params['value'] = 0
            newCurrentSource.model           = 'I'
            newCurrentSource.nodes           = instObj.circuit.elements[refDes].nodes
            instObj.circuit.elements[variable] = newCurrentSource
            instObj.circuit.indepVars.append(variable)
    # Create the vector with indepemdent variables (current and voltage sources)
    Iv = makeSrcVector(instObj.circuit, instObj.parDefs, 'all', value = 'id', numeric = instObj.numeric)
    # Calculate the contribution to the detector variance for each source.
    # First the squared denominator, we need it for all sources
    M = instObj.M.subs(ini.Laplace, 0)
    denom2 = simplify(maxDet(M, numeric = instObj.numeric)**2, method = 'factor')
    # Now all terms of the numerator
    allTerms = maxCramerNumer(M, Iv, detP, detN, numeric = instObj.numeric)
    ovarTerms = {}
    for src in instObj.circuit.indepVars:
        # Now the squared numerator for sources that have a nonzero dcVar value.
        if 'dcvar' in list(instObj.circuit.elements[src].params.keys()) and instObj.circuit.elements[src].params['dcvar'] != 0:
            if instObj.numeric:
                # Calculate the numeric value of the source
                value = fullSubs(instObj.circuit.elements[src].params['dcvar'], instObj.parDefs)
            else:
                value = instObj.circuit.elements[src].params['dcvar']
            # Select the coefficient for each variance source from allTerms
            numer2 = simplify(sp.Poly(allTerms, sp.Symbol(src)).coeffs()[0]**2, method = 'factor')
            ovarTerms[src] = value*simplify(numer2/denom2, method = 'fraction')
    return (ovarTerms, dcSolution)

if __name__ == '__main__':
    s = sp.Symbol('s')
    loopGainNumer = -s*(1 + s/20)*(1 + s/40)/2
    loopGainDenom = (s + 1)**2*(1 + s/4e3)*(1 + s/50e3)*(1 + s/1e6)
    loopGain        = loopGainNumer/loopGainDenom
    r = findServoBandwidth(loopGain)
    print(r)
