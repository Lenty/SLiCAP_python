#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 17:08:41 2021

@author: anton
"""
from SLiCAP.SLiCAPyacc import *

def createResultObject(instr):
    """
    Returns an instance of the *allResults* object with the instruction data copied to it.
    
    :param instr: SLiCAP instruction object.
    :type instr: SLiCAPinstruction.instruction
    
    :return: result
    :rtype: SLiCAPprotos.allResults object
    """
    result = allResults()
    result.simType        = instr.simType
    result.gainType       = instr.gainType
    result.convType       = instr.convType
    result.dataType       = instr.dataType
    result.step           = instr.step
    result.stepVar        = instr.stepVar
    result.stepVars       = []
    if type(instr.stepVars) == list:
        # Make a deep copy of the list
        result.stepVars = [var for var in instr.stepVars]
    result.stepMethod     = instr.stepMethod
    result.stepStart      = instr.stepStart
    result.stepStop       = instr.stepStop
    result.stepNum        = instr.stepNum
    result.stepList       = []
    # Make a deep copy of the list
    result.stepList = [num for num in instr.stepList]
    result.stepArray      = []
    # Make a deep copy of the array
    for row in instr.stepArray:
        if type(row) == list:
            rowCopy = [num for num in row]
            result.stepArray.append(rowCopy)
    result.source         = instr.source
    if type(instr.detector) == list:
        # Make a deep copy of the detector list
        result.detector       = [detector for detector in instr.detector]
    else:
        result.detector = instr.detector 
    result.lgRef          = instr.lgRef
    result.circuit        = instr.circuit
    result.errors         = instr.errors
    result.detUnits       = instr.detUnits
    result.detLabel       = instr.detLabel
    result.srcUnits       = instr.srcUnits
    result.numeric        = instr.numeric
    result.label          = instr.label
    result.parDefs        = None
    if instr.parDefs != None:
        result.parDefs = {}
        for key in list(instr.parDefs.keys()):
            result.parDefs[key] = instr.parDefs[key]
    return result   

def makeMaxDetPos(instr, result):
    """
    Returns the index of the detector colum(s) for calculation of Cramer's rule.

    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`

    :return: tuple: (detP, detN):

                    - detP (*int, int*): number of the row of the vector with dependent
                      variables that corresponds with the positive detector
                    - detN (*int, int*): number of the row of the vector with dependent
                      variables that corresponds with the negative detector

    :return type: tuple
    """
    
    detectors = [str(var) for var in list(result.Dv)]
    detP, detN = result.detector
    if detP != None:
        try:
            detP = detectors.index(detP) + 1
        except ValueError:
            print("Error: unknown detector:", detP)
            instr.errors += 1
    else:
        detP = 0
    if detN != None:
        try:
            detN = detectors.index(detN) + 1
        except ValueError:
            print("Error: unknown detector:", detN)
            instr.errors += 1
    else:
        detN = 0
    return detP, detN

def doInstruction(instr):
    """
    Executes the instruction and returns the result.


    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    
    :return: Result of the execution of the instruction.
    :rtype: SLiCAPprotos.allResults()
    """
    if instr.errors == 0:
        result = createResultObject(instr)
        instr = makeSubsDict(instr)  
        oldLGrefElements = []
        for i in range(len(instr.lgRef)):
            if instr.lgRef[i] != None:
                if instr.gainType == 'asymptotic':
                    oldLGrefElements.append(instr.circuit.elements[instr.lgRef[i]])
                    newLGrefElement = element()
                    newLGrefElement.nodes = oldLGrefElements[-1].nodes
                    newLGrefElement.model = 'N'
                    newLGrefElement.type = 'N'
                    newLGrefElement.refDes = oldLGrefElements[-1].refDes
                    instr.circuit.elements[instr.lgRef[i]] = newLGrefElement
                    instr.circuit = updateCirData(instr.circuit)
                elif instr.gainType == 'loopgain' or instr.gainType == 'servo' or instr.gainType == 'direct':
                    instr.lgValue[i] = instr.circuit.elements[instr.lgRef[i]].params['value']
                    if instr.gainType == 'direct':
                        instr.circuit.elements[instr.lgRef[i]].params['value'] = sp.N(0)
                    else:    
                        instr.circuit.elements[instr.lgRef[i]].params['value'] = sp.Symbol("_LGREF_" + str(i+1))
        if instr.dataType == 'numer':
            result = doNumer(instr, result)            
        elif instr.dataType == 'denom':
            result = doDenom(instr, result)
        elif result.dataType == 'laplace':
            result = doLaplace(instr, result)
        elif instr.dataType == 'poles':
            result = doPoles(instr, result)
        elif instr.dataType == 'zeros':
            result = doZeros(instr, result)
        elif instr.dataType == 'pz':
            result = doPZ(instr, result)
        elif instr.dataType == 'noise':
            result = doNoise(instr, result)
        elif instr.dataType == 'dcvar':
            result = doDCvar(instr, result)
        elif instr.dataType == 'dc':
            result = doDC(instr, result)
        elif instr.dataType == 'impulse':
            result = doImpulse(instr, result)
        elif instr.dataType == 'step':
            result = doStep(instr, result)
        elif instr.dataType == 'time':
            result = doTime(instr, result)
        elif instr.dataType == 'solve':
            result = doSolve(instr, result)
        elif instr.dataType == 'dcsolve':
            result = doDCsolve(instr, result)
        elif instr.dataType == 'timesolve':
            result = doTimeSolve(instr, result)
        elif instr.dataType == 'matrix':
            result = doMatrix(instr, result)
        elif instr.dataType == 'params':
            pass
        else:
            print('Error: unknown dataType:', instr.dataType)
        if instr.gainType == 'asymptotic':
            # Restore the original loop gain reference element
            for i in range(len(instr.lgRef)):
                if instr.lgRef[i] != None:
                    instr.circuit.elements[instr.lgRef[i]] = oldLGrefElements[i]
            instr.circuit = updateCirData(instr.circuit) 
        elif instr.gainType == 'direct' or instr.gainType == 'loopgain' or instr.gainType == 'servo':
            for i in range(len(instr.lgRef)):
                if instr.lgRef[i] != None:
                    instr.circuit.elements[instr.lgRef[i]].params['value'] = instr.lgValue[i]
    return result

def doNumer(instr, result):
    """
    Returns the numerator of a transfer function, or of the Laplace Transform 
    of a detector voltage or current.
    
    The result will be stored in the **.numer** attribute of the resturn object. In
    cases of parameter stepping, this attribute is a list with numerators.

    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    
    :return: Result of the execution of the instruction.
    :rtype: SLiCAPprotos.allResults()
    """
    if instr.step:
        if ini.stepFunction:
            if instr.gainType == 'loopgain' or instr.gainType == 'servo':
                numer, denom = sp.fraction(doLoopGainServo(instr, result))
            else:
                numer = doMaxInstr(instr, result).numer[0]
            result.numer = stepFunctions(instr.stepDict, sp.simplify(numer))
        else:
            stepVars = list(instr.stepDict.keys())
            numSteps = len(instr.stepDict[stepVars[0]])
            for i in range(numSteps):
                for j in range(len(stepVars)):
                    instr.parDefs[stepVars[j]] = instr.stepDict[stepVars[j]][i]
                if instr.gainType == 'loopgain' or instr.gainType == 'servo':
                    numer, denom = sp.fraction(doLoopGainServo(instr, result))
                    result.numer.append(numer)
                else:
                    result = doMaxInstr(instr, result)
    else:
        if instr.gainType == 'loopgain' or instr.gainType == 'servo':
            doLoopGainServo(instr, result)
        else:
            result = doMaxInstr(instr, result)
        result.numer = result.numer[0]
        result.numer = sp.simplify(result.numer)
    return result

def doDenom(instr, result):
    """
    Returns the denominator of a transfer function, or of the Laplace Transform
    of a detector voltage or current.
    
    The result will be stored in the **.denom** attribute of the resturn object. In
    cases of parameter stepping, this attribute is a list with numerators.

    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    
    :return: Result of the execution of the instruction.
    :rtype: SLiCAPprotos.allResults()
    """
    if instr.step:
        if ini.stepFunction:
            if instr.gainType == 'loopgain' or instr.gainType == 'servo':
                numer, denom = sp.fraction(doLoopGainServo(instr, result))
            else:
                denom = doMaxInstr(instr, result).denom[0]
            result.denom = stepFunctions(instr.stepDict, sp.simplify(denom))
        else:
            stepVars = list(instr.stepDict.keys())
            numSteps = len(instr.stepDict[stepVars[0]])
            for i in range(numSteps):
                for j in range(len(stepVars)):
                    instr.parDefs[stepVars[j]]=instr.stepDict[stepVars[j]][i]
                if instr.gainType == 'loopgain' or instr.dataType == 'servo':
                    numer, denom = sp.fraction(doLoopGainServo(instr, result))
                    result.denom.append(denom)
                else:
                    result = doMaxInstr(instr, result)
    else:
        if instr.gainType == 'loopgain' or instr.gainType == 'servo':
            doLoopGainServo(instr, result)
        else:
            result = doMaxInstr(instr, result)
        result.denom = result.denom[0]
        result.denom = sp.simplify(result.denom)
    return result

def doLaplace(instr, result):
    """
    Returns a transfer function, or the Laplace Transform of a detector voltage or current.
    
    The result will be stored in the **.laplace** attribute of the resturn object. In
    cases of parameter stepping, this attribute is a list with numerators.

    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    
    :return: Result of the execution of the instruction.
    :rtype: SLiCAPprotos.allResults()
    """
    if instr.step:
        if ini.stepFunction:
            if instr.gainType == 'loopgain' or instr.gainType == 'servo':
                laplaceFunc = doLoopGainServo(instr, result)
            else:
                result = doMaxInstr(instr, result)
                laplaceFunc = sp.simplify(result.laplace[0])
            result.laplace = stepFunctions(instr.stepDict, laplaceFunc)
        else:
            stepVars = list(instr.stepDict.keys())
            numSteps = len(instr.stepDict[stepVars[0]])
            for i in range(numSteps):
                for j in range(len(stepVars)):
                    instr.parDefs[stepVars[j]] = instr.stepDict[stepVars[j]][i]
                if instr.gainType == 'loopgain' or instr.gainType == 'servo':
                    result.laplace.append(doLoopGainServo(instr, result))
                else:
                    result = doMaxInstr(instr, result)
        result.laplace[-1] = sp.simplify(result.laplace[-1])
    else:
        if instr.gainType == 'loopgain' or instr.gainType == 'servo':
            result.laplace = doLoopGainServo(instr, result)
        else:    
            result = doMaxInstr(instr, result)
            result.laplace = result.laplace[0]
        result.laplace =sp.simplify(result.laplace)
        result.numer, result.denom = sp.fraction(result.laplace)
    return result

def doLoopGainServo(instr, result):
    """
    Returns the Laplace expression of the loop gain of the asymptotic-gain
    feedback model, or of the 'servo function' as defined by Montagne. 
    The calculation uses the return difference, as defined by Bode (1945).
    
    The results are stored in the following attributes of the return object:
        
        - **.numer**: the numerator of the loop gain or the servo fucntion or a list
          of numerators if parameter stepping is applied.
        - **.denom**: the denominator of the loop gain or the servo fucntion or a list
          of denominators if parameter stepping is applied.
        - **.laplace**: the loop gain or the servo fucntion or a list
          of laplace expressions if parameter stepping is applied.

    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
  
    :return: Result of the execution of the instruction.
    :rtype: SLiCAPprotos.allResults()
    """
    
    num, den = doMaxLoopGainServo(instr, result)
    if instr.numeric:
        num = sp.N(num)
        den = sp.N(den)
    result.denom.append(den)
    result.numer.append(num)
    result.laplace.append(num/den)
    return num/den

def doMaxLoopGainServo(instr, result):
    """
    Returns a tuple with the numerator and the denominator of the loop gain or
    the servo function; depeding on the gain type.

    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    
    :return: numer, denom
    :rtype: tuple with two sympy expressions
    """
    makeMaxMatrices(instr, result)
    M = python2maxima(result.M)
    if instr.lgValue[0] != None:
        if instr.numeric:
            lg1 = fullSubs(instr.lgValue[0], instr.parDefs)
        else:
            lg1 = instr.lgValue[0]
    else:
        lg1 = None
    if instr.lgValue[1] != None:
        if instr.numeric:
            lg2 = fullSubs(instr.lgValue[1], instr.parDefs)
        else:
            lg2 = instr.lgValue[1]
    else:
        lg2 = None
    if instr.gainType == 'loopgain':
        maxResult = doMaxFunction('doLoopGain', [M, lg1, lg2])
        numer, denom = sp.fraction(maxResult)
    elif instr.gainType == 'servo':
        numer, denom = sp.fraction(doMaxFunction('doServo', [M, lg1, lg2]))  
    return numer, denom

def doPoles(instr, result):
    """
    Adds the result of a poles analysis to result.

    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    instr.dataType = "denom"
    result.dataType = "denom"
    result = doDenom(instr, result)
    if instr.step:
        for poly in result.denom:
            result.poles.append(numRoots(poly, ini.Laplace))
        instr.dataType = "poles"
        result.dataType = "poles"               
    else:
        variables = list(result.denom.atoms(sp.Symbol))
        if len(variables) == 1 and variables[0] == ini.Laplace:
            result.poles = list(numRoots(result.denom, ini.Laplace))
            instr.dataType = "poles"
            result.dataType = "poles"
        else:
            # findRoots with maxima, also for symbolic
            instr.dataType = "poles"
            result.dataType = "poles"
            result = doMaxInstr(instr, result)
            result.poles = result.poles[0]
    return result

def doZeros(instr, result):
    """
    Adds the result of a zeros analysis to result.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    instr.dataType = "numer"
    result.dataType = "numer"
    result = doNumer(instr, result)
    if instr.step:
        for poly in result.numer:
            result.zeros.append(numRoots(poly, ini.Laplace))
        instr.dataType = "zeros"
        result.dataType = "zeros" 
    else:
        variables = list(result.numer.atoms(sp.Symbol))
        if len(variables) == 1 and variables[0] == ini.Laplace:
            result.zeros = list(numRoots(result.numer, ini.Laplace))
            instr.dataType = "zeros"
            result.dataType = "zeros"
        else:
            # findRoots with maxima, also for symbolic
            instr.dataType = "zeros"
            result.dataType = "zeros"
            result = doMaxInstr(instr, result)
            result.zeros = result.zeros[0]
    return result

def doPZ(instr, result):
    """
    Adds the result of a pole-zero analysis to result.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    instr.dataType = 'laplace'
    result.dataType = 'laplace'
    result = doLaplace(instr, result)
    if result.step:
        for i in range(len(result.laplace)):
            numer, denom = sp.fraction(normalizeRational(result.laplace[i]))
            variables = list(numer.atoms(sp.Symbol))
            if len(variables) == 1 and variables[0] == ini.Laplace:
                result.zeros.append(list(numRoots(numer, ini.Laplace)))
            else:
                # findRoots with maxima, also for symbolic
                instr.dataType = "zeros"
                result.dataType = "zeros"
                result = doMaxInstr(instr, result)
            variables = list(denom.atoms(sp.Symbol))
            if len(variables) == 1 and variables[0] == ini.Laplace:
                result.poles.append(list(numRoots(denom, ini.Laplace)))
            else:
                # findRoots with maxima, also for symbolic
                instr.dataType = "poles"
                result.dataType = "poles"
                result = doMaxInstr(instr, result)
            try:
                result.poles[-1], result.zeros[-1] = cancelPZ(result.poles[-1], result.zeros[-1])
            except:
                pass
            result.DCvalue.append(gainValue(numer, denom))        
    else:
        numer, denom = sp.fraction(normalizeRational(result.laplace))
        variables = list(numer.atoms(sp.Symbol))
        if len(variables) == 1 and variables[0] == ini.Laplace:
            result.zeros = list(numRoots(numer, ini.Laplace))
        else:
            # findRoots with maxima, also for symbolic
            instr.dataType = "zeros"
            result.dataType = "zeros"
            result = doMaxInstr(instr, result)
            result.zeros = result.zeros[0]
        variables = list(denom.atoms(sp.Symbol))
        if len(variables) == 1 and variables[0] == ini.Laplace:
            result.poles = list(numRoots(denom, ini.Laplace))
            instr.dataType = "poles"
            result.dataType = "poles"
        else:
            # findRoots with maxima, also for symbolic
            instr.dataType = "poles"
            result.dataType = "poles"
            result = doMaxInstr(instr, result)
            result.poles = result.poles[0]
        try:
            result.poles, result.zeros = cancelPZ(result.poles, result.zeros)
        except:
            pass
        result.DCvalue = gainValue(numer, denom)  
    instr.dataType = 'pz'
    result.dataType = 'pz'
    return result

def calcNumer(instr, result):
    """
    Calculates the numerator of the source-detector gain.

    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    if instr.source != [None, None]:
        dataType = instr.dataType
        instr.gainType = 'gain'
        result.gainType = 'gain'
        instr.dataType = 'numer'
        result.dataType = 'numer'
        numerator = doMaxInstr(instr, result)
        instr.gainType = 'vi'
        result.gainType = 'vi'
        instr.dataType = dataType
        result.dataType = dataType
    return result

def doNoise(instr, result):
    """
    Adds the result of a noise analysis to result.

    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    if instr.step:
        if ini.stepFunction:
            if instr.source != [None, None]:
                result = calcNumer(instr, result)
            noiseResult = doMaxInstr(instr, result)
            result.onoise = stepFunctions(instr.stepDict, noiseResult.onoise[0])
            result.inoise = stepFunctions(instr.stepDict, noiseResult.inoise[0])
            for srcName in list(noiseResult.onoiseTerms.keys()):
                result.onoiseTerms[srcName] = stepFunctions(instr.stepDict, noiseResult.onoiseTerms[srcName][0])
                result.inoiseTerms[srcName] = stepFunctions(instr.stepDict, noiseResult.inoiseTerms[srcName][0])
        else:
            stepVars = list(instr.stepDict.keys())
            numSteps = len(instr.stepDict[stepVars[0]])
            for i in range(numSteps):
                for j in range(len(stepVars)):
                    instr.parDefs[stepVars[j]]=instr.stepDict[stepVars[j]][i]
                if instr.source != [None, None]:
                    result = calcNumer(instr, result)
                result = doMaxInstr(instr, result)   
    else:
        if instr.source != [None, None]:
            result = calcNumer(instr, result)
        result = doMaxInstr(instr, result)
        result.onoise = result.onoise[0]
        result.inoise = result.inoise[0]
        for key in list(result.onoiseTerms.keys()):          
            if len(result.onoiseTerms[key]) > 0:
                result.onoiseTerms[key] = result.onoiseTerms[key][0]
                if instr.source != [None, None]:
                    result.inoiseTerms[key] = result.inoiseTerms[key][0]
            else:
                del(result.onoiseTerms[key])
                if instr.source != [None, None]:
                    del(result.inoiseTerms[key])
    return result

def doDCvar(instr, result):
    """
    Adds the result of a dcvar analysis to result.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    delDCvarSources(instr)
    if instr.step:
        print("Warning: parameter stepping not (yet) tested for 'dcvar' analysis!")
        if ini.stepFunction:
            instr.dataType = 'dcsolve'
            result.dataType = 'dcsolve'
            result.dcSolve = doMaxInstr(instr, result).dcSolve[0]
            instr.dataType = 'dcvar'
            result.dataType = 'dcvar'
            if instr.source != [None, None]:
                result = calcNumer(instr, result)
            addDCvarSources(instr, result.dcSolve)
            varResult = doMaxInstr(instr, result)
            result.ovar = stepFunctions(instr.stepDict, varResult.ovar[0])
            result.ivar = stepFunctions(instr.stepDict, varResult.ivar[0])
            for srcName in list(varResult.ovarTerms.keys()):
                result.ovarTerms[srcName] = stepFunctions(instr.stepDict, varResult.ovarTerms[srcName][0])
                result.ivarTerms[srcName] = stepFunctions(instr.stepDict, varResult.ivarTerms[srcName][0])
            delDCvarSources(instr)
        else:
            stepVars = list(instr.stepDict.keys())
            numSteps = len(instr.stepDict[stepVars[0]])
            for i in range(numSteps):
                for j in range(len(stepVars)):
                    instr.parDefs[stepVars[j]]=instr.stepDict[stepVars[j]][i]
                delDCvarSources(instr)
                instr.dataType = 'dcsolve'
                result.dataType = 'dcsolve'
                result.dcSolve = doMaxInstr(instr, result).dcSolve[i]
                instr.dataType = 'dcvar'
                result.dataType = 'dcvar'
                if instr.source != [None, None]:
                    result = calcNumer(instr, result)
                addDCvarSources(instr, result.dcSolve)
                result = doMaxInstr(instr, result)
                delDCvarSources(instr)
    else:    
        instr.dataType = 'dcsolve'
        result.dataType = 'dcsolve'
        result.dcSolve = doMaxInstr(instr, result).dcSolve[0]
        instr.dataType = 'dcvar'
        result.dataType = 'dcvar'
        if instr.source != [None, None]:
            result = calcNumer(instr, result)
        addDCvarSources(instr, result.dcSolve)       
        result = doMaxInstr(instr, result)
        result.ovar = result.ovar[0]
        result.ivar = result.ivar[0]
        for key in list(result.ovarTerms.keys()):
            if len(result.ovarTerms[key]) > 0:
                result.ovarTerms[key] = result.ovarTerms[key][0]
                if instr.source != [None, None]:
                    result.ivarTerms[key] = result.ivarTerms[key][0]
            else:
                del(result.ovarTerms[key])
                if instr.source != [None, None]:
                    del(result.ivarTerms[key])
        delDCvarSources(instr)
    return result

def addDCvarSources(instr, dcSolution):
    """
    Adds the dcvar sources of resistors to instr.circuit for dataType: 'dcvar'.

    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`
    
    :param dcSolution: DC solution of the network obtained from execution of
                       this instruction with dataType: 'dcsolve'
                       
    :type dcSolution: sympy.Matrix
    
    :return: updated instruction object
    :rtype: :class`SLiCAPinstruction.instruction`
    """   
    for el in list(instr.circuit.elements.keys()):
        if 'dcvar' in list(instr.circuit.elements[el].params.keys()):
            DCcurrent = 0
            refDes = instr.circuit.elements[el].refDes     
            if instr.circuit.elements[el].model == 'r':
                pos = instr.depVars().index('I_' + refDes)
                DCcurrent = dcSolution[pos]
            elif instr.circuit.elements[el].model == 'R':
                nodeP, nodeN = instr.circuit.elements[el].nodes
                if nodeP != '0':
                    posP = instr.depVars().index('V_' + nodeP)
                    Vpos = dcSolution[posP]
                else: 
                    Vpos = 0
                if nodeN != '0':
                    posN = instr.depVars().index('V_' + nodeN)
                    Vneg = dcSolution[posN]
                else:
                    Vneg = 0
                DCcurrent = (Vpos - Vneg)/instr.circuit.elements[el].params['value']
            if DCcurrent != 0:
                errorCurrentVariance = instr.circuit.elements[refDes].params['dcvar']/instr.circuit.elements[refDes].params['value']**2 * DCcurrent**2
                newCurrentSource = element()
                newCurrentSource.refDes          = 'I_dcvar_' + refDes
                newCurrentSource.params['dcvar'] = sp.simplify(errorCurrentVariance)
                newCurrentSource.params['noise'] = 0
                newCurrentSource.params['dc']    = 0
                newCurrentSource.params['value'] = 0
                newCurrentSource.model           = 'I'
                newCurrentSource.type            = 'I'
                newCurrentSource.nodes           = instr.circuit.elements[refDes].nodes
                instr.circuit.elements[newCurrentSource.refDes] = newCurrentSource
                instr.circuit.indepVars.append(newCurrentSource.refDes)
    return instr

def delDCvarSources(instr):
    """
    Deletes the dcVar sources from instr.circuit, added by executing this 
    instruction with dataType: 'dcvar'.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`
    
    :return: updated instruction object
    :rtype: :class`SLiCAPinstruction.instruction`
    """
    names = []
    for i in range(len(instr.circuit.indepVars)):
        refDes = instr.circuit.indepVars[i]
        if len(refDes) > 8:
            prefix = refDes[0:8]
            if prefix == 'I_dcvar_':
                del instr.circuit.elements[refDes]
                names.append(refDes)
    for name in names:
        instr.circuit.indepVars.remove(name)
    return instr

def addResNoiseSources(instr):
    """
    Adds the noise sources of resistors to instr.circuit for dataType: 'noise'.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`
    
    :return: updated instruction object
    :rtype: :class:`SLiCAPinstruction.instruction`
    """
    for el in list(instr.circuit.elements.keys()):
        if instr.circuit.elements[el].model.upper() == 'R':
            params = list(instr.circuit.elements[el].params.keys())
            if 'noisetemp' in params:
                Temp = instr.circuit.elements[el].params['noisetemp']
                if Temp != False and Temp != 0 and instr.circuit.elements[el].params['value'] != 0:
                    spectrum = sp.sympify('4*k')*Temp/instr.circuit.elements[el].params['value']
                    if 'noiseflow' in params:
                        flow = instr.circuit.elements[el].params['noiseflow']
                        if flow != False and flow != 0:
                            spectrum *= (1 + flow/ini.frequency)
                    noiseCurrent = element()
                    noiseCurrent.refDes = 'I_noise_' + instr.circuit.elements[el].refDes
                    noiseCurrent.params['noise'] = spectrum
                    noiseCurrent.params['value'] = sp.N(0)
                    noiseCurrent.params['dc']    = sp.N(0)
                    noiseCurrent.params['dcvar'] = sp.N(0)
                    noiseCurrent.model           = 'I'
                    noiseCurrent.type            = 'I'
                    noiseCurrent.nodes           = instr.circuit.elements[el].nodes
                    instr.circuit.elements[noiseCurrent.refDes] = noiseCurrent
                    instr.circuit.indepVars.append(noiseCurrent.refDes)
    # Add the global parameters k and T to the circuit parameter definitions
    Boltzmann = sp.Symbol('k')   
    Temp      = sp.Symbol('T')         
    if Boltzmann not in list(instr.circuit.parDefs.keys()):
        instr.circuit.parDefs[Boltzmann] = SLiCAPPARAMS['k']
    if Temp not in list(instr.circuit.parDefs.keys()):
        instr.circuit.parDefs[Boltzmann] = SLiCAPPARAMS['T']
    return instr

def delResNoiseSources(instr):
    """
    Deletes the noise sources from instr.circuit, added by executing this 
    instruction with dataType: 'noise'.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`
    
    :return: updated instruction object
    :rtype: :class:`SLiCAPinstruction.instruction`
    """
    names = []
    for i in range(len(instr.circuit.indepVars)):
        refDes = instr.circuit.indepVars[i]
        if len(refDes) > 8:
            prefix = refDes[0:8]
            if prefix == 'I_noise_':
                del instr.circuit.elements[refDes]
                names.append(refDes)
    for name in names:
        instr.circuit.indepVars.remove(name)
    return instr

def doDC(instr, result):
    """
    Calculates the DC response at the detector using the parameter 'dc' of
    independent sources as input.
    
    The result will be stored in the .dc attribute of the result object.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`
    """
    if instr.step:
        if ini.stepFunction:
            DCsol = doMaxInstr(instr, result)[0]
            result.dcSolve = stepFunctions(instr.stepDict, DCsol)
        else:
            stepVars = list(instr.stepDict.keys())
            numSteps = len(instr.stepDict[stepVars[0]])
            for i in range(numSteps):
                for j in range(len(stepVars)):
                    instr.parDefs[stepVars[j]]=instr.stepDict[stepVars[j]][i]
                    result = doMaxInstr(instr, result)[0]
    else:
        result = doMaxInstr(instr, result)
        result.dc = result.dc[0]
    return result

def doImpulse(instr, result):
    """
    Calculates the inverse Laplace transform of the source-detector transfer.
    
    First it calculates the Laplace transform of the sou-detector transfer
    and subsequently the inverse Laplace Transform.
    
    The Laplace Transform of the source-detector transfer will be stored in the
    .laplace attribute of the result object.
    
    The result will be stored in the .impulse attribute of the result object.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    instr.dataType = 'laplace'
    result.dataType = 'laplace'
    result = doLaplace(instr, result)
    if instr.step:
        result.impulse = []
        for laplaceResult in result.laplace:
            laplaceResult = normalizeRational(laplaceResult, ini.Laplace)
            result.impulse.append(doMaxIlt(laplaceResult))
    else:
        laplaceResult = normalizeRational(result.laplace, ini.Laplace)
        result.impulse = doMaxIlt(laplaceResult) # calculated the ILT
    instr.dataType = 'impulse'
    result.dataType = 'impulse'
    return result

def doStep(instr, result):
    """
    Calculates the unit step response of the circuit. This is the inverse 
    Laplace transform of the source-detector transfer divided by the Laplace
    variable.
    
    First it calculates the Laplace transform of the source-detector transfer
    and subsequently the inverse Laplace Transform.
    
    The Laplace Transform of the source-detector transfer will be stored in the
    .laplace attribute of the result object.
    
    The unit step response will be stored in the .stepResp  attribute of the
    result object.

    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    instr.dataType = 'laplace'
    result.dataType = 'laplace'
    result = doLaplace(instr, result)
    if instr.step:
        result.stepResp = []
        for laplaceResult in result.laplace:
            laplaceResult = normalizeRational(laplaceResult*1/ini.Laplace, ini.Laplace)
            result.stepResp.append(doMaxIlt(laplaceResult))
    else:
        laplaceResult = normalizeRational(result.laplace*1/ini.Laplace, ini.Laplace)
        result.stepResp = doMaxIlt(laplaceResult)
    instr.dataType = 'step'
    result.dataType = 'step'
    return result

def doTime(instr, result):
    """
    Calculated the inverse Laplace transform of the detector voltage or current.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    instr.dataType = 'laplace'
    result.dataType = 'laplace'
    result = doLaplace(instr, result)
    if instr.step:
        result.time = []
        for laplaceResult in result.laplace:
            laplaceResult = normalizeRational(laplaceResult, ini.Laplace)
            
            result.time.append(doMaxIlt(laplaceResult))
    else:
        laplaceResult = normalizeRational(result.laplace, ini.Laplace)
        result.time = doMaxIlt(laplaceResult) # Modify?
    instr.dataType = 'time'
    result.dataType = 'time'
    return result

def doSolve(instr, result):
    """
    Solves the network: calculates the Laplace transform of all dependent 
    variables.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    if instr.step:
        if ini.stepFunction:
            sol = doMaxInstr(instr, result).solve[0]
            result.solve = stepFunctions(instr.stepDict, sol)
        else:
            stepVars = list(instr.stepDict.keys())
            numSteps = len(instr.stepDict[stepVars[0]])
            for i in range(numSteps):
                for j in range(len(stepVars)):
                    instr.parDefs[stepVars[j]]=instr.stepDict[stepVars[j]][i]
                result.solve.append(doMaxInstr(instr, result))
    else:
        result.solve = doMaxInstr(instr, result).solve[0]
    return result

def doDCsolve(instr, result):
    """
    Finds the DC solution of the network using the .dc attribute of independent
    sources as inputs.
    
    The DC solution will be stored in the .dcSolve attribute of the result
    object.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    if instr.step:
        if ini.stepFunction:
            sol = doMaxInstr(instr, result).dcSolve[0]
            result.dcSolve = stepFunctions(instr.stepDict, sol)
        else:
            stepVars = list(instr.stepDict.keys())
            numSteps = len(instr.stepDict[stepVars[0]])
            for i in range(numSteps):
                for j in range(len(stepVars)):
                    instr.parDefs[stepVars[j]]=instr.stepDict[stepVars[j]][i]
                result.dcSolve.append(doMaxInstr(instr, result))
    else:
        result.dcSolve = doMaxInstr(instr, result).dcSolve[0]
    return result

def doTimeSolve(instr, result):
    """
    Calculates the time-domain solution of the circuit. 
    
    The result will be stored in the .timeSolve attribute of the result object.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    if instr.step:
        if ini.stepFunction:
            sol = doMaxInstr(instr, result).timeSolve[0]
            result.timeSolve = stepFunctions(instr.stepDict, sol)
        else:
            stepVars = list(instr.stepDict.keys())
            numSteps = len(instr.stepDict[stepVars[0]])
            for i in range(numSteps):
                for j in range(len(stepVars)):
                    instr.parDefs[stepVars[j]] = instr.stepDict[stepVars[j]][i]
                result.timeSolve.append(doMaxInstr(instr, result))
    else:
        result.timeSolve = doMaxInstr(instr, result).timeSolve[0]
    return result

def doMatrix(instr, result):
    """
    Calculates the MNA matrix and the vector with dependent and independent 
    variables, based on the conversion type:
        
    - instr.convType == None: The basic MNA equation
    - instr.convType == 'all': The basic equation on a basis of common-mode and
      differential-mode variables
    - instr.convType == 'dd': The differential-mode equivalent representation
    - instr.convType == 'cc': The common-mode equivalent representation
    - instr.convType == 'cd': The differential-mode to common-mode conversion
      reprsentation
    - instr.convType == 'dc': The common-mode to differential-mode conversion
      reprsentation
     
    The results are stored in the following attributes of the result object:
    
    - .Iv: Vector with independent variables (independent voltage and current 
      sources)
    - .Dv: Vector with dependent variables (nodal voltages and branch currents)
    - .M: Matrix: Iv=M*Dv
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    result = makeMaxMatrices(instr, result)
    return result
    
def doMaxIlt(laplaceRational):
    """
    Calculates the inverse Laplace Transform of *laplaceRational* using 
    Maxima CAS.
    
    :param laplaceRational: Sympy rational function of the Laplace variable.
    :type laplaceRational: Sympy.Expr

    :param result: Inverse Laplace Transform of *laplaceRational*
    :type result: Sympy.Expr
    """
    try:
        laplaceRational = normalizeLaplaceRational(laplaceRational)
    except:
        pass
    varList = list(laplaceRational.atoms(sp.Symbol))
    if len(varList) == 1 and varList[0] == ini.Laplace:
        maxInstr = 'string(newIlt(' + python2maxima(laplaceRational) + ',s,t));'
        result = maxEval(maxInstr)
        try:
            result = sp.sympify(result) 
        except:
            print("Error: could not evaluate the Inverse Laplace Transform")
    elif len(varList) > 1 and ini.Laplace in varList:
        maxInstr = 'string(ilt(' + python2maxima(laplaceRational) + ',s,t));'
        result = maxEval(maxInstr)
        try:
            result = sp.sympify(result) 
        except:
            print("Error: could not evaluate the Inverse Laplace Transform")
    else:
        result = sp.DiracDelta(sp.Symbol('t'))*laplaceRational
    if result == sp.Symbol('result'):
        print("Error: could not evaluate the Inverse Laplace Transform")
        result = False
    return result

def doMaxInstr(instr, result):
    """
    Executes an instruction with Maxima CAS and updates *result* with the 
    instruction results.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    maxInstr, result = makeMaxInstr(instr, result)      # Create the maxima instruction
    maxResult = maxEval(maxInstr)                       # Execute the maxima instruction results
    result = parseMaxResult(result, instr.circuit.indepVars, maxResult) # Convert maxima results into SLiCAP results     
    return result

def doMaxFunction(funcName, args):
    """
    Calls a Maxima CAS function and executes it with the given arguments *args*.
    
    :param funcName: Name of the function to be executed.
    :type funcName: str
    
    :param args: List with function arguments
    :type args: list
    
    :return: Sympy expression (execution result)
    :rtype: Sympy.Expr
    """
    maxInstr = "string("
    maxInstr += funcName +'('
    for arg in args:
        maxInstr += str(arg) + ','
    maxInstr = maxInstr[:-1] + '));'
    result = maxEval(maxInstr)
    return sp.sympify(result)

def makeMaxInstr(instr, result):
    """
    Creates the Maxima CAS input for execution of the instruction.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    
    :return: tuple with Input for Maxima CAS and result object.
    :rtype: tuple with str and :class:`allResult()`
    """
    if instr.dataType == 'numer':
        result = makeMaxMatrices(instr, result) 
        detP, detN = makeMaxDetPos(instr, result)  
        maxInstr = 'M : ' + python2maxima(result.M) + '$'
        maxInstr += 'detCols: [' + str(detP) + ',' + str(detN) + ']$'
        maxInstr += 'Iv: ' + python2maxima(result.Iv.transpose()) + '$'
        maxInstr += maxString('doNumer(M,detCols, Iv)', instr.numeric )   
    elif instr.dataType == 'denom': 
        result = makeMaxMatrices(instr, result) 
        maxInstr = 'M:' + python2maxima(result.M) + '$'
        maxInstr += maxString('doDet(M)', instr.numeric )  
    elif instr.dataType == 'laplace':
        result = makeMaxMatrices(instr, result) 
        detP, detN = makeMaxDetPos(instr, result)  
        maxInstr = 'M : ' + python2maxima(result.M) + '$'
        maxInstr += 'detCols:[' + str(detP) + ',' + str(detN) + ']$'
        maxInstr += 'Iv: ' + python2maxima(result.Iv.transpose()) + '$'
        maxInstr += maxString('doLaplace(M,detCols,Iv)', instr.numeric)
    elif instr.dataType == 'dc':
        result = makeMaxMatrices(instr, result) 
        detP, detN = makeMaxDetPos(instr, result) 
        maxInstr = 'M : ' + python2maxima(result.M.subs(ini.Laplace, 0)) + '$'
        maxInstr += 'Iv: ' + python2maxima(result.Iv.subs(ini.Laplace, 0).transpose()) + '$'
        maxInstr += 'detCols:[' + str(detP) + ',' + str(detN) + ']$'
        maxInstr += maxString('doLaplace(M,detCols,Iv)', instr.numeric)
    elif instr.dataType == 'noise':
        result = makeMaxMatrices(instr, result) 
        detP, detN = makeMaxDetPos(instr, result)   
        maxInstr = 'M: ' + python2maxima(result.M) + '$'
        maxInstr += 'detCols:[' + str(detP) + ',' + str(detN) + ']$'
        if instr.source != [None, None] and result.numer[0] !=0:
            maxInstr += 'n: ' + python2maxima(result.numer[0]) + '$'
        else:
            maxInstr += 'n:false$'
        maxInstr += 'Iv:' + python2maxima(result.Iv.transpose()) + '$'
        maxInstr += 'sources:['        
        for name in instr.circuit.indepVars:
            if 'noise' in list(instr.circuit.elements[name].params.keys()):
                value = instr.circuit.elements[name].params['noise']
                result.snoiseTerms[name] = value
                if instr.numeric == True:
                    value = fullSubs(value, instr.parDefs)
                maxInstr += name + '=' + str(value) + ','
        if maxInstr[-1] == ',':
            maxInstr = maxInstr[0:-1]
        maxInstr += ']$'
        maxInstr += maxString('doNoise(M,n,detCols,Iv,sources)', instr.numeric)
    elif instr.dataType == 'dcvar':
        result = makeMaxMatrices(instr, result) 
        detP, detN = makeMaxDetPos(instr, result)   
        maxInstr = 'M: ' + python2maxima(result.M) + '$'
        maxInstr += 'detCols:[' + str(detP) + ',' + str(detN) + ']$'
        if instr.source != [None, None] and result.numer[0] !=0:
            maxInstr += 'n:' + python2maxima(result.numer[0]) + '$'
        else:
            maxInstr += 'n:false$'
        maxInstr += 'Iv:' + python2maxima(result.Iv.transpose().subs(ini.Laplace, 0)) + '$'
        maxInstr += 'sources:['
        for name in instr.circuit.indepVars:
            if 'dcvar' in list(instr.circuit.elements[name].params.keys()):
                value = instr.circuit.elements[name].params['dcvar']
                result.svarTerms[name] = value
                if instr.numeric == True:
                    value = fullSubs(value, instr.parDefs)
                maxInstr += name + '=' + str(value) + ','
        if maxInstr[-1] == ',':
            maxInstr = maxInstr[0:-1]
        maxInstr += ']$'
        maxInstr += maxString('doDCvar(M,n,detCols,Iv,sources)', instr.numeric)
    elif instr.dataType == 'solve':
        result = makeMaxMatrices(instr, result)   
        maxInstr = 'M : ' + python2maxima(result.M) + '$'
        maxInstr += 'Iv: ' + python2maxima(result.Iv.transpose()) + '$'
        maxInstr += maxString('doSolve(M,Iv)', instr.numeric)
    elif instr.dataType == 'dcsolve':
        result = makeMaxMatrices(instr, result)     
        maxInstr = 'M : ' + python2maxima(result.M) + '$'
        maxInstr += 'Iv: ' + python2maxima(result.Iv.transpose()) + '$'
        maxInstr += maxString('doSolveDC(M,Iv)', instr.numeric)
    elif instr.dataType == 'timesolve':
        result = makeMaxMatrices(instr, result) 
        maxInstr = 'M : ' + python2maxima(result.M) + '$'
        maxInstr += 'Iv: ' + python2maxima(result.Iv.transpose()) + '$'
        maxInstr += maxString('doSolveTime(M,Iv)', instr.numeric)
    elif instr.dataType == "poles":
        maxInstr = 'expr: ' + python2maxima(result.denom) + '$'
        maxInstr += maxString('findRoots(expr)', instr.numeric)
    elif instr.dataType == "zeros":
        maxInstr = 'expr: ' + python2maxima(result.numer) + '$'
        maxInstr += maxString('findRoots(expr)', instr.numeric)
    elif instr.dataType == "solve":
        result = makeMaxMatrices(instr, result) 
        maxInstr = 'M :' + python2maxima(result.M) + '$'
        maxInstr += 'Iv:' + python2maxima(result.Iv.transpose()) + '$'
        maxInstr += maxString('doSolve(M,Iv)', instr.numeric)
    elif instr.dataType == "dcsolve":
        result = makeMaxMatrices(instr, result) 
        maxInstr = 'M :' + python2maxima(result.M) + '$'
        maxInstr += 'Iv:' + python2maxima(result.Iv.transpose()) + '$'
        maxInstr += maxString('doSolveDC(M,Iv)', instr.numeric)
        print("Error: no Maxima CAS function implemented for this data type.")     
    return (maxInstr, result)

def maxString(maxInstr, numeric):
    """
    Returns the instruction for maxima with either symbolic or numeric output.
    
    :param maxInstr: Function to be evaluated by maxima CAS.
    :type maxInstr: str
    
    :param numeric: True if the result must be converted to 'big float', else
                    False.
    
    :type numeric: Bool
    
    :return: Maxima instruction for string output.
    :rtype: str.
    """
    if numeric:
        maxInstr = 'string(bfloat(' + maxInstr + '));'
    else:
        maxInstr = 'string(' + maxInstr + ');'
    return maxInstr

def makeMaxMatrices(instr, result):
    """
    Returns an allResults() object of which the following attributes have been 
    updated:
        
        - M  = MNA matrix
        - Iv = Vector with independent variables (voltages and current of 
          independent voltage and current sources, repectively)
        - Dv = Vector with dependent variables (unknown nodal voltages and 
          branch currents)

    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    
    :return: result object with updated attributes Iv, M, and Dv:
    :rtype: SLiCAPprotos.allResults
    """
    # Create the MNA matrix
    result.M, result.Dv = makeMatrices(instr)
    
    # Create vecor with independent variables
    Iv = [0 for i in range(len(instr.depVars()))]
    result.Iv = sp.Matrix(Iv)
    gainTypes = ['gain', 'asymptotic', 'direct']
    if instr.gainType == 'vi':
        if instr.dataType == "noise" or instr.dataType == "dcvar":
            result.Iv = makeSrcVector(instr.circuit, instr.parDefs, 'all', value = 'id', numeric = instr.numeric)
        elif instr.dataType == "dc" or instr.dataType == "dcsolve":
            result.Iv = makeSrcVector(instr.circuit, instr.parDefs, 'all', value = 'dc', numeric = instr.numeric)
        else:
            result.Iv = makeSrcVector(instr.circuit, instr.parDefs, 'all', value = 'value', numeric = instr.numeric)
    elif instr.gainType in gainTypes:
        if instr.source != [None, None]:
            if instr.source[0] == None or instr.source[1] == None:
                ns = 1
            else:
                ns = 2
        for i in range(len(instr.source)):
            if instr.source[i] != None:
                if instr.source[i][0].upper() == 'I':
                    nodeP, nodeN = instr.circuit.elements[instr.source[i]].nodes
                    if nodeP != '0':
                        pos = instr.depVars().index('V_' + nodeP)
                        if instr.convType == 'cc' or instr.convType == 'cd':
                            result.Iv[pos] -= 1/ns
                        else:
                            # differential input
                            result.Iv[pos] -= (-1)**i
                    if nodeN != '0':
                        pos = instr.depVars().index('V_' + nodeN)
                        if instr.convType == 'cc' or instr.convType == 'cd':
                            result.Iv[pos] += 1/ns
                        else:
                            # differential input
                            result.Iv[pos] += (-1)**i
                elif instr.source[i][0].upper() == 'V':
                    pos = instr.depVars().index('I_' + instr.source[i])
                    if instr.convType == 'cc' or instr.convType == 'cd':
                        result.Iv[pos] = 1
                    else:
                        # differential input
                        result.Iv[pos] = (-1)**i/ns
    else:
        result.Iv = makeSrcVector(instr.circuit, instr.parDefs, 'all', value = 'value', numeric = instr.numeric)
    if instr.numeric:
        result.M = sp.N(result.M)
        result.Dv = sp.N(result.Dv)
        result.Iv = sp.N(result.Iv)
    if instr.convType != None:
        result = convertMatrices(instr, result)
    return result

def makeSubsDict(instr):
    """
    Creates a substitution dictionary that does not contain the step parameters
    for the instruction.

    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`
    
    :return: Updated instruction object
    :rtype: :class`SLiCAPinstruction.instruction()`
    """
    if instr.numeric and ini.stepFunction and instr.step:
        instr.parDefs = {}
        for key in list(instr.circuit.parDefs.keys()):
            if key not in list(instr.stepDict.keys()):
                instr.parDefs[key] = instr.circuit.parDefs[key]
    else:
        instr.parDefs = instr.circuit.parDefs
    # Adapt instr.ParDefs for balancing
    if instr.convType != None and instr.removePairSubName:
        instr = pairParDefs(instr)
    return instr

def parseMaxResult(result, indepVars, maxResult):
    """
    Adds Maxima CAS execution results to the result object.
    
    :param result: Result object to which the results must be added
    :type result: :class`SLiCAPprotos.allResults()`
    
    :param inDepVars: Names of independent variables
    :type inDepVars: List of str
    
    :param maxResult: Maxima CAS  execution result.
    :type maxResult: Sympy.Expr
    """
    if result.dataType != 'noise' and result.dataType != 'dcvar' and result.dataType != 'poles' and result.dataType != 'zeros' and result.dataType != 'pz':
        maxResult = sp.sympify(maxResult)
        if result.numeric:
            maxResult = sp.N(maxResult)
        if result.dataType == 'numer':
            result.numer.append(maxResult)
        elif result.dataType == 'denom':
            result.denom.append(maxResult)
        elif result.dataType == 'laplace':
            result.laplace.append(maxResult)
        elif result.dataType == 'impulse':
            result.impulse.append(maxResult)
        elif result.dataType == 'step':
            result.stepResp.append(maxResult)
        elif result.dataType == 'time':
            result.time.append(maxResult)
        elif result.dataType == 'dc':
            result.dc.append(maxResult)
        elif result.dataType == 'solve':
            result.solve.append(maxResult)
        elif result.dataType == 'dcsolve':
            result.dcSolve.append(maxResult)
        elif result.dataType == 'timesolve':
            result.timeSolve.append(maxResult)
    elif result.dataType == 'noise' or result.dataType == 'dcvar':
        oTerms, iTerms = maxResult[2:-2].split('],[')
        oTerms = oTerms.split(',')
        iTerms = iTerms.split(',')
        ot     = sp.N(0) # Detector-referred total
        it     = sp.N(0) # Source-referred total
        if result.dataType == 'noise':
            for j in range(len(indepVars)):
                if indepVars[j] not in list(result.onoiseTerms.keys()):
                    result.onoiseTerms[indepVars[j]] = []
                    result.inoiseTerms[indepVars[j]] = []
                try:
                    term = sp.factor(sp.sympify(oTerms[j]))
                    if term == False:
                        term = sp.N(0)
                except:
                    term = sp.N(0)
                ot += term
                result.onoiseTerms[indepVars[j]].append(term)
                try:
                    term = sp.factor(sp.sympify(iTerms[j]))
                    if term == False:
                        term = sp.N(0)
                except:
                    term = sp.N(0)
                it += term
                result.inoiseTerms[indepVars[j]].append(term)
            result.onoise.append(ot)
            result.inoise.append(it)
        if result.dataType == 'dcvar':
            for j in range(len(indepVars)):
                if indepVars[j] not in list(result.ovarTerms.keys()):
                    result.ovarTerms[indepVars[j]] = []
                    result.ivarTerms[indepVars[j]] = []
                try:
                    term = sp.factor(sp.sympify(oTerms[j]))
                    if term == False:
                        term = sp.N(0)
                except:
                    term = sp.N(0)
                ot += term
                result.ovarTerms[indepVars[j]].append(term)
                try:
                    term = sp.factor(sp.sympify(iTerms[j]))
                    if term == False:
                        term = sp.N(0)
                except:
                    term = sp.N(0)
                it += term
                result.ivarTerms[indepVars[j]].append(term)
            result.ovar.append(ot)
            result.ivar.append(it)
    elif result.dataType == 'poles' or result.dataType == 'zeros':
        if maxResult != '[]':
            results = list(sp.sympify(maxResult))
        else:
            results = []
        if result.dataType == 'poles':
            result.poles.append(results)
        else:
            result.zeros.append(results)
    elif result.dataType == 'pz':
        gain, zeros, poles = maxResult[2:-2].split('],[')
        result.DCvalue.append(sp.sympify(gain))
        poles=poles.split(',')
        try:
            result.poles.append(list(sp.sympify(poles)))
        except:
            pass
        zeros=zeros.split(',')
        try:
            result.zeros.append(list(sp.sympify(zeros)))
        except:
            pass

    return result

def stepFunctions(stepDict, function):
    """
    Substitutes values for step parameters in *function* and returns a list
    of functions with these substitutions.

    :param stepDict: Dictionary with key-value pair:
                     key: step parameter name (*sympy.Symbol*)
                     value: list with step values for this parameter.
    :type stepDict:  Dictionary
    :param function: Function in which the parameters need to be substituted
    :type function: sympy.Expr

    :return: List with functions (*sympy.Expr*). The number of
             functions equals the number of steps. Function i equals
             the input function in which the step variable has been
             replaced with its i-th step value.
    :return type: list
    """
    stepVars = list(stepDict.keys())
    numSteps = len(stepDict[stepVars[0]])
    functions = []
    for i in range(numSteps):
        newFunction = sp.N(function)
        for j in range(len(stepVars)):
            newFunction = newFunction.xreplace({stepVars[j]: stepDict[stepVars[j]][i]})
        functions.append(newFunction)
    return functions

# Functions for converting the MNA matrix anf the vecors with independent and
# dependent variables into equivalent common-mode and differential-mode variables.    

def findBaseNames(instr):
    """
    Returns a list with base names of paired elements. The base name is the 
    element identifier without the pairing extension.
    
    :param instr: instruction with circuit and pairing extensions
    :type instr: SLiCAPinstruction.instruction()
    
    :return: base IDs
    :rtype: list
    """
    lenExt = len(instr.pairExt[0])
    pairedElements = {}
    baseIDs = []
    for refDes in list(instr.circuit.elements.keys()):
        if len(refDes) > lenExt:
            if refDes[-lenExt:] == instr.pairExt[0]:
                if refDes[:-lenExt] not in list(pairedElements.keys()):
                    pairedElements[refDes[:-lenExt]] = [instr.pairExt[0]]
                elif pairedElements[refDes[:-lenExt]][0] == instr.pairExt[1]:
                    pairedElements[refDes[:-lenExt]].append(instr.pairExt[0])
            if refDes[-lenExt:] == instr.pairExt[1]:
                if refDes[:-lenExt] not in list(pairedElements.keys()):
                    pairedElements[refDes[:-lenExt]] = [instr.pairExt[1]]
                elif pairedElements[refDes[:-lenExt]][0] == instr.pairExt[0]:
                    pairedElements[refDes[:-lenExt]].append(instr.pairExt[1])
    for key in list(pairedElements.keys()):
        if len(pairedElements[key]) == 2:
            baseID = key.split('_')[-1]
            if baseID not in baseIDs:
                baseIDs.append(baseID)
    return baseIDs

def pairParDefs(instr):
    """
    Removes the pair extension from paired parameters in both keys and values in
    instr.parDefs.
    
    :param instr: instruction with circuit and pairing extensions
    :type instr: SLiCAPinstruction.instruction()
    
    :return: instr
    :rtupe: SLiCAPinstruction.instruction()
    """
    baseIDs = findBaseNames(instr)
    lenExt  = len(instr.pairExt[0])
    substDict = {}
    newParDefs = {}
    # remove subcircuit extension of paired circuits from parameter names
    for key in list(instr.parDefs.keys()):
        parName = str(key)
        nameParts = parName.split('_')
        if len(nameParts[-1]) > lenExt and nameParts[-1][-lenExt:] in instr.pairExt and nameParts[-1][:-lenExt] in baseIDs:
            value = instr.parDefs[key]
            newParDefs[sp.Symbol(parName[:-lenExt])] = value
            params = list(value.atoms(sp.Symbol))
            # remove subcircuit extension of paired circuits from parameters in expressions
            for param in params:
                parName = str(param)
                nameParts = parName.split('_')
                if len(nameParts[-1]) > lenExt:
                    if nameParts[-1][-lenExt:] in instr.pairExt and nameParts[-1][:-lenExt] in baseIDs:
                        substDict[param] = sp.Symbol(parName[:-lenExt])
        else:
            newParDefs[key] = instr.parDefs[key]
    # perform substitutions
    for param in list(newParDefs.keys()):
        # In parameter names
        newParDefs[param].subs(substDict)
    instr.parDefs = newParDefs
    return instr

def convertMatrices(instr, result):
    """
    Converts the result attributes M, Iv and Dv into those of equivalent
    common-mode or differential mode circuits. 
    
    If instruction.removePairSubName == True, it also removes the pair extensions
    from paired parameters.
    
    The conversion type is defined by the attribute instr.convType it can be:
        
        - 'dd' Diferential-mode transfer
        - 'cc' Common-mode transfer
        - 'dc' Differential-mode to common-mode conversion
        - 'cd' Common-mode to differential-mode conversion
        - 'all' The complete vectors with redefined and re-arranged common-mode
          and differential-mode quantities.
          
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`

    :param result: **allResults()** object that holds instruction results
    :type result: :class:`allResult()`
    """
    pairs, unPaired, dmVars, cmVars, A = createConversionMatrices(instr)
    if instr.removePairSubName:
        baseIDs = findBaseNames(instr)
        lenExt  = len(instr.pairExt[0])
        params = list(set(list(result.M.atoms(sp.Symbol)) + list(result.Iv.atoms(sp.Symbol))))
        substDict = {}   
        for param in params:
            parName = str(param)
            nameParts = parName.split('_')
            if len(nameParts[-1]) > lenExt:
                if nameParts[-1][-lenExt:] in instr.pairExt and nameParts[-1][:-lenExt] in baseIDs:
                    newParam = sp.Symbol(parName[:-lenExt])
                    substDict[param] = newParam           
        result.M = result.M.subs(substDict)
        result.Iv = result.Iv.subs(substDict)
    result.Dv = sp.Matrix(dmVars + cmVars)
    result.M  = A*result.M*A.transpose()
    result.Iv = A*result.Iv
    dimDm = len(pairs)
    dimCm = dimDm + len(unPaired)
    result = getSubMatrices(result, dimDm, dimCm, instr.convType)
    return result
    
def createConversionMatrices(instr):
    """
    Creates the matrax for a base transformation from nodal voltages and branche
    currents to common-mode and differential-mode equivalents.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`
    
    :return: pairs, unPaired, dmVars, cmVars, A
    
             - pairs: a list with tuples with paired variables
             - unPaired: a list with unpaired variables
             - dmVars: a list with differential-mode variables
             - cmVars: a list with common mode variables
             - A: the base transformation matrix
             
    :rtype: tuple
    """
    pairs, unPaired, dmVars, cmVars = pairVariables(instr)
    depVars = [var for var in instr.depVars()]
    dim = len(depVars)
    A = sp.zeros(dim)
    n = len(pairs)
    m = len(unPaired)
    # Create conversion matrix: express nodal voltages and branch currents in
    # corresponding differential-mode and common-mode quantities.
    for i in range(n):
        row0 = i    # differential-mode variable
        row1 = i+n  # common-mode variable
        col0 = depVars.index(pairs[i][0]) # nodal voltage or branch current
        col1 = depVars.index(pairs[i][1]) # nodal voltage or branch current
        if pairs[i][0][0] == 'V':
            # transform pair of node voltages into DM and CM node voltage
            A[i, col0] = 1/2
            A[i, col1]  = -1/2
            A[i+n, col0] = 1
            A[i+n, col1] = 1
        elif pairs[i][0][0] == 'I':
            # transform pair of branch currents into DM and CM branch current
            A[i, col0] = 1
            A[i, col1]  = -1
            A[i+n, col0] = 1/2
            A[i+n, col1] = 1/2
    for i in range(m):
        # Unpaired variable, no transformation
        col = depVars.index(unPaired[i])
        row = 2*n  + i
        A[row, col] = 1 
    return pairs, unPaired, dmVars, cmVars, A

def pairVariables(instr):
    """  
    Combines nodal voltages and branche currents in pairs of variables that
    can be resolved in common-mode, and differential-mode variables.
    
    Pairing is defined by the instr.pairedVars and instr.pairedCircuits.
    
    :param instr: **instruction()** object that holds instruction data.
    :type instr: :class:`instruction()`
    
    :return: pairs, unPaired, dmVars, cmVars
    
             - pairs: a list with tuples with paired variables
             - unPaired: a list with unpaired variables
             - dmVars: a list with differential-mode variables
             - cmVars: a list with common mode variables
             
    :rtype: tuple
    """
    depVars = [var for var in instr.circuit.depVars]
    paired = []
    pairs = []
    unPaired = []
    dmVars = []
    cmVars = []
    sub1, sub2 = instr.pairExt
    if sub1 != None and sub2 != None:
        l_sub1 = len(sub1)
        l_sub2 = len(sub2)
        
        while len(depVars) != 0:
            var = depVars[0]
            if var != 'V_0':
                paired = False
                if var[-l_sub1:] == sub1:
                    pairedVar = var[0:-l_sub1] + sub2
                    if pairedVar in depVars:
                        pairs.append((var, pairedVar))
                        paired = True
                elif var[-l_sub2:] == sub2:
                    pairedVar = var[0:-l_sub2] + sub1
                    if pairedVar in depVars:
                        pairs.append((pairedVar, var))
                        paired = True
                if paired:
                    depVars.remove(var)
                    depVars.remove(pairedVar)
                    if pairs[-1][0][-l_sub1:] == sub1:
                        baseName = pairs[-1][0][0: -l_sub1]
                    if baseName[-1] != '_':
                        baseName += '_'
                    dmVars.append(baseName + 'D')
                    cmVars.append(baseName + 'C')
                else:
                    unPaired.append(var)   
                    depVars.remove(var)
            else:
                depVars.remove(var)
    cmVars += unPaired
    return pairs, unPaired, dmVars, cmVars
  
def getSubMatrices(result, dimDm, dimCm, convType):
    """
    Updates the attributes M, Iv, and Dv of result according to the conversion
    type: convType.
    
    :param result: instruction results of which the matrix attributes M, Iv, 
                   and Dv have been set.
    
    :param dimDm: Number of differential-mode variables
    :type dimDm: str
    
    :param dimCm: Number of common-mode variables
    :type dimCm: str
    
    :param convType: Conversion type, can be 'dd', 'dc', 'cd', 'cc' and 'all'.
    :type convType: str
    
    :result: updated instruction result
    :rtype: :class: SLiCAP.allResults()
    """
    convType = convType.lower()
    if convType == 'dd':
        result.M  = result.M.extract([i for i in range(0, dimDm)],[i for i in range(0, dimDm)])
        result.Iv = sp.Matrix(result.Iv[0:dimDm])
        result.Dv = sp.Matrix(result.Dv[0:dimDm])
    elif convType == 'dc':
        result.M  = result.M.extract([i for i in range(0,dimDm)],[i for i in range(dimDm, dimDm+dimCm)])
        result.Iv = sp.Matrix(result.Iv[0:dimDm])
        result.Dv = sp.Matrix(result.Dv[dimDm:dimDm+dimCm])
    elif convType == 'cd':
        result.M  = result.M.extract([i for i in range(dimDm, dimDm+dimCm)], [i for i in range(0,dimDm)])
        result.Iv = sp.Matrix(result.Iv[dimDm:dimDm+dimCm])
        result.Dv = sp.Matrix(result.Dv[0:dimDm])
    elif convType == 'cc':
        result.M  = result.M.extract([i for i in range(dimDm, dimDm+dimCm)], [i for i in range(dimDm, dimDm+dimCm)])
        result.Iv = sp.Matrix(result.Iv[dimDm:dimDm+dimCm])
        result.Dv = sp.Matrix(result.Dv[dimDm:dimDm+dimCm])
    elif convType == 'all':
        pass
    else:
        print("Warning: unknown conversion type: %s, assuming: 'all'."%(convType))
    return result

if __name__ == '__main__':
    from SLiCAP import initProject
    prj = initProject('testproject')
    #import noiseTest as nt
    import LRC
    print(LRC.result2.solve)