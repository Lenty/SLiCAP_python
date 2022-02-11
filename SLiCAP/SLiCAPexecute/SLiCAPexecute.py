#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 17:08:41 2021

@author: anton
"""
from SLiCAP.SLiCAPyacc import *

LGREF = sp.Symbol('_LGREF_')
MAXFUNCTIONS = {}

MAXFUNCTIONS['doDet'] = """MAXMATRIXDIM:25$doDet(M):=block([],if length(M)>MAXMATRIXDIM
then result:det(M) else result:newdet(M),return(result))$
det(M):=block([D,dim,i],dim:length(M),if dim=2 then D:M[1,1]*M[2,2]-M[1,2]*M[2,1]
else block(D:0,for i from 1 thru dim do if M[1,i] # 0 then 
D:D+M[1,i]*(-1)^(i+1)*det(minor(M,1,i))),return(expand(D)))$compile(det)$"""

MAXFUNCTIONS['doNumer'] = """
doNumer(M,srcRows,detCols):=block([],result: 0,if srcRows[1]#0  then if detCols[1]#0 then 
result: result+(-1)^(srcRows[1]+detCols[1])*doDet(minor(M,srcRows[1],detCols[1])),
if srcRows[1]#0 then if detCols[2]#0 then 
result:result-(-1)^(srcRows[1]+detCols[2])*doDet(minor(M,srcRows[1],detCols[2])),
if srcRows[2]#0 then if detCols[1]#0 then 
result:result-(-1)^(srcRows[2]+detCols[1])*doDet(minor(M,srcRows[2],detCols[1])),
if srcRows[2]#0 then if detCols[2]#0 then 
result:result+(-1)^(srcRows[2]+detCols[2])*doDet(minor(M,srcRows[2],detCols[2])),
return(result))$"""

MAXFUNCTIONS['doLaplace'] = """
doLaplace(M,srcRows,detCols,Iv,gainType):=block([],
if gainType="vi" then result:doCramer(M,detCols,Iv)
else result:doNumer(M,srcRows,detCols)/doDet(M),return(result))$
doCramerNumer(M,detCols,Iv):=block([],result:0,
if detCols[1]#0 then result:result+doDet(CramerMatrix(M,Iv,detCols[1])),
if detCols[2]#0 then result:result-doDet(CramerMatrix(M,Iv,detCols[2])),
return(expand(result)))$
doCramer(M,detCols,Iv):=block([],return(expand(doCramerNumer(M,detCols,Iv)/doDet(M))))$
CramerMatrix(M,V,c):=block([],CramerMatrix:transpose(M),
CramerMatrix[c]:V[1],return(transpose(CramerMatrix)))$"""

MAXFUNCTIONS['normalize'] = """
normalizeLaplaceRational(expr):=block([denExpr,numExpr,normDenom,normNumer,i,lowestCoeff],
denExpr:denom(expr),numExpr:num(expr),normDenom:0,normNumer:0,lowestCoeff:coeff(denExpr,s,lopow(denExpr,s)),
for i from 0 thru hipow(denExpr,s) do normDenom:normDenom+s^i*fullratsimp(coeff(denExpr,s,i)/lowestCoeff),
for i from 0 thru hipow(numExpr,s) do normNumer:normNumer+s^i*fullratsimp(coeff(numExpr,s,i)/lowestCoeff),
expr: normNumer/normDenom,return(expr))$"""

MAXFUNCTIONS['newIlt'] = """
newIlt(ratLaplace,s,t):=block([oldD,oldP],oldD:demoivre,oldP:polyfactor,demoivre:true,polyfactor:true,
result:bfloat(expand(ilt(expand(num(ratLaplace))/(allroots(expand(denom(ratLaplace)))),s,t))),
demoivre:oldD,polyfactor:oldP,return(result))$
doIlt(expr,s,t):=block([lof],lof:listofvars(expr),if length(lof)=1 and lof[1]=s then 
expr:newIlt(bfloat(expr),s,t) else expr:ilt(expr,s,t),return(expr))$"""

MAXFUNCTIONS['doNoise'] = """
doNoise(M,srcRows,detCols,Iv,sources):=block(
[den,n,onoise,srcName,srcValue,noiseTerm,onoiseTerms:[],inoiseTerms:[]],
den:subst([s=%i*2*pi*f],doDet(M)),den: factor(den*conjugate(den)),if srcRows#[0,0]
then (n:doNumer(M, srcRows, detCols),n:subst([s=%i*2*%pi*f],n),n:factor(n*conjugate(n)))
else n:false,onoise:subst([s=%i*2*%pi*f],doCramerNumer(M,detCols,Iv)),
for i from 1 thru length(sources) do (srcName:lhs(sources[i]),srcValue:rhs(sources[i]),
noiseTerm:coeff(onoise,srcName,1),noiseTerm:factor(noiseTerm*conjugate(noiseTerm)),
onoiseTerms:append(onoiseTerms,[factor(fullratsimp(noiseTerm/den))*srcValue]),
if n#false then inoiseTerms:append(inoiseTerms,[factor(fullratsimp(noiseTerm/n))*srcValue])
else inoiseTerms:append(inoiseTerms,[false])),return([onoiseTerms,inoiseTerms]))$"""

MAXFUNCTIONS['doDCvar'] = """
doDCvar(M,srcRows,detCols,Iv,sources):=block(
[den,n,ovar,srcName,srcValue,varTerm,ovarTerms:[],ivarTerms:[]],
M:subst([s=0],M),den:(doDet(M))^2,if srcRows#[0,0]
then (n:doNumer(M,srcRows,detCols),n:n^2) else n:false,ovar:doCramerNumer(M,detCols,Iv),
for i from 1 thru length(sources) do (srcName:lhs(sources[i]),srcValue:rhs(sources[i]),
varTerm:coeff(ovar,srcName,1)^2,ovarTerms:append(ovarTerms,[factor(fullratsimp(varTerm/den))*srcValue]),
if n#false then ivarTerms:append(ivarTerms,[factor(fullratsimp(varTerm/n))*srcValue])
else ivarTerms:append(ivarTerms,[false])),return([ovarTerms,ivarTerms]))$"""

MAXFUNCTIONS['solve'] = """
doSolve(M,Iv):=block([],result:factor(invert(M).transpose(Iv)),return(result))$
doSolveDC(M,Iv):=block([],M:subst([s=0],M),Iv:subst([s=0],Iv),result:doSolve(M,Iv),return(result))$
doSolveTime(M,Iv):=block([l,i],expr:doSolve(M,Iv),l:length(transpose(Iv)),for i from 1 thru l do 
expr[i][1]:doIlt(expr[i][1],s,t),return(expr))$"""

MAXFUNCTIONS['pz'] = """
roots(listWithExpr):=block([],results:[],for i from 1 thru length(listWithExpr) do 
results:append(results,[findRoots(listWithExpr[i])]),return(results))$
findRoots(expr):=block([lof],lof:listofvars(expr),if length(lof)=1 and lof[1]=s then
result: allroots(bfloat(expr)) else result:solve(expr,s),for i from 1 thru length(result) do
result[i]:rhs(result[i]),return(result))$
numRoots(expr):=block([],result:allroots(bfloat(expr)),for i from 1 thru length(result) do
result[i]:rhs(result[i]),return(result))$
"""

MAXFUNCTIONS['doReturnRatio'] = """
doReturnRatio(det_M, det_M0, denomLG):=block([],
result:fullratsimp((det_M0*denomLG-det_M)/(det_M0*denomLG)),
return(result))$
"""
MAXFUNCTIONS['doLoopGain'] = """
MAXMATRIXDIM:25$doDet(M):=block([],if length(M)>MAXMATRIXDIM
then result:det(M) else result:newdet(M),return(result))$
det(M):=block([D,dim,i],dim:length(M),if dim=2 then D:M[1,1]*M[2,2]-M[1,2]*M[2,1]
else block(D:0,for i from 1 thru dim do if M[1,i] # 0 then 
D:D+M[1,i]*(-1)^(i+1)*det(minor(M,1,i))),return(expand(D)))$compile(det)
$doLoopGain(M,lgRef):=block([],
M_D:subst(""" + str(LGREF) + """=lgRef,M),
D_M:doDet(M_D),
M_0:subst(""" + str(LGREF) + """=0,M),
D_0:doDet(M_0),
result:fullratsimp((D_0-D_M)/D_0),
return(result))$
"""

MAXFUNCTIONS['doServo'] = """
MAXMATRIXDIM:25$doDet(M):=block([],if length(M)>MAXMATRIXDIM
then result:det(M) else result:newdet(M),return(result))$
det(M):=block([D,dim,i],dim:length(M),if dim=2 then D:M[1,1]*M[2,2]-M[1,2]*M[2,1]
else block(D:0,for i from 1 thru dim do if M[1,i] # 0 then 
D:D+M[1,i]*(-1)^(i+1)*det(minor(M,1,i))),return(expand(D)))$compile(det)$
doServo(M,lgRef):=block([],
M_D:subst(""" + str(LGREF) + """=lgRef,M),
D_M:doDet(M_D),
M_0:subst(""" + str(LGREF) + """=0,M),
D_0:doDet(M_0),
result:fullratsimp((D_0-D_M)/D_M),
return(result))$
"""

def createResultObject(instr):
    """
    Returns an instance of the *allResults* object with the instruction daya copeid to it.
    
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
    # Make a deep copy of the list
    if type(instr.stepVars) == list:
        for var in instr.stepVars:
            result.stepVars.append(var)
    result.stepMethod     = instr.stepMethod
    result.stepStart      = instr.stepStart
    result.stepStop       = instr.stepStop
    result.stepNum        = instr.stepNum
    result.stepList       = []
    # Make a deep copy of the list
    for num in instr.stepList:
        result.stepList.append(num)
    result.stepArray      = []
    # Make a deep copy of the array
    for row in instr.stepArray:
        if type(row) == list:
            rowCopy = []
            for num in row:
                rowCopy.append(num)
            result.stepArray.append(rowCopy)
    result.source         = instr.source
    result.detector       = instr.detector
    result.detPairs       = instr.detPairs
    result.lgRef          = instr.lgRef
    result.circuit        = instr.circuit
    result.errors         = instr.errors
    result.detUnits       = instr.detUnits
    result.detLabel       = instr.detLabel
    result.srcUnits       = instr.srcUnits
    result.numeric        = instr.numeric
    result.label          = instr.label
    result.parDefs        = instr.parDefs
    return result   

def makeMaxSrcDetPos(instr):
    """
    Returns the number of the source row(s) and detector colum(s) for
    calculation of cofactors or for application of Cramer's rule.

    The number range is from 0 to the dimension of the matrix. Zero is
    used for the reference node.

    :param instr: **allResults()** object that holds instruction data.
    :type instr: :class:`allResult()`

    :return: tuple: (detP, detN, srcP, srcN):

            - detP (*int, int*): number of the row of the vector with dependent
              variables that corresponds with the positive detector
            - detN (*int, int*): number of the row of the vector with dependent
              variables that corresponds with the negative detector
            - srcP (*int, int*): number of the row of the vector with dependent
              variables that corresponds with the positive source
            - srcN (*int, int*): number of the row of the vector with dependent
              variables that corresponds with the negative source

    :return type: tuple
    """
    detectors = []
    for var in instr.circuit.depVars:
        if var != 'V_0':
            detectors.append(var)
    detP, detN = instr.detector
    if detP != None:
        detP = detectors.index(detP) + 1
    else:
        detP = 0
    if detN != None:
        detN = detectors.index(detN) + 1
    else:
        detN = 0
    if instr.source != None:
        # If there is s source defined:
        if instr.source[0].upper() == 'V':
            # The source row corresponds with that of the current through
            # the voltage source
            srcP = detectors.index('I_' + instr.source) + 1
            srcN = 0
        elif instr.source[0].upper() == 'I':
            # The source rows correspond with those of the nodal voltages
            # of the source nodes
            nodes = instr.circuit.elements[instr.source].nodes
            if nodes[0] != '0':
                srcN = detectors.index('V_' + nodes[0]) + 1
            else:
                srcN = 0
            if nodes[1] != '0':
                srcP = detectors.index('V_' + nodes[1]) + 1
            else:
                srcP = 0
    else:
        # If there is no source defined, srcP and srcN are set to 0
        srcP = 0
        srcN = 0
    return(detP, detN, srcP, srcN)

def lgValue(instr):
    """
    Return the gain of the loop gain reference.

    :param instr: SLiCAP instruction* object with the instruction data.
    :type instr: SLiCAPinstruction.instruction()`

    :return: Gain of the loop gain reference.

    :return type: sympy.Expr
    """
    value = instr.circuit.elements[instr.lgRef].params['value']
    if instr.simType == 'numeric':
        value = fullSubs(sp.N(value), instr.parDefs)
    return value

def doInstruction(instr):
    result = createResultObject(instr)
    if instr.errors == 0:
        instr = makeSubsDict(instr)        
        if instr.gainType == 'asymptotic':
            # The reference variable needs to replaced with a nullor and both the 
            # self.circuit.depVars and self.varIndex need to be changed accordingly.
            # Old values need to be restored after execution of the instruction.
            oldLGrefElement = instr.circuit.elements[instr.lgRef]
            newLGrefElement = element()
            newLGrefElement.nodes = oldLGrefElement.nodes
            newLGrefElement.model = 'N'
            newLGrefElement.type = 'N'
            newLGrefElement.refDes = oldLGrefElement.refDes
            instr.circuit.elements[instr.lgRef] = newLGrefElement
            instr.circuit = updateCirData(instr.circuit)
        elif instr.gainType == 'direct':
            oldLGvalue = instr.circuit.elements[instr.lgRef].params['value']
            instr.circuit.elements[instr.lgRef].params['value'] = sp.N(0)
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
            instr.circuit.elements[instr.lgRef] = oldLGrefElement
            instr.circuit = updateCirData(instr.circuit) 
        elif instr.gainType == 'direct':
             instr.circuit.elements[instr.lgRef].params['value'] = oldLGvalue
    return result

def doNumer(instr, result):
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
    if instr.step:
        if ini.stepFunction:
            if instr.gainType == 'loopgain' or instr.gainType == 'servo':
                numer, denom = sp.fraction(doLoopGainServo(instr, result))
            else:
                denom = doMaxInstr(instr, result).denom[0]
                if instr.gainType == 'loopgain':
                    lgNumer, lgDenom = sp.fraction(lgValue(instr))
                    denom *= lgDenom
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
    """
    oldDataType = instr.dataType
    instr.dataType = 'matrix'
    result.dataType = 'matrix'
    oldLGvalue = instr.circuit.elements[instr.lgRef].params['value']
    
    instr.circuit.elements[instr.lgRef].params['value'] = LGREF
    result = doMatrix(instr, result)
    
    instr.circuit.elements[instr.lgRef].params['value'] = oldLGvalue
    num, den = doMaxLoopGainServo(instr, result)
    if instr.numeric:
        num = sp.N(num)
        den = sp.N(den)
    result.denom.append(den)
    result.numer.append(num)
    result.laplace.append(num/den)
    
    instr.dataType = oldDataType
    result.dataType = oldDataType
    return num/den

def doMaxLoopGainServo(instr, result):
    """
    """
    M = python2maxima(result.M)
    if instr.gainType == 'loopgain':
        maxResult = doMaxFunction('doLoopGain', [M, lgValue(instr)])
        numer, denom = sp.fraction(maxResult)
    elif instr.gainType == 'servo':
        numer, denom = sp.fraction(doMaxFunction('doServo', [M, lgValue(instr)]))  
    return numer, denom

def doPoles(instr, result):
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

def doNoise(instr, result):
    if instr.step:
        if ini.stepFunction:
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
                result = doMaxInstr(instr, result)   
    else:
        result = doMaxInstr(instr, result)
        result.onoise = result.onoise[0]
        result.inoise = result.inoise[0]
        for key in list(result.onoiseTerms.keys()):
            if len(result.onoiseTerms[key]) > 0:
                result.onoiseTerms[key] = result.onoiseTerms[key][0]
                if instr.source != None:
                    result.inoiseTerms[key] = result.inoiseTerms[key][0]
            else:
                del(result.onoiseTerms[key])
                if instr.source != None:
                    del(result.inoiseTerms[key])
    return result

def doDCvar(instr, result):
    if instr.step:
        if ini.stepFunction:
            instr.dataType = 'dcsolve'
            result.dataType = 'dcsolve'
            result = doDCsolve(instr, result)
            
            Dv = result.Dv
            instr.dataType = 'dcvar'
            result.dataType = 'dcvar'
            instr = addDCvarSources(instr, Dv)
            varResult = doMaxInstr(instr, result)
            result.ovar = stepFunctions(instr.stepDict, varResult.ovar[0])
            result.ivar = stepFunctions(instr.stepDict, varResult.ivar[0])
            for srcName in list(varResult.ovarTerms.keys()):
                result.ovarTerms[srcName] = stepFunctions(instr.stepDict, varResult.ovarTerms[srcName][0])
                result.ivarTerms[srcName] = stepFunctions(instr.stepDict, varResult.ivarTerms[srcName][0])
            instr = delDCvarSources(Dv)
        else:
            stepVars = list(instr.stepDict.keys())
            numSteps = len(instr.stepDict[stepVars[0]])
            for i in range(numSteps):
                for j in range(len(stepVars)):
                    instr.parDefs[stepVars[j]]=instr.stepDict[stepVars[j]][i]
                instr.dataType = 'dcsolve'
                result.dataType = 'dcsolve'
                result = doDCsolve(instr, result)
                Dv = result.Dv
                instr.dataType = 'dcvar'
                result.dataType = 'dcvar'
                instr  = addDCvarSources(instr, Dv)
                result = doMaxInstr(instr, result)
                instr  = delDCvarSources(instr, Dv)
    else:
        instr.dataType = 'dcsolve'
        result.dataType = 'dcsolve'
        result = doDCsolve(instr, result)            
        Dv = result.Dv
        instr.dataType = 'dcvar'
        result.dataType = 'dcvar'
        instr  = addDCvarSources(instr, Dv, result.dcSolve)
        result = doMaxInstr(instr, result)
        instr  = delDCvarSources(instr, Dv)
        result.ovar = result.ovar[0]
        result.ivar = result.ivar[0]
        for key in list(result.ovarTerms.keys()):
            if len(result.ovarTerms[key]) > 0:
                result.ovarTerms[key] = result.ovarTerms[key][0]
                if instr.source != None:
                    result.ivarTerms[key] = result.ivarTerms[key][0]
            else:
                del(result.ovarTerms[key])
                if instr.source != None:
                    del(result.ivarTerms[key])
    return result

def addDCvarSources(instr, Dv, dcSolution):
    for variable in Dv:
        variable = str(variable)
        varType = variable[0]
        refDes  = variable[2:]
        if varType.upper() == 'I' and refDes[0].upper() == 'R' and 'dcvar' in list(instr.circuit.elements[refDes].params.keys()):
            # Calculate the error current
            errorCurrentVariance = instr.circuit.elements[refDes].params['dcvar']/ instr.circuit.elements[refDes].params['value']**2 * dcSolution[instr.circuit.varIndex[variable]]**2
            # Add a current source to the sicuit elements
            newCurrentSource = element()
            newCurrentSource.refDes          = variable
            newCurrentSource.params['dcvar'] = sp.simplify(errorCurrentVariance)
            newCurrentSource.params['noise'] = 0
            newCurrentSource.params['dc']    = 0
            newCurrentSource.params['value'] = 0
            newCurrentSource.model           = 'I'
            newCurrentSource.nodes           = instr.circuit.elements[refDes].nodes
            instr.circuit.elements[variable] = newCurrentSource
            instr.circuit.indepVars.append(variable)
    return instr

def delDCvarSources(instr, Dv):
    for variable in Dv:
        variable = str(variable)
        varType = variable[0]
        refDes  = variable[2:]
        if varType.upper() == 'I' and refDes[0].upper() == 'R' and 'dcvar' in list(instr.circuit.elements[refDes].params.keys()):
            # Delete DC variance sources added by a previous dcVar analysis
            if variable in list(instr.circuit.elements.keys()):
                del(instr.circuit.elements[variable])
                instr.circuit.depVars.remove(variable)
    return instr

def doDC(instr, result):
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
        result.impulse = doMaxIlt(laplaceResult) # Modify?
    instr.dataType = 'impulse'
    result.dataType = 'impulse'
    return result

def doStep(instr, result):
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
        result.stepResp = doMaxIlt(laplaceResult) # Modify?
    instr.dataType = 'step'
    result.dataType = 'step'
    return result

def doTime(instr, result):
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
    result.M, result.Iv, result.Dv = makeMaxMatrices(instr)
    return result
    
def doMaxIlt(laplaceRational):
    try:
        laplaceRational = normalizeLaplaceRational(laplaceRational)
    except:
        pass
    maxInstr = "assume_pos:true$assume_pos_pred:symbolp$ratprint:false$"
    maxInstr += MAXFUNCTIONS['newIlt']
    varList = list(laplaceRational.atoms(sp.Symbol))
    if len(varList) == 1 and varList[0] == ini.Laplace:
        maxInstr += 'result:newIlt(' + python2maxima(laplaceRational) + ',s,t)$\n'
        result = maxEval(maxInstr)
        try:
            result = sp.sympify(result) 
        except:
            print("Error: could not evaluate the Inverse Laplace Transform")
    elif len(varList) > 1 and ini.Laplace in varList:
        maxInstr += 'result:ilt(' + python2maxima(laplaceRational) + ',s,t)$\n'
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
    maxInstr, result = makeMaxInstr(instr, result, save=False)                  # Create the maxima instruction
    maxResult = maxEval(maxInstr, numeric=instr.numeric)                                            # Execute the maxima instruction results
    result = parseMaxResult(result, instr.circuit.indepVars, maxResult)        # Convert maxima results into SLiCAP results     
    return result

def doMaxFunction(funcName, args):
    maxInstr = "assume_pos:true$assume_pos_pred:symbolp$ratprint:false$"
    maxInstr += "result:"
    maxInstr += MAXFUNCTIONS[funcName]
    maxInstr += funcName +'('
    for arg in args:
        maxInstr += str(arg) + ','
    maxInstr = maxInstr[:-1] + ')$'
    result = maxEval(maxInstr)
    return sp.sympify(result)

def makeMaxInstr(instr, result, save=False):
    maxInstr = "assume_pos:true$assume_pos_pred:symbolp$ratprint:false$"
    if instr.dataType == 'numer':
        result.M, result.Iv, result.Dv = makeMaxMatrices(instr) 
        detP, detN, srcP, srcN = makeMaxSrcDetPos(instr)  
        maxInstr += MAXFUNCTIONS['doDet'] 
        maxInstr += MAXFUNCTIONS['doNumer']  
        maxInstr += 'M : ' + python2maxima(result.M) + '$\n'
        maxInstr += 'detCols: [' + str(detP) + ',' + str(detN) + ']$\n'
        maxInstr += 'srcRows: [' + str(srcP) + ',' + str(srcN) + ']$\n'
        maxInstr += 'result: doNumer(M,srcRows,detCols)$'
    elif instr.dataType == 'denom': 
        result.M, result.Iv, result.Dv = makeMaxMatrices(instr) 
        maxInstr += MAXFUNCTIONS['doDet'] 
        maxInstr += 'M:' + python2maxima(result.M) + '$\n'
        maxInstr += 'result: doDet(M)$'
    elif instr.dataType == 'laplace':
        result.M, result.Iv, result.Dv = makeMaxMatrices(instr) 
        detP, detN, srcP, srcN = makeMaxSrcDetPos(instr) 
        maxInstr += MAXFUNCTIONS['doDet'] 
        maxInstr += MAXFUNCTIONS['doLaplace']  
        maxInstr += 'M : ' + python2maxima(result.M) + '$\n'
        maxInstr += 'detCols: [' + str(detP) + ',' + str(detN) + ']$\n'
        maxInstr += 'srcRows: [' + str(srcP) + ',' + str(srcN) + ']$\n'
        maxInstr += MAXFUNCTIONS['doNumer']
        if instr.gainType == 'vi':
            maxInstr += 'Iv: ' + python2maxima(result.Iv.transpose()) + '$\n'
        maxInstr += 'result:doLaplace(M,srcRows,detCols,Iv,"' + str(instr.gainType) + '")$'
    elif instr.dataType == 'dc':
        result.M, result.Iv, result.Dv = makeMaxMatrices(instr) 
        detP, detN, srcP, srcN = makeMaxSrcDetPos(instr) 
        maxInstr += MAXFUNCTIONS['doDet'] 
        maxInstr += MAXFUNCTIONS['doLaplace']  
        maxInstr += MAXFUNCTIONS['doNumer']
        maxInstr += 'M : ' + python2maxima(result.M.subs(ini.Laplace, 0)) + '$\n'
        maxInstr += 'Iv: ' + python2maxima(result.Iv.subs(ini.Laplace, 0).transpose()) + '$\n'
        maxInstr += 'detCols: [' + str(detP) + ',' + str(detN) + ']$\n'
        maxInstr += 'srcRows: [' + str(srcP) + ',' + str(srcN) + ']$\n'
        maxInstr += 'result: doLaplace(M,srcRows,detCols,Iv,"' + str(instr.gainType) + '")$'
    elif instr.dataType == 'noise':
        result.M, result.Iv, result.Dv = makeMaxMatrices(instr) 
        detP, detN, srcP, srcN = makeMaxSrcDetPos(instr) 
        maxInstr += MAXFUNCTIONS['doDet'] 
        maxInstr += MAXFUNCTIONS['doNumer']
        maxInstr += MAXFUNCTIONS['doLaplace']
        maxInstr += MAXFUNCTIONS['doNoise']   
        maxInstr += 'M : ' + python2maxima(result.M) + '$\n'
        maxInstr += 'detCols: [' + str(detP) + ',' + str(detN) + ']$\n'
        maxInstr += 'srcRows: [' + str(srcP) + ',' + str(srcN) + ']$\n'
        maxInstr += 'Iv: ' + python2maxima(result.Iv.transpose()) + '$\n'
        maxInstr += 'sources: ['
        for name in instr.circuit.indepVars:
            if 'noise' in list(instr.circuit.elements[name].params.keys()):
                value = instr.circuit.elements[name].params['noise']
                result.snoiseTerms[name] = value
                if instr.numeric == True:
                    value = fullSubs(value, instr.parDefs)
                maxInstr += name + '=' + str(value) + ','
        if maxInstr[-1] == ',':
            maxInstr = maxInstr[0:-1]
        maxInstr += ']$\n'
        maxInstr += 'result:doNoise(M,srcRows,detCols,Iv,sources)$'
    elif instr.dataType == 'dcvar':
        result.M, result.Iv, result.Dv = makeMaxMatrices(instr) 
        detP, detN, srcP, srcN = makeMaxSrcDetPos(instr) 
        maxInstr += MAXFUNCTIONS['doDet'] 
        maxInstr += MAXFUNCTIONS['doNumer']
        maxInstr += MAXFUNCTIONS['doLaplace']
        maxInstr += MAXFUNCTIONS['doDCvar']   
        maxInstr += 'M : ' + python2maxima(result.M) + '$\n'
        maxInstr += 'detCols: [' + str(detP) + ',' + str(detN) + ']$\n'
        maxInstr += 'srcRows: [' + str(srcP) + ',' + str(srcN) + ']$\n'
        maxInstr += 'Iv: ' + python2maxima(result.Iv.transpose()) + '$\n'
        maxInstr += 'sources: ['
        for name in instr.circuit.indepVars:
            if 'dcvar' in list(instr.circuit.elements[name].params.keys()):
                value = instr.circuit.elements[name].params['dcvar']
                result.svarTerms[name] = value
                if instr.numeric == True:
                    value = fullSubs(value, instr.parDefs)
                maxInstr += name + '=' + str(value) + ','
        if maxInstr[-1] == ',':
            maxInstr = maxInstr[0:-1]
        maxInstr += ']$\n'
        maxInstr += 'result:doDCvar(M,srcRows,detCols,Iv,sources)$'
    elif instr.dataType == 'solve':
        result.M, result.Iv, result.Dv = makeMaxMatrices(instr)        
        maxInstr += MAXFUNCTIONS['doDet'] 
        maxInstr += MAXFUNCTIONS['solve'] 
        maxInstr += 'M : ' + python2maxima(result.M) + '$\n'
        maxInstr += 'Iv: ' + python2maxima(result.Iv.transpose()) + '$\n'
        maxInstr += 'result: doSolve(M,Iv)$'
    elif instr.dataType == 'dcsolve':
        result.M, result.Iv, result.Dv = makeMaxMatrices(instr)        
        maxInstr += MAXFUNCTIONS['doDet'] 
        maxInstr += MAXFUNCTIONS['solve'] 
        maxInstr += 'M : ' + python2maxima(result.M) + '$\n'
        maxInstr += 'Iv: ' + python2maxima(result.Iv.transpose()) + '$\n'
        maxInstr += 'result: doSolveDC(M,Iv)$'
    elif instr.dataType == 'timesolve':
        result.M, result.Iv, result.Dv = makeMaxMatrices(instr) 
        maxInstr += MAXFUNCTIONS['doDet'] 
        maxInstr += MAXFUNCTIONS['solve'] 
        maxInstr += MAXFUNCTIONS['newIlt'] 
        maxInstr += 'M : ' + python2maxima(result.M) + '$\n'
        maxInstr += 'Iv: ' + python2maxima(result.Iv.transpose()) + '$\n'
        maxInstr += 'result: doSolveTime(M,Iv)$'
    elif instr.dataType == "poles":
        maxInstr += MAXFUNCTIONS['pz']
        maxInstr += 'expr: ' + python2maxima(result.denom) + '$\n'
        maxInstr += 'result:findRoots(expr)$'
    elif instr.dataType == "zeros":
        maxInstr += MAXFUNCTIONS['pz']
        maxInstr += 'expr: ' + python2maxima(result.numer) + '$\n'
        maxInstr += 'result:findRoots(expr)$'
    elif instr.dataType == "solve":
        result.M, result.Iv, result.Dv = makeMaxMatrices(instr) 
        maxInstr += MAXFUNCTIONS["solve"]
        maxInstr += 'instr@M :' + python2maxima(result.M) + '$\n'
        maxInstr += 'instr@Iv:' + python2maxima(result.Iv.transpose()) + '$\n'
        maxInstr += 'result:doSolve(M,Iv)$'
    elif instr.dataType == "dcsolve":
        result.M, result.Iv, result.Dv = makeMaxMatrices(instr) 
        maxInstr += MAXFUNCTIONS["solve"]
        maxInstr += 'instr@M :' + python2maxima(result.M) + '$\n'
        maxInstr += 'instr@Iv:' + python2maxima(result.Iv.transpose()) + '$\n'
        maxInstr += 'result:doSolveDC(M,Iv)$'
    elif instr.dataType != 'params':
        result.M, result.Iv, result.Dv = makeMaxMatrices(instr) 
        maxInstr += 'load("'+ini.installPath+'SLiCAPmaxima/SLiCAP.mac")$\n'
        detP, detN, srcP, srcN = makeMaxSrcDetPos(instr) 
        maxInstr += 'instr:new(instruction)$\n'
        maxInstr += 'instr@M :' + python2maxima(result.M) + '$\n'
        maxInstr += 'instr@Iv:' + python2maxima(result.Iv.transpose()) + '$\n'
        maxInstr += 'instr@Dv:' + python2maxima(result.Dv.transpose()) + '$\n'
        maxInstr += 'instr@gainType:"' + instr.gainType + '"$\n'
        maxInstr += 'instr@dataType:"' + instr.dataType + '"$\n'
        maxInstr += 'instr@lgRef:"' + instr.lgRef + '"$\n'
        if instr.numeric:
            maxInstr += 'instr@numeric:true$\n'
        else:
            maxInstr += 'instr@numeric:false$\n'
        maxInstr += 'instr@detCols:[' + str(detP) + ',' + str(detN) + ']$\n'
        maxInstr += 'instr@srcRows:[' + str(srcP) + ',' + str(srcN) + ']$\n'
        if instr.dataType =='noise' or instr.dataType == 'dcvar':
            maxInstr += 'instr@sources:['
            for name in instr.circuit.indepVars:
                if instr.dataType == 'noise':
                    value = instr.circuit.elements[name].params['noise']
                elif instr.dataType == 'dcvar':
                     value = instr.circuit.elements[name].params['dcvar']
                if instr.numeric == True:
                    value = fullSubs(value, instr.parDefs)
                maxInstr += name + '=' + str(value) + ','
            maxInstr = maxInstr[0:-1] + ']$\n' 
        maxInstr += 'result:execute(instr)$'
    return (maxInstr, result)

def makeMaxMatrices(instr):
    # Create the MNA matrix
    M, Dv = makeMatrices(instr)
    
    # Create vecor with independent variables: this requires source names and values for noise and dcvar analysis
    if instr.dataType == "noise" or instr.dataType == "dcvar":
        Iv = makeSrcVector(instr.circuit, instr.parDefs, 'all', value = 'id', numeric = instr.numeric)
    elif instr.dataType == "dc" or instr.dataType == "dcsolve":
        Iv = makeSrcVector(instr.circuit, instr.parDefs, 'all', value = 'dc', numeric = instr.numeric)
    elif instr.dataType != 'denom':
        Iv = makeSrcVector(instr.circuit, instr.parDefs, 'all', value = 'value', numeric = instr.numeric)
    else:
        Iv =sp.Matrix()
    if instr.numeric:
        M = sp.N(M)
        Dv = sp.N(Dv)
        Iv = sp.N(Iv)
    return M, Iv, Dv

def makeSubsDict(instr):
    # Create a substitution dictionary for this instruction that does not contain
    # step parameters 
    if instr.numeric and ini.stepFunction and instr.step:
        instr.parDefs = {}
        for key in list(instr.circuit.parDefs.keys()):
            if key not in list(instr.stepDict.keys()):
                instr.parDefs[key] = instr.circuit.parDefs[key]
    else:
        instr.parDefs = instr.circuit.parDefs
    return instr

def parseMaxResult(result, indepVars, maxResult):
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
                    term = sp.sympify(oTerms[j])
                    if term == False:
                        term = sp.N(0)
                except:
                    term = sp.N(0)
                ot += term
                result.onoiseTerms[indepVars[j]].append(term)
                try:
                    term = sp.sympify(iTerms[j])
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
                    term = sp.sympify(oTerms[j])
                    if term == False:
                        term = sp.N(0)
                except:
                    term = sp.N(0)
                ot += term
                result.ovarTerms[indepVars[j]].append(term)
                try:
                    term = sp.sympify(iTerms[j])
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
    Substitutes values for step parameters in function and returns a list
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

if __name__ == '__main__':
    from SLiCAP import initProject
    prj = initProject('testproject')
    #import noiseTest as nt
    import LRC
    print(LRC.result2.solve)