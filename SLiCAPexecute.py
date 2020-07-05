#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 17:41:46 2020

@author: anton
"""

from SLiCAPyacc import *
       
def doInstruction(instObj):
    """
    Execution of the instruction with parameter stepping.
    """
    if instObj.step:
        if ini.stepFunction:
            # Create a substitution dictionary that does not contain step parameters
            subsDict = {}
            if instObj.stepMethod == 'array':
                for key in instObj.circuit.parDefs.keys():
                    if key not in instObj.stepVars:
                        subsDict[key] = instObj.circuit.parDefs[key]
            else:
                for key in instObj.circuit.parDefs.keys():
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
                        instObj.DCvalue.append(sp.Subs(numers[i]/denoms[i], ini.Laplace, 0))
            elif instObj.dataType == 'step':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                numer = doNumer(instObj)
                numers = stepFunctions(instObj, numer)
                for i in range(len(denoms)):
                    try:
                        instObj.stepResp.append(maxILT(numers[i], denoms[i]*ini.Laplace))
                    except:
                        print "Warning: could not calculate the unit step response."
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
                        instObj.stepResp.append(maxILT(numers[i], denoms[i]))
                    except:
                        print "Warning: could not calculate the unit impulse response."
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
                        instObj.laplace.append(normalizeLaplaceRational(numers[i]/denoms[i]))
                    else:
                        instObj.laplace.append(numers[i]/denoms[i])
            elif instObj.dataType == 'solve':
                sol = doSolve(instObj)
                instObj.solve = stepFunctions(instObj, sol)
                for i in range(len(instObj.solve)):
                    instObj.solve[i] = sp.simplify(instObj.solve[i])
                    """
                    Todo:
                    
                        simplification, normalization and factorization
                        according to ini settings.
                    """
            elif instObj.dataType == 'noise':
                detP, detN, srcP, srcN = makeSrcDetPos(instObj)
                if instObj.source != None:
                    # Calculate the squared gain from source to detector as a
                    # function of ini.frequency
                    gain2 = maxCramerCoeff2(instObj.circuit, instObj.M, instObj.source, detP, detN, dc = False, numeric = instObj.numeric)
                    gain2 = sp.simplify(gain2/maxDet2(instObj.M, dc = False, numeric = instObj.numeric))
                # Calculate the contributions of each noise source to the
                # spectral density of the total output noise
                onoiseTerms = doNoise(instObj, detP, detN)
                # apply function stepping
                for elID in onoiseTerms.keys():
                    if instObj.source != None:
                        instObj.inoiseTerms[elID] = stepFunctions(instObj, sp.simplify(onoiseTerms[elID]/gain2))
                    instObj.onoiseTerms[elID] = stepFunctions(instObj, onoiseTerms[elID])
                    instObj.snoiseTerms[elID] = stepFunctions(instObj, instObj.circuit.elements[elID].params['noise'])
                numRuns = len(instObj.onoiseTerms[elID])
                for i in range(numRuns):
                    # calcuate onoise and inoise for each run
                    onoise = 0
                    inoise = 0
                    for elID in onoiseTerms.keys():
                        onoise += instObj.onoiseTerms[elID][i]
                        if instObj.source != None:
                            inoise += instObj.inoiseTerms[elID][i]
                    instObj.onoise.append(sp.simplify(onoise))
                    if instObj.source != None:
                        instObj.inoise.append(sp.simplify(inoise))
            elif instObj.dataType == 'dc':
                dc = doDC(instObj)
                instObj.dc = stepFunctions(instObj, dc)
            elif instObj.dataType == 'dcsolve':
                dcSolve = doSolveDC(instObj)
                instObj.dcSolve = stepFunctions(instObj, dcSolve)
            elif instObj.dataType == 'dcvar':
                detP, detN, srcP, srcN = makeSrcDetPos(instObj)
                if instObj.source != None:
                    # Calculate the squared DC gain from source to detector
                    gain2 = maxCramerCoeff2(instObj.circuit, instObj.M, instObj.source, detP, detN, dc = True, numeric = instObj.numeric)
                    gain2 = sp.simplify(gain2/maxDet2(instObj.M, dc = True, numeric = instObj.numeric))
                # Calculate the contributions of each variance source to the
                # variance at the detector
                ovarTerms, dcSol = doDCvar(instObj, detP, detN)
                # apply function stepping
                for elID in ovarTerms.keys():
                    if instObj.source != None:
                        instObj.ivarTerms[elID] = stepFunctions(instObj, sp.simplify(ovarTerms[elID]/gain2))
                    instObj.ovarTerms[elID] = stepFunctions(instObj, ovarTerms[elID])
                    instObj.svarTerms[elID] = stepFunctions(instObj, instObj.circuit.elements[elID].params['dcvar'])
                numRuns = len(instObj.ovarTerms[elID])
                for i in range(numRuns):
                    # calcuate ovar and ivar for each run
                    ovar = 0
                    ivar = 0
                    for elID in ovarTerms.keys():
                        ovar += instObj.ovarTerms[elID][i]
                        if instObj.source != None:
                            ivar += instObj.ivarTerms[elID][i]
                    instObj.ovar.append(sp.simplify(ovar))
                    if instObj.source != None:
                        instObj.ivar.append(sp.simplify(ivar))
                # step the DC solution
                instObj.dcSolve = stepFunctions(instObj, instObj.dcSol)
        else:
            # Create a deep copy of the substitution dictionary
            subsDict = {}
            for key in instObj.circuit.parDefs.keys():
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
        # No parameter stepping, just do the non-stepped instruction.
        instObj.parDefs = instObj.circuit.parDefs
        doDataType(instObj)
    return instObj

def stepFunctions(instObj, function):
    """
    Substitutes step values for step parameters in functions and returns a list
    of functions with these substitutions.
    """
    
    """
    # The lambdify method was not faster then one-by-one substitution
    if instObj.stepMethod == 'array':
        func = sp.lambdify(instObj.stepVars, function)
        functions = [func(instObj.stepArray[i]) for i in range(len(instObj.stepArray))]
    else:
        func = sp.lambdify(instObj.stepVar, function)
        functions = [func(instObj.stepList[i]) for i in range(len(instObj.stepList))]
    """
    # One-by-one substitition
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
    Returns the instruction object with the result of the execution without 
    parameter stepping
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
        try:
            instObj.stepResp = maxILT(doNumer(instObj), doDenom(instObj)*ini.Laplace)
        except:
            print "Warning: could not calculate the unit step response."
    elif instObj.dataType == 'impulse' or instObj.dataType == 'time':
        numer = doNumer(instObj)
        denom = doDenom(instObj)
        if instObj.gainType == 'vi':
            nNum, nDen = sp.fraction(numer)
            numer = nNum
            denom = denom*nDen
        try:
            instObj.stepResp = maxILT(numer, denom)
        except:
            print "Warning: could not calculate the unit impulse response."
    elif instObj.dataType == 'solve':
        if instObj.step:
            instObj.solve.append(doSolve(instObj))
        else:
            instObj.solve = doSolve(instObj)    
    elif instObj.dataType == 'noise':
        # Calculate the contributions of each noise source to the
        # spectral density of the total output noise
        detP, detN, srcP, srcN = makeSrcDetPos(instObj)
        onoiseTerms = doNoise(instObj, detP, detN)
        inoiseTerms = {}
        snoiseTerms = {}
        onoise      = 0
        alreadyKeys = instObj.onoiseTerms.keys()
        if instObj.source != None:
            # Calculate the squared gain from source to detector as a
            # function of ini.frequency
            gain2 = maxCramerCoeff2(instObj.circuit, instObj.M, instObj.source, detP, detN, dc = False, numeric = instObj.numeric)
            gain2 = sp.simplify(gain2/maxDet2(instObj.M, dc = False, numeric = instObj.numeric))
            inoise = 0
        for key in onoiseTerms.keys():
            onoise += onoiseTerms[key]
            snoiseTerms[key] = instObj.circuit.elements[key].params['noise']
            if instObj.source != None:
                inoiseTerms[key] = sp.simplify(onoiseTerms[key]/gain2)
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
            instObj.onoise.append(sp.simplify(onoise))
            if instObj.source != None:
                instObj.inoise.append(sp.simplify(inoise))
        else:
            instObj.onoise = onoise
            if instObj.source != None:
                instObj.inoise = sp.simplify(inoise)      
    elif instObj.dataType == 'dc':
        (detP, detN, srcP, srcN) = makeSrcDetPos(instObj)
        if instObj.step:
            instObj.dc.append(doDC(instObj, detP, detN))
        else:
            instObj.dc= doDC(instObj)        
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
        alreadyKeys = instObj.ovarTerms.keys()
        if instObj.source != None:
            # Calculate the squared DC gain from source to detector
            gain2 = maxCramerCoeff2(instObj.circuit, instObj.M, instObj.source, detP, detN, dc = True, numeric = instObj.numeric)
            gain2 = sp.simplify(gain2/maxDet2(instObj.M, dc = True, numeric = instObj.numeric))
            ivar = 0
        for key in ovarTerms.keys():
            ovar += ovarTerms[key]
            svarTerms[key] = instObj.circuit.elements[key].params['dcvar']
            if instObj.source != None:
                ivarTerms[key] = sp.simplify(ovarTerms[key]/gain2)
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
            instObj.ovar.append(sp.simplify(ovar))
            if instObj.source != None:
                instObj.ivar.append(sp.simplify(ivar))
            instObj.dcSolve.append(dcSol)
        else:
            instObj.ovar = ovar
            if instObj.source != None:
                instObj.ivar = sp.simplify(ivar) 
            instObj.dcSolve = dcSol
    return instObj

def doDenom(instObj):
    """
    Calculates the denominator of a transfer by evaluating of the determinant
    of the MNA matrix.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: Sympy expression.
    """
    denom = maxDet(instObj.M)
    if instObj.gainType == 'servo':
        (detP, detN, srcP, srcN) = makeSrcDetPos(instObj)
        numer = maxNumer(instObj.M, detP, detN, srcP, srcN)
        (lgNumer, lgDenom) = sp.fraction(sp.together(lgValue(instObj)))
        numer = numer * lgNumer
        denom = denom * lgDenom + numer
    elif instObj.gainType == 'loopgain':
        (lgNumer, lgDenom) = sp.fraction(sp.together(lgValue(instObj)))
        denom = denom * lgDenom
    return sp.collect(denom, ini.Laplace)

def doPoles(instObj):
    """
    Calculates the denominator of a transfer from source to detector and find
    the poles.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: List with zeros, empty list if no zeros are found.
    """
    denom = sp.expand(sp.collect(doDenom(instObj).evalf(), ini.Laplace))
    return numRoots(denom, ini.Laplace)

def lgValue(instObj):
    """
    Calculates the corrected gain of the loop gain reference. In case of
    a loop gain reference of the type EZ and HZ the calculation of the loop
    gain proceeds as if a current source was placed in parallel with the
    output impedance (zo) of this controlled source. The value of this source
    is the loop gain reference divided by the output impedance of the device
    (Norton equivalent representation).
    """
    lgRef = instObj.circuit.elements[instObj.lgRef]
    if lgRef.model == 'g':
        value = lgRef.params['value']
    elif lgRef.model == 'E':
        value = lgRef.params['value']
    elif lgRef.model == 'EZ':
        value = lgRef.params['value']/lgRef.params['zo']
    elif lgRef.model == 'HZ':
        value = lgRef.params['value']/lgRef.params['zo']
    elif lgRef.model == 'H':
        value = lgRef.params['value']
    elif lgRef.model == 'F':
        value = lgRef.params['value']
    elif lgRef.model == 'G':
        value = lgRef.params['value']
    if instObj.simType == 'numeric':
        value = fullSubs(value, instObj.circuit.parDefs)
    return value

def makeSrcDetPos(instObj):
    """
    Returns the number of the source rows and detector colums for calculation
    of the cofactors or application of Cramer's rule.
    """
    detectors = []
    for var in instObj.circuit.depVars:
        if var != 'V_0':
            detectors.append(var)
    if instObj.gainType == 'loopgain' or instObj.gainType == 'servo':
        lgRef = instObj.circuit.elements[instObj.lgRef]
        if lgRef.model == 'E':
            srcP = detectors.index('I_o_' + instObj.lgRef)
            srcN = None
            if lgRef.nodes[2] == '0':
                detP = None
            else:
                detP = detectors.index('V_' + lgRef.nodes[2])
            if lgRef.nodes[3] == '0':
                detN = None
            else:
                detN = detectors.index('V_' + lgRef.nodes[3])
        elif lgRef.model == 'EZ':
            # Signal source is a current source in parallel with Zo
            # gain will be divided by the value of Zo.
            if lgRef.nodes[2] == '0':
                detP = None
            else:
                detP = detectors.index('V_' + lgRef.nodes[2])
            if lgRef.nodes[3] == '0':
                detN = None
            else:
                detN = detectors.index('V_' + lgRef.nodes[3])
            if lgRef.nodes[0] == '0':
                srcP = None
            else:
                srcP = detectors.index('V_' + lgRef.nodes[0])
            if lgRef.nodes[1] == '0':
                srcN = None
            else:
                srcN = detectors.index('V_' + lgRef.nodes[1])
        elif lgRef.model == 'F':
            if lgRef.nodes[1] == '0':
                srcP = None
            else:
                srcP = detectors.index('V_' + lgRef.nodes[1])
            if lgRef.nodes[0] == '0':
                srcN = None
            else:
                srcN = detectors.index('V_' + lgRef.nodes[0])
            detP = detectors.index('I_i_' + instObj.lgRef)
            detN = None
        elif lgRef.model == 'G':
            srcP = detectors.index('I_o_' + instObj.lgRef)
            srcN = None
            if lgRef.nodes[2] == '0':
                detP = None
            else:
                detP = detectors.index('V_' + lgRef.nodes[2])
            if lgRef.nodes[3] == '0':
                detN = None
            else:
                detN = detectors.index('V_' + lgRef.nodes[3])
        elif lgRef.model == 'g':
            if lgRef.nodes[2] == '0':
                detP = None
            else:
                detP = detectors.index('V_' + lgRef.nodes[2])
            if lgRef.nodes[3] == '0':
                detN = None
            else:
                detN = detectors.index('V_' + lgRef.nodes[3])
            if lgRef.nodes[1] == '0':
                srcP = None
            else:
                srcP = detectors.index('V_' + lgRef.nodes[1])
            if lgRef.nodes[0] == '0':
                srcN = None
            else:
                srcN = detectors.index('V_' + lgRef.nodes[0])
        elif lgRef.model == 'H':
            srcP = detectors.index('I_o' + instObj.lgRef)
            srcN = None
            detP = detectors.index('I_i_' + instObj.lgRef)
            detN = None
        elif lgRef.model == 'HZ':
            detP = detectors.index('I_i_' + instObj.lgRef)
            detN = None
            if lgRef.nodes[0] == '0':
                srcP = None
            else:
                srcP = detectors.index('V_' + lgRef.nodes[0])
            if lgRef.nodes[1] == '0':
                srcN = None
            else:
                srcN = detectors.index('V_' + lgRef.nodes[1])    
    else:
        (detP, detN) = instObj.detector
        if detP != None:
            detP = detectors.index(detP)
        if detN != None:
            detN = detectors.index(detN)
        if instObj.source != None:
            if instObj.source[0].upper() == 'V':
                srcP = detectors.index('I_' + instObj.source)
                srcN = None
            elif instObj.source[0].upper() == 'I':
                nodes = instObj.circuit.elements[instObj.source].nodes
                if nodes[0] != '0':
                    srcP = detectors.index('V_' + nodes[0])
                else:
                    scrP = None
                if nodes[1] != 0:
                    srcN = detectors.index('V_' + nodes[1])
                else:
                    srcN = None
        else:
            srcP = None
            srcN = None
    return(detP, detN, srcP, srcN)
    
def doNumer(instObj):
    """
    Calculates the numerator of a transfer by evaluating cofactors or the 
    numerator of the detector response using Cramer's rule.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: Sympy expression.
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
    Calculates the numerator of a transfer from source to detector and find the
    zeros.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: List with zeros, empty list if no zeros are found.
    """
    numer = sp.expand(sp.collect(doNumer(instObj).evalf(), ini.Laplace))
    return numRoots(numer, ini.Laplace)
    
def doPZ(instObj):
    """
    Calculates the numerator and the denominator of the transfer from source to
    detector and determines the zero-frequency value, the poles and the zeros.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: List with poles, list with zeros, DCvalue.
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
        
        F(s) = gain * s^l (1+b_1*s + ... + b_m*s^m)/ (1+a_1*s + ... + a_n*s^n),

        with l zero if there is a finite nonzero zero-frequency value, else
        positive or negative integer.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: Sympy expression.
    """
    numer = doNumer(instObj)
    denom = doDenom(instObj)
    if ini.normalize:
        if ini.normalize == True:
            return normalizeLaplaceRational(numer/denom)
        else:
            return numer/denom
    elif ini.simplify:
        if ini.factor == True:
            numer, denom = sp.fraction(sp.simplify(numer/denom))
            return sp.factor(numer)/sp.factor(denom)
        else:
            return sp.simplify(numer/denom)
    elif ini.factor:
        result = sp.factor(numer)/sp.factor(denom)
        if ini.simplify == True:
            result = sp.simplify(result)
        return result   
    else:
        return numer/denom

def doSolve(instObj):
    """
    Calculates the solution of a network.
    """
    Iv = makeSrcVector(instObj.circuit, instObj.parDefs, 'all', value = 'value', numeric = instObj.numeric)
    return maxSolve(instObj.M, Iv, numeric = instObj.numeric)

def doNoise(instObj, detP, detN):
    """
    Calculates the contributions of all noise sources to the noise spectral
    density at the detector.
    Returns a dictionary:
        key   =  ID of the noise source
        value = contribution to the noise spectral density th the detector
                in V^2/Hz or in A^2/Hz
    """
    denom2 = maxDet2(instObj.M, dc=False, numeric = instObj.numeric)
    onoiseTerms = {}
    for src in instObj.circuit.indepVars:
        if 'noise' in instObj.circuit.elements[src].params.keys() and instObj.circuit.elements[src].params['noise'] != 0:
            if instObj.numeric:
                value = fullSubs(instObj.circuit.elements[src].params['noise'], instObj.parDefs)
            else:
                value = instObj.circuit.elements[src].params['noise']
            numer2 = maxCramerCoeff2(instObj.circuit, instObj.M, src, detP, detN, dc=False, numeric = instObj.numeric)
            onoiseTerms[src] = sp.simplify(sp.factor(numer2)/sp.factor(denom2))*value
    return onoiseTerms

def doDC(instObj, detP, detN):
    """
    """
    Iv = makeSrcVector(instObj.circuit, instObj.parDefs, 'all', value = 'dc', numeric = instObj.numeric)
    M = instObj.M.subs(ini.Laplace, 0)
    numer = maxCramerNumer(M, Iv, detP, detN, numeric = instObj.numeric)
    denom = maxDet(M, numeric = instObj.numeric)
    return sp.simplify(numer/denom)

def doSolveDC(instObj):
    """
    Calculates the DC solution of a network. It uses the dc value field of
    independent sources and replaces the Laplace variable in the matrix with 0.
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
    
    If these elements existed, they will be removed, as well as references in 
    to them the list circuit.indepVars.
    """
    dcSolution = doSolveDC(instObj)
    # Add error sources
    for variable in instObj.Dv:
        variable = str(variable)
        varType = variable[0]
        refDes  = variable[2:]
        if varType.upper() == 'I' and refDes[0].upper() == 'R' and 'dcvar' in instObj.circuit.elements[refDes].params.keys():
            if variable in instObj.circuit.elements.keys():
                del(instObj.circuit.elements[variable])
                instObj.circuit.depVars.remove(variable)
            errorCurrentVariance = instObj.circuit.elements[refDes].params['dcvar']/ instObj.circuit.elements[refDes].params['value']**2 * dcSolution[instObj.circuit.varIndex[variable]]**2
            newCurrentSource = element()
            newCurrentSource.refDes          = variable
            newCurrentSource.params['dcvar'] = sp.simplify(errorCurrentVariance)
            newCurrentSource.params['noise'] = 0
            newCurrentSource.params['dc']    = 0
            newCurrentSource.params['value'] = 0
            newCurrentSource.model           = 'I'
            newCurrentSource.nodes           = instObj.circuit.elements[refDes].nodes
            instObj.circuit.elements[variable] = newCurrentSource
            instObj.circuit.indepVars.append(variable)
    Iv = makeSrcVector(instObj.circuit, instObj.parDefs, 'all', value = 'dcvar', numeric = instObj.numeric)
    denom2 = maxDet2(instObj.M, dc=True, numeric = instObj.numeric)
    ovarTerms = {}
    for src in instObj.circuit.indepVars:
        if 'dcvar' in instObj.circuit.elements[src].params.keys() and instObj.circuit.elements[src].params['dcvar'] != 0:
            if instObj.numeric:
                value = fullSubs(instObj.circuit.elements[src].params['dcvar'], instObj.parDefs)
            else:
                value = instObj.circuit.elements[src].params['dcvar']
            numer2 = maxCramerCoeff2(instObj.circuit, instObj.M, src, detP, detN, dc=True, numeric = instObj.numeric)
            ovarTerms[src] = sp.simplify(sp.factor(numer2)/sp.factor(denom2))*value
    return (ovarTerms, dcSolution)

def checkNumeric(expr, stepVar = None):
    """
    Checks if the expressions does not contain parameters other then stepVar',
    'ini.Laplace', 'FREQUECY' or 'OMEGA'.
    
    expr:         Sympy expression
    stepVar:      str or Sympy.Symbol
    return value: 'True' if numeric, else 'False'.
    """
    numeric = True
    if type(expr) == str:
        expr = sp.N(sp.sympify(expr))
    if isinstance(expr, tuple(sp.core.all_classes)):
        expr = sp.N(expr)
        params = list(expr.atoms(sp.Symbol))
        for par in params:
            if stepVar == None and par != ini.Laplace and par != ini.frequency:
                numeric = False
            elif par != stepVar and par != ini.Laplace and par != ini.frequency:
                numeric = False
    return numeric

def findServoBandwidth(loopgainRational):
    """
    Determines the intersection points of the asymptotes of the magnitude of
    the loopgain with unity. It returns a dictionary with key-value pairs:
        
        - hpf: frequency of high-pass intersection
        - hpo: order at high-pass intersection
        - lpf: frequency of low-pass intersection
        - lpo: order at low-pass intersection
        - mbv: mid-band value of the loopgain (highest value at order = zero)
        - mbf: lowest freqency of mbv
        
    """
    numer, denom    = sp.fraction(loopgainRational)
    numer           = sp.expand(sp.collect(numer.evalf(), ini.Laplace))
    denom           = sp.expand(sp.collect(denom.evalf(), ini.Laplace))
    poles           = numRoots(denom, ini.Laplace)
    zeros           = numRoots(numer, ini.Laplace)
    (poles, zeros)  = cancelPZ(poles, zeros)
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
    freqsOrders     = np.zeros((numCornerFreqs, 6))
    mbv             = sp.N(sp.Subs(loopgainRational, ini.Laplace, 0))
    mbf             = 0
    for i in range(numZeros):
        freqsOrders[i, 0] = np.abs(zeros[i])
        freqsOrders[i, 1] = 1
    for i in range(numPoles):
        freqsOrders[numZeros + i, 0] = np.abs(poles[i])
        freqsOrders[numZeros + i, 1] = -1
    # sort the rows with increasing corner frequencies 
    freqsOrders = freqsOrders[freqsOrders[:,0].argsort()]
    
    start = 0
    for i in range(numCornerFreqs):
        if freqsOrders[i, 0] == 0:
            start = i + 1
            freqsOrders[i, 2] = startOrder
            freqsOrders[i, 4] = 0
            freqsOrders[i, 5] = freqsOrders[-1, 0]
        if i == start:
            freqsOrders[i, 2] =  startOrder + freqsOrders[i, 1]
            freqsOrders[i, 3] = startValue/(freqsOrders[i, 0]**freqsOrders[i, 1])
            if freqsOrders[i, 2] != 0:
                Bw = freqsOrders[i, 3]**(-1/freqsOrders[i, 2])
            else:
                Bw = 0
            if Bw > freqsOrders[i, 0]:
                if freqsOrders[i, 2] > 0 and freqsOrders[i, 1] > 0:
                    freqsOrders[i, 4] = Bw
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                elif freqsOrders[i, 2] < 0 and freqsOrders[i, 1] < 0:
                    freqsOrders[i, 5] = Bw
                    freqsOrders[i, 4] = 0
                elif freqsOrders[i, 2] < 0 and freqsOrders[i, 1] > 0:
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                    freqsOrders[i, 4] = 0
                elif freqsOrders[i, 2] > 0 and freqsOrders[i, 1] > 0:
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                    freqsOrders[i, 4] = Bw
                elif freqsOrders[i, 2] == 0:
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                    freqsOrders[i, 4] = 0
            else:
                freqsOrders[i, 4] = 0
                freqsOrders[i, 5] = freqsOrders[-1, 0]
        elif i > start:
            freqsOrders[i, 2] = freqsOrders[i - 1, 2] + freqsOrders[i, 1]
            if freqsOrders[i, 1] != 0:
                freqsOrders[i, 3] = freqsOrders[i - 1, 3]/(freqsOrders[i, 0]**freqsOrders[i, 1])
            else:
                freqsOrders[i, 3] = np.NaN
            if freqsOrders[i, 2] != 0:
                freqsOrders[i, 5] = freqsOrders[i, 3]**(-1/freqsOrders[i, 2])
            else:
                freqsOrders[i, 5] = 0
            if freqsOrders[i, 2] != 0:
                Bw = freqsOrders[i, 3]**(-1/freqsOrders[i, 2])
            else:
                Bw = 0
            if Bw > freqsOrders[i, 0]:
                if freqsOrders[i, 2] > 0 and freqsOrders[i, 1] > 0:
                    freqsOrders[i, 4] = Bw
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                elif freqsOrders[i, 2] < 0 and freqsOrders[i, 1] < 0:
                    freqsOrders[i, 5] = Bw
                    freqsOrders[i, 4] = 0
                elif freqsOrders[i, 2] < 0 and freqsOrders[i, 1] > 0:
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                    freqsOrders[i, 4] = 0
                elif freqsOrders[i, 2] > 0 and freqsOrders[i, 1] > 0:
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                    freqsOrders[i, 4] = Bw
                elif freqsOrders[i, 2] == 0:
                    freqsOrders[i, 5] = freqsOrders[-1, 0]
                    freqsOrders[i, 4] = 0
            else:
                freqsOrders[i, 4] = 0
                freqsOrders[i, 5] = freqsOrders[-1, 0]
    result = {}
    result['hpf']=np.amax(freqsOrders[:,4])
    result['lpf']=np.amin(freqsOrders[:,5])
    result['hpo']=freqsOrders[np.where(freqsOrders[:,4]==result['hpf'])[0][0],2]
    result['lpo']=freqsOrders[np.where(freqsOrders[:,5]==result['lpf'])[0][0],2]
    for i in range(numCornerFreqs):
        if freqsOrders[i,2] == 0 and freqsOrders[i,3] > mbv:
            result['mbv'] = freqsOrders[i,3]
            result['mbf'] = freqsOrders[i,0]
    if ini.Hz:
        result['hpf'] = result['hpf']/np.pi/2
        result['lpf'] = result['lpf']/np.pi/2
        result['mbf'] = result['mbf']/np.pi/2
    return result

def rmsNoise(noiseResult, noise, fmin, fmax, source = None):
    """
    """
    fmax = checkNumber(fmax)
    fmin = checkNumber(fmin)
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
    rms =  sp.sqrt(maxIntegrate(noiseData, ini.frequency, start=fmin, stop=fmax))
    return rms

if __name__ == '__main__': 
    s = sp.Symbol('s')
    loopGainNumer = -s*(1 + s/20)*(1 + s/40)/2
    loopGainDenom = (s + 1)**2*(1 + s/4e3)*(1 + s/50e3)*(1 + s/1e6)
    loopGain        = loopGainNumer/loopGainDenom
    r = findServoBandwidth(loopGain)
    print r