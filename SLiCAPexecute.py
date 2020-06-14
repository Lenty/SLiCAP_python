#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 17:41:46 2020

@author: anton
"""

from SLiCAPyacc import *

#### Return structures depend on data type
        
class allResults(object):
    """
    Return  structure for results, has attributes for all data types and
    instruction data.
    """
    def __init__(self):
        self.DCvalue     = []   # Zero-frequency value in case of 
                                # dataType 'pz'
        self.poles       = []   # Complex frequencies in [rad/s] or [Hz]
        self.zeros       = []   # Complex frequencies in [rad/s] or [Hz]
        self.sources     = []   # Names of the sources with dc variance or noise
        self.srcTerms    = []   # Dict with respective variance or noise
        self.ivarTerms   = []   # Dict with respective contributions to 
                                # source-referred variance
        self.ovarTerms   = []   # Dict with respective contributions to 
                                # detector-referred variance
        self.ivar        = []   # Total source-referred variance
        self.ovar        = []   # Total detector-referred variance
        self.dcSolve     = []   # DC solution of the network
        self.inoiseTerms = []   # Dict with respective spectral contributions
                                # to source-referred noise
        self.onoiseTerms = []   # Dict with espective spectral contributions
                                # to detector-referred noise
        self.inoise      = []   # Total source-referred noise spectral density
        self.onoise      = []   # Total detector-referred noise spectral 
        self.Iv          = None # Vector with independent variables
        self.M           = None # MNA matrix
        self.Dv          = None # Vector with dependent variables
        self.denom       = []   # Laplace poly of denominator
        self.numer       = []   # Laplace poly of numerator
        self.laplace     = []   # Laplace transfer functions
        self.time        = []   # Time-domain responses
        self.impulse     = []   # Unit impulse responses
        self.stepResp    = []   # Unit step responses
        # instruction settings
        self.simType     = None
        self.gainType    = None
        self.dataType    = None
        self.step        = None
        self.stepVar     = None
        self.stepVars    = None
        self.stepMethod  = None
        self.stepStart   = None
        self.stepStop    = None
        self.stepNum     = None
        self.stepList    = []
        self.stepArray   = []
        self.source      = None
        self.detector    = None
        self.lgRef       = None
        self.circuit     = None
        self.parDefs     = None
        self.numeric     = None
        self.errors      = 0
       
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
            (instObj.Iv, instObj.M, instObj.Dv) = makeMatrices(instObj.circuit, instObj.parDefs, instObj.numeric, instObj.gainType, instObj.lgRef)
            # Do stepping by means of substitution in the numerator and denominator
            if instObj.dataType == 'poles':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                # pz analysis is numeric so better lambdify!
                for poly in denoms:
                    instObj.poles.append(numRoots(poly, LAPLACE))
                instObj.zeros = []
            elif instObj.dataType == 'zeros':
                numer = doNumer(instObj)
                numers = stepFunctions(instObj, numer)
                for poly in numers:
                    instObj.zeros.append(numRoots(poly, LAPLACE))
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
                    poles = numRoots(denoms[i], LAPLACE)
                    zeros = numRoots(numers[i], LAPLACE)
                    (poles, zeros) = cancelPZ(poles, zeros)
                    instObj.poles.append(poles)
                    instObj.zeros.append(zeros)
                    try:
                        # Lets try a real limit with Maxima CAS
                        instObj.DCvalue.append(maxLimit(numers[i]/denoms[i], str(LAPLACE), '0', 'plus'))
                    except:
                        # If not just substitute s=0 with Sympy
                        instObj.DCvalue.append(sp.Subs(numers[i]/denoms[i], LAPLACE, 0))
            elif instObj.dataType == 'step':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                numer = doNumer(instObj)
                numers = stepFunctions(instObj, numer)
                for i in range(len(denoms)):
                    try:
                        instObj.stepResp.append(invLaplace(numers[i], denoms[i]*LAPLACE))
                    except:
                        print "Warning: could not calculate the unit step response."
            elif instObj.dataType == 'impulse':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                numer = doNumer(instObj)
                numers = stepFunctions(instObj, numer)
                for i in range(len(denoms)):
                    try:
                        instObj.stepResp.append(invLaplace(numers[i], denoms[i]))
                    except:
                        print "Warning: could not calculate the unit impulse response."
            elif instObj.dataType == 'time':
                pass
            elif instObj.dataType == 'numer':
                numer = doNumer(instObj)
                instObj.numer = stepFunctions(instObj, numer)
            elif instObj.dataType == 'denom':
                denom = doDenom(instObj)
                instObj.denom = stepFunctions(instObj, denom)
            elif instObj.dataType == 'laplace':
                denom = doDenom(instObj)
                denoms = stepFunctions(instObj, denom)
                numer = doNumer(instObj)
                numers = stepFunctions(instObj, numer)
                instObj.laplace = []
                for i in range(len(denoms)):
                    instObj.laplace.append(normalizeLaplaceRational(numers[i], denoms[i]))
            elif instObj.dataType == 'solve':
                pass
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
    # The lambdify method was not faster
    if instObj.stepMethod == 'array':
        func = sp.lambdify(instObj.stepVars, function)
        functions = [func(instObj.stepArray[i]) for i in range(len(instObj.stepArray))]
    else:
        func = sp.lambdify(instObj.stepVar, function)
        functions = [func(instObj.stepList[i]) for i in range(len(instObj.stepList))]
    """
    # One by one substitition
    if instObj.stepMethod == 'array':
        functions = []
        for i in range(len(instObj.stepArray[0])):
            subsList = []
            for j in range(len(instObj.stepVars)):
                subsList.append((instObj.stepVars[j], instObj.stepArray[j][i]))
            functions.append(function.subs(subsList))
    else:
        functions = [function.subs(instObj.stepVar, instObj.stepList[i]) for i in range(len(instObj.stepList))]
    return functions

def doDataType(instObj):
    """
    Returns the instruction object with the result of the execution without 
    parameter stepping
    """
    (instObj.Iv, instObj.M, instObj.Dv) = makeMatrices(instObj.circuit, instObj.parDefs, instObj.numeric, instObj.gainType, instObj.lgRef)
    if instObj.dataType == 'matrix':
        pass
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
            instObj.stepResp = invLaplace(doNumer(instObj), doDenom(instObj)*LAPLACE)
        except:
            print "Warning: could not calculate the unit step response."
    elif instObj.dataType == 'impulse':
        try:
            instObj.stepResp = invLaplace(doNumer(instObj), doDenom(instObj))
        except:
            print "Warning: could not calculate the unit impulse response."
    elif instObj.dataType == 'time':
        pass 
    elif instObj.dataType == 'solve':
        pass            
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
    return denom


def doPoles(instObj):
    """
    Calculates the denominator of a transfer from source to detector and find
    the poles.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: List with zeros, empty list if no zeros are found.
    """
    denom = sp.expand(sp.collect(doDenom(instObj).evalf(), LAPLACE))
    return numRoots(denom, LAPLACE)

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
    of the cofactors.
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
    return(detP, detN, srcP, srcN)
    
def doNumer(instObj):
    """
    Calculates the numerator of a transfer by evaluating cofactors.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: Sympy expression.
    """
    (detP, detN, srcP, srcN) = makeSrcDetPos(instObj)
    numer = maxNumer(instObj.M, detP, detN, srcP, srcN)
    if instObj.gainType == 'loopgain' or instObj.gainType == 'servo':
        (lgNumer, lgDenom) = sp.fraction(sp.together(lgValue(instObj)))
        numer *= lgNumer
    elif instObj.gainType == 'servo':
        numer *= -lgNumer
    return numer

def doZeros(instObj):
    """
    Calculates the numerator of a transfer from source to detector and find the
    zeros.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: List with zeros, empty list if no zeros are found.
    """
    numer = sp.expand(sp.collect(doNumer(instObj).evalf(), LAPLACE))
    return numRoots(numer, LAPLACE)
    
def doPZ(instObj):
    """
    Calculates the numerator and the denominator of the transfer from source to
    detector and determines the zero-frequency value, the poles and the zeros.
    
    instObj:      Instruction object with MNA matrix stored in 'instrObject.M'
    return value: List with poles, list with zeros, DCvalue.
    """
    numer = sp.expand(sp.collect(doNumer(instObj).evalf(), LAPLACE))
    denom = sp.expand(sp.collect(doDenom(instObj).evalf(), LAPLACE))
    poles = numRoots(denom, LAPLACE)
    zeros = numRoots(numer, LAPLACE)
    (poles, zeros) = cancelPZ(poles, zeros)
    try:
        # Lets try a real limit with maxima
        DCvalue = maxLimit(numer/denom, str(LAPLACE), '0', 'plus')
    except:
        # If not just substitute s=0
        DCvalue = sp.Subs(numer/denom, LAPLACE, 0)
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
    return normalizeLaplaceRational(numer, denom)

def checkNumeric(expr, stepVar = None):
    """
    Checks if the expressions does not contain parameters other then stepVar',
    'LAPLACE', 'FREQUECY' or 'OMEGA'.
    
    expr:         Sympy expression
    stepVar:      str or Sympy.Symbol
    return value: 'True' if numeric, else 'False'.
    """
    numeric = True
    if type(expr) == str:
        expr = sp.N(sp.sympify(expr))
    if isinstance(expr, tuple(sp.core.all_classes)):
        expr = sp.N(expr)
        params = list(expr.free_symbols)
        for par in params:
            if stepVar == None and par != LAPLACE and par != FREQUENCY and par != OMEGA:
                numeric = False
            elif par != stepVar and par != LAPLACE and par != FREQUENCY and par != OMEGA:
                numeric = False
    return numeric

if __name__ == '__main__':
    pass