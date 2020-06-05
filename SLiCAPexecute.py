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
    Return  structure for results, has attributes for all data types
    """
    def __init__(self):
        self.DCvalue     = None # Zero-frequency value in case of 
                                # dataType 'pz'
        self.poles       = None # Complex frequencies in [rad/s] or [Hz]
        self.zeros       = None # Complex frequencies in [rad/s] or [Hz]
        self.sources     = None # Names of the sources with dc variance or noise
        self.srcTerms    = None # Dict with respective variance or noise
        self.ivarTerms   = None # Dict with respective contributions to 
                                # source-referred variance
        self.ovarTerms   = None # Dict with respective contributions to 
                                # detector-referred variance
        self.ivar        = None # Total source-referred variance
        self.ovar        = None # Total detector-referred variance
        self.dcSolve     = None # DC solution of the network
        self.inoiseTerms = None # Dict with respective spectral contributions
                                # to source-referred noise
        self.onoiseTerms = None # Dict with espective spectral contributions
                                # to detector-referred noise
        self.inoise      = None # Total source-referred noise spectral density
        self.onoise      = None # Total detector-referred noise spectral 
        self.Iv          = None # Vector with independent variables
        self.M           = None # MNA matrix
        self.Dv          = None # Vector with dependent variables
        self.laplace     = None # Laplace transfer functions
        self.time        = None # Time-domain responses
        self.impulse     = None # Unit impulse responses
        self.step        = None # Unit step responses
        self.denom       = None # Laplace poly of denominator
        self.numer       = None # Laplace poly of numerator
    
        
def doInstruction(instObj):
    # In this case we need substitution and things get different with 
    # parameter stepping:
    if instObj.step == True and instObj.stepMethod != 'array':
        try:
            del instObj.parDefs[instObj.stepVar]
        except:
            pass
    elif instObj.step == True and instObj.stepMethod == 'array':
        # In this case we build the matrix for every step
        pass
    else:
        pass
    if instObj.errors == 0:
        if instObj.simType == 'numeric':
            numeric = True
        else:
            numeric = False
        (instObj.Iv, instObj.M, instObj.Dv) = makeGainType(instObj, numeric)
        if instObj.dataType == 'matrix':
            instObj.results.Iv = instObj.Iv
            instObj.results.M = instObj.M
            instObj.results.Dv = instObj.Dv
        elif instObj.dataType == 'poles':
            instObj.results.poles = doPoles(instObj)  
            instObj.results.zeros = []
            instObj.DCvalue = None
        elif instObj.dataType == 'zeros':
            instObj.results.zeros = doZeros(instObj)
            instObj.results.poles == []
            instObj.DCvalue = None
        elif instObj.dataType == 'pz':
            (poles, zeros, DCvalue) = doPZ(instObj)
            instObj.results.poles = poles
            instObj.results.zeros = zeros
            instObj.results.DCvalue = DCvalue
        elif instObj.dataType == 'denom':
            denom = doDenom(instObj)
            instObj.results.denom = denom
        elif instObj.dataType == 'numer':
            numer = doNumer(instObj)
            instObj.results.numer = numer
        elif instObj.dataType == 'laplace':
            laplace = doLaplace(instObj)
            instObj.results.laplace = laplace           
    return instObj

def makeGainType(instObj, numeric, subsDict = None):
    """
    Adds the matrices (Iv, M and Dv) to the instruction object 'instObj.
    When single-parameter stepping is enabled, the step variable is kept
    symbolic in the matrix. Single-parameter stepping will then be done after 
    the transfer, a numerator or a denominator has been calculated.
    Multi-parameter stepping is done by creating the matrix with each step.
    """
    if instObj.step == True and instObj.stepMethod != 'array':
        # make a copy of the parameter definitions, but do not include the
        # step variable
        parDefs = {}
        stepVar = sp.Symbol(instObj.stepVar)
        for key in instObj.circuit.parDefs.keys():
            if key != stepVar:
                parDefs[key] = instObj.circuit.parDefs[key]
    elif instObj.step == True and instObj.stepMethod == 'array' and subsDict != None:
        parDefs = subsDict
    else:
        parDefs = instObj.circuit.parDefs
    return makeMatrices(instObj.circuit, parDefs, numeric, gainType = instObj.gainType, lgRef = instObj.lgRef)

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

def doImpulse(instrObj):
    numer = doNumer(instObj)
    denom = doDenom(instObj)
    Fs = numer/denom
    try:
        impulse = maxILT(Fs)
    except:
        pass
    return impulse

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