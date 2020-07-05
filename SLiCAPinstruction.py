#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 23:14:38 2020

@author: anton
"""
from SLiCAPexecute import *

GAINTYPES = ['vi', 'gain', 'loopgain', 'servo', 'asymptotic', 'direct',]
DATATYPES = ['matrix', 'noise', 'solve', 'time', 'dc', 'dcvar', 'dcsolve', 
             'numer', 'denom', 'laplace', 'zeros', 'poles', 'pz', 'impulse', 
             'step']

class instruction(object):
    """
    Prototype Instruction object, with execute and check methods.
    """
    def __init__(self):
        self.circuit    = None
        self.simType    = None
        self.gainType   = None
        self.dataType   = None
        self.step       = None
        self.stepVar    = None
        self.stepVars   = None
        self.stepMethod = None
        self.stepStart  = None
        self.stepStop   = None
        self.stepNum    = None
        self.stepList   = []
        self.stepArray  = []
        self.source     = None
        self.detector   = None
        self.lgRef      = None
        self.parDefs    = None
        self.numeric    = None
        self.results    = None
        self.Iv         = None # Vector with independent variables, adjusted for instruction.gainType
        self.M          = None # MNA matrix, adjusted for instruction.gainType
        self.Dv         = None # Vector with dependent variables, adjusted for instruction.gainType
        self.G          = None # Conductance matrix (not implemented)
        self.C          = None # Capacitance matrix (not implemented)
        self.R          = None # Inverse of the conductance matrix (not implemented)
        self.TAU        = None # dot porduct of self.R and self.C
        self.errors     = 0
        self.results    = allResults()
        self.detUnits   = None
        self.srcUnits   = None
        
    def checkCircuit(self, fileName):
        """
        Checks the circuit and makes it the (local) ciruit object for this
        instruction.
        """
        self.circuit = checkCircuit(fileName)
        
    def check(self):
        """
        Check the completeness and consistancy of the instruction data before
        it can be executed.
        """
        self.errors = 0
        if self.circuit == None:
            self.errors += 1
            print "Error: missing circuit definition."
        elif type(self.circuit) != type(circuit()):
            self.errors += 1
            print "Error: not SLiCAP a circuit object."
        if self.gainType == None:
            self.errors += 1
            print "Error: missing gainType specification."
        elif self.gainType.lower() not in GAINTYPES:
            self.errors += 1
            print "Error: unknown gainType: '%s'."%(self.gainType)
        else:
            self.gainType = self.gainType.lower()
        if self.dataType == None:
            self.errors += 1
            print "Error: missing dataType specification."
        elif self.dataType.lower() not in DATATYPES:
            self.errors += 1
            print "Error: unknown dataType: '%s'."%(self.dataType)
        else:
            self.dataType = self.dataType.lower()
        if self.simType == None:
            self.errors += 1
            print "Error: missing simType specification."
        elif self.simType.lower() != 'numeric' and self.simType != 'symbolic':
            self.errors += 1
            print "Error: unknown simType: '%s'."%(self.simType)
        else:
            self.simType = self.simType.lower()
            if self.simType == 'numeric':
                self.numeric = True
            elif self.simType == 'symbolic':
                self.numeric = False
        if self.errors == 0:
            if self.gainType == 'vi':
                if self.dataType == 'laplace':
                    # need detector
                    self.checkDetector()
                elif self.dataType == 'noise':
                    # need detector
                    self.checkDetector()
                    # only needs a sourrce for input noise analysis
                    self.checkSource(need = False)
                elif self.dataType == 'matrix':
                    # need nothing
                    pass
                elif self.dataType == 'solve':
                    # need nothing
                    pass
                elif self.dataType == 'time':
                    # need detector
                    self.checkDetector()
                elif self.dataType == 'dc':
                    # need detector
                    self.checkDetector()
                elif self.dataType == 'dcvar':
                    # need detector
                    self.checkDetector()
                elif self.dataType == 'dcsolve':
                    # need nothing
                    pass
                else:
                    self.errors += 1
                    print "Error: dataType '%s' not available for gainType: '%s'."%(self.dataType, self.gainType)
            else:
                if self.dataType == 'laplace':
                    # need source and detector
                    self.checkDetector()
                    self.checkSource()
                elif self.dataType == 'numer':
                    # need source and detector
                    self.checkDetector()
                    self.checkSource()
                elif self.dataType == 'denom':
                    # need nothing
                    pass
                elif self.dataType == 'impulse':
                    # need source and detector
                    self.checkDetector()
                    self.checkSource()
                elif self.dataType == 'step':
                    # need source and detector
                    self.checkDetector()
                    self.checkSource()
                elif self.dataType == 'poles':
                    # need numeric
                    self.checkNumeric()
                elif self.dataType == 'zeros':
                    # need numeric, source and detector
                    self.checkNumeric()
                    self.checkDetector()
                    self.checkSource()
                elif self.dataType == 'pz':
                    # need numeric source and detector
                    self.checkNumeric()
                    self.checkDetector()
                    self.checkSource()
                else:
                    self.errors += 1
                    print "Error: dataType '%s' not available for gainType: '%s'."%(self.dataType, self.gainType)
                if self.gainType == 'asymptotic':
                    # need loop gain reference
                    self.checkLGref()
                elif self.gainType == 'direct':
                    # need loop gain reference
                    self.checkLGref()
                elif self.gainType == 'loopgain':
                    # need loop gain reference
                    self.checkLGref()
                elif self.gainType == 'servo':
                    # need loop gain reference
                    self.checkLGref()
                else:
                    pass
        if self.step == True:
            if not self.numeric:
                self.errors += 1
                print "Error: symbolic stepping has not been implemented, use substitution instead."
            elif self.dataType == 'matrix':
                self.errors += 1
                print "Error: parameter stepping with dataType 'matrix' has not been implemented."
            else:
                # Check step parameters
                self.checkStep()
        return
    
    def checkNumeric(self):
        if not self.numeric:
            self.errors += 1
            print "Error: dataType '%s' not available for simType: '%s'."%(self.dataType, self.simType)
        return
    
    def checkSource(self, need = True):
        if type(self.source) == bool:
            if need:
                self.errors += 1
                print "Error: missing source definition."
        elif self.source not in self.circuit.indepVars:
            self.errors += 1
            print "Error: unkown source: '%s'."%(self.source)
        else:
            self.srcUnits = self.source[0].upper()
            if self.srcUnits == 'I':
                self.srcUnits = 'A'
        return
    
    def checkLGref(self):
        if type(self.lgRef) == bool:
            self.errors += 1
            print "Error: missing loop gain reference definition."
        elif self.lgRef not in self.circuit.controlled:
            self.errors += 1
            print "Error: unkown loop gain reference: '%s'."%(self.lgRef)
        return
    
    def checkDetector(self):
        """
        The tyoe of self.detector can be:
            bool: no detector has been defined
            str:  a single detector, nodal voltage or branch current
            list: either two nodat voltages or two branch currents
        """
        if self.detector != None:
            # detector has two nodes or two voltage sources
            if type(self.detector) == str:
                # Change the detector definition
                self.detector = [self.detector, None]
            detP = self.detector[0]
            detN = self.detector[1]
            # detectors must be of the same type
            if detP == None or detN == None:
                pass
            elif detP[0] != detN[0]:
                self.errors += 1
                print "Error: two detectors must be of the same type."
            if detP != None and detP not in self.circuit.depVars:
                self.errors += 1
                print "Error: unkown detector: '%s'."%(detP)
            if detN != None and detN not in self.circuit.depVars:
                self.errors += 1
                print "Error: unkown detector: '%s'."%(detN)
            if self.lgRef != None:
                # Impossible to calculate the asymptotic gain with these values
                forbidden = 'I_i_' + self.lgRef
                if detP == forbidden or detN == forbidden:
                    self.errors += 1
                    print "Error: forbidden combination of lgRef and detector."
            # Node zero does not exist in the matrix. It is the reference node.
            if detP == 'V_0':
                self.detector[0] = None
            if detN == 'V_0':
                self.detector[1] = None   
            if self.detector[0] != None:
                self.detUnits = detP[0].upper()
            elif self.detector[1] != None:
                self.detUnits = detN[0].upper()
            if self.detUnits == 'I':
                self.detUnits = 'A'
        else:
            self.errors += 1
            print "Error: missing detector definition."
        return
    
    def checkStep(self):
        # Check stepMethod
        if self.stepMethod == None:
            self.errors += 1
            print "Error: missing stepMethod."
        else:
            self.stepMethod = self.stepMethod.lower()
            if self.stepMethod == 'lin':
                self.checkStepVar()
                self.checkStepNum()
                self.checkStepStart()
                self.checkStepStop()
                if self.errors == 0:
                    self.stepList = np.linspace(self.stepStart, self.stepStop, self.stepNum)
            elif self.stepMethod == 'log':
                self.checkStepVar()
                self.checkStepNum()
                self.checkStepStart()
                self.checkStepStop()
                if self.errors == 0 and self.stepStart * self.stepStop > 0:
                    self.stepList = np.geomspace(self.stepStart, self.stepStop, self.stepNum)
                else:
                    self.errors += 1
                    print "Error: logarithmic stepping cannot include zero."
            elif self.stepMethod == 'list':
                self.checkStepVar()
                self.checkStepList()
            elif self.stepMethod == 'array':
                self.checkStepVars()
                if self.errors == 0:
                    self.checkStepArray()
            else:
                self.errors += 1
                print "Error: unknown stepMethod: '%s'."%(self.stepMethod)
        return
    
    def checkStepVar(self):
        if self.stepVar == None:
            print "Error: missing step variable."
        else:
            self.stepVar = sp.Symbol(str(self.stepVar))
            if self.stepVar not in self.circuit.parDefs.keys() and \
            self.stepVar not in self.circuit.params:
                print "Warning: unknown step parameter '%s'."%(self.stepVar)
        return
    
    def checkStepStart(self):
        """
        Assuming: None, float, int or str as input type.
        """
        if self.stepStart == None:
            self.errors += 1
            print "Error: missing stepStart value."
        else:
            value = checkNumber(self.stepStart)
            if value == None:
                self.errors += 1
                print "Error: cannot determine numeric value of stepStart."
            else:
                self.stepStart = value
        return
        
    def checkStepStop(self):
        """
        Assuming: None, float, int or str as input type.
        """
        if self.stepStop == None:
            self.errors += 1
            print "Error: missing stepStop value."
        else:
            value = checkNumber(self.stepStop)
            if value == None:
                self.errors += 1
                print "Error: cannot determine numeric value of stepStop."
            else:
                self.stepStop = value
        return
    
    def checkStepNum(self):
        """
        Assuming: None, float, int or str as input type.
        """
        if self.stepNum == None:
            self.errors += 1
            print "Error: missing stepNum value."
        else:
            value = checkNumber(self.stepNum)
            if value == None:
                self.errors += 1
                print "Error: cannot determine numeric value of stepSNum."
            elif value < 1:
                print "Warning: number of steps = 0."
                self.stepNum = int(value)
            else:
                self.stepNum = int(value)
        return
    
    def checkStepVars(self):
        if self.stepVars == None:
            self.errors += 1
            print "Error: missing list stepVars."
        elif type(self.stepVars) == list:
            if len(self.stepVars) == 0:
                self.errors += 1
                print "Error: empty stepVars."
            for i in range(len(self.stepVars)):     
                if not isinstance(self.stepVars[i], tuple(sp.core.all_classes)):
                    self.stepVars[i] = sp.Symbol(self.stepVars[i])
                if self.stepVars[i] not in self.circuit.parDefs.keys() and \
                self.stepVars[i] not in self.circuit.params:
                    print "Warning: unknown step parameter '%s'."%(self.stepVars[i])
        else:
            self.errors += 1
            print "Error: expected a list type for 'stepVar'."
        return
    
    def checkStepList(self):
        if self.stepList == None:
            self.errors += 1
            print "Error: missing stepList."
        elif type(self.stepList) == list:
            if len(self.stepList) == 0:
                self.errors += 1
                print "Error: empty stepList."
            for i in range(len(self.stepList)):
                value = checkNumber(stepVal)
                if value == None:
                    self.errors += 1
                    print "Error: cannot determine numeric value of stepList[%s]."%(i)
                else:
                    stepList[i] = value              
        else:
            self.errors += 1
            print "Error: expected a list type for 'stepValues'."
        return
        
    def checkStepArray(self):
        """
        The step array is a list of lists. The number of lists must equal the
        number of step variables. Each entry in a list is a step value of the
        associated step variable. All lists should have equal lengths.
        """
        if self.stepArray == None:
            self.errors += 1
            print "Error: missing stepArray."
        elif type(self.stepArray) == list:
            numVars = len(self.stepArray)
            if numVars != len(self.stepVars):
                self.errors += 1
                print "Error: mismatch between dimensions of stepArray and stepVars."
            else:
                numSteps = len(self.stepArray[0])
                for i in range(numVars):
                    if len(self.stepArray[i]) != numSteps:
                        self.errors += 1
                        print "Error: unequal number of steps for step variables."
                    if self.errors == 0:
                        for j in range(numSteps):
                            value = checkNumber(self.stepArray[i][j])
                            if value == None:
                                self.errors += 1
                                print "Error: cannot determine numeric value of stepArray[%s, %s]."%(i, j)
                            else:
                                self.stepArray[i][j] = value   
        return
    
    def stepParams(self, param):
        """
        Returns a dictionary with:
            key:    parameter name
            value:  list with parameter values after recursive substitution of
                    all parameters for the stepped values of the step variable.
        """
        self.checkStep()
        if self.errors != 0:
            print "Errors found 'stepParams()' cannot be executed."
            return {}
        substDict = {}
        if self.stepMethod == 'array':
            print 'Error: "stepParams" not implemented for stepMethod "array".'
            return parvalues
        for key in self.circuit.parDefs.keys():
            if key != self.stepVar:
                substDict[key] = self.circuit.parDefs[key]
        if sp.Symbol(param) not in self.circuit.parDefs.keys():
            print "Error: unkonwn parameter '%s'."%(param)
        else:
            try:
                func = fullSubs(self.circuit.parDefs[sp.Symbol(param)], substDict)
                func = sp.lambdify(self.stepVar, func)
                parValues = [func(self.stepList[i]) for i in range(len(self.stepList))]
            except:
                print 'Error: could not create function for "%s(%s)".'%(str(param), str(self.stepVar))
                parValues = []
        return parValues
    
    def execute(self):
        self.check()
        if self.errors != 0:
            print "Errors found. Instruction will not be executed."
            return(allResults())
        else: 
            # Create an instance of allResults() and copy instruction data.
            # This keeps the correct instruction information with the result
            # in cases that the instruction is modified at a later stage.
            r = allResults()
            r.simType        = self.simType
            r.gainType       = self.gainType
            r.dataType       = self.dataType
            r.step           = self.step
            r.stepVar        = self.stepVar
            r.stepVars       = self.stepVars
            r.stepMethod     = self.stepMethod
            r.stepStart      = self.stepStart
            r.stepStop       = self.stepStop
            r.stepNum        = self.stepNum
            r.stepList       = self.stepList
            r.stepArray      = self.stepArray
            r.source         = self.source
            r.detector       = self.detector
            r.lgRef          = self.lgRef
            r.circuit        = self.circuit
            r.parDefs        = self.parDefs
            r.errors         = self.errors
            r.detUnits       = self.detUnits
            r.srcUnits       = self.srcUnits
            r.numeric        = self.numeric
            return doInstruction(r)
    
    def delPar(self, parName):
        # delete a parameter definition
        self.circuit.delPar(parName)
        return
        
    def defPar(self, parName, parValue):
        # define a parameter
        self.circuit.defPar(str(parName), parValue)
        return
    
    def defPars(self, parDict):
        # define multiple parameters.
        self.circuit.defPars(parDict)
        return
    
    def getParValue(self, parName):
        # single params and multiple.
        if self.simType == 'numeric':
            numeric = True
        else:
            numeric = False
        return self.circuit.getParValue(parName, numeric)
    
    def indepVars(self):
        print self.circuit.indepVars
        return
    
    def depVars(self):
        print self.circuit.depVars
        return
    
    def controlled(self):
        print self.circuit.controlled
        return
    
    def stepParams(self, paramPlot):
        parNames = self.circuit.parDefs.keys() + self.circuit.params
        errors = 0
        yValues = {}
        # check the input
        if paramPlot.xVar == None:
             print "Error: missing x variable."
             errors +=1
        elif sp.Symbol(paramPlot.xVar) not in parNames:
            print "Error: unknown parameter: '%s'."%(paramPlot.xVar)
            errors += 1
        if paramPlot.yVar == None:
             print "Error: missing y variable."
             errors +=1
        elif sp.Symbol(paramPlot.yVar) not in parNames:
            print "Error: unknown parameter: '%s'."%(paramPlot.yVar)
            errors += 1
        elif paramPlot.pVar == None and sp.Symbol(paramPlot.pVar) not in parNames:
            print "Error: unknown parameter: '%s'."%(paramPlot.pVar)
            errors += 1
        scaleFactors = SCALEFACTORS.keys()
        if paramPlot.xScale != None and paramPlot.xScale not in scaleFactors:
            print "Error: unknown scale factor '%s'."%(paramPlot.xScale)
            errors += 1
        if paramPlot.yScale != None and paramPlot.yScale not in scaleFactors:
            print "Error: unknown scale factor '%s'."%(paramPlot.yScale)
            errors += 1
        if paramPlot.pScale != None and paramPlot.pScale not in scaleFactors:
            print "Error: unknown scale factor '%s'."%(paramPlot.pScale)
            errors += 1
        if paramPlot.xNum == None:
            print "Error: missing number of points for x variable."
            errors += 1
        else:
            xNum = checkNumber(paramPlot.xNum)
            if xNum == None:
                print "Error: '%s' is not a number."%(paramPlot.xNum)
                errors += 1
        if paramPlot.xStart == None:
            print "Error: missing start value for x variable."
            errors += 1
        else:
            xStart = checkNumber(paramPlot.xStart)
            if xStart == None:
                print "Error: '%s' is not a number."%(paramPlot.xStart)
                errors += 1
        if paramPlot.xStop == None:
            print "Error: missing stop value for x variable."
            errors += 1
        else:
            xStop = checkNumber(paramPlot.xStop)
            if paramPlot.xStop == None:
                print "Error: '%s' is not a number."%(paramPlot.xStop)
                errors += 1
        if paramPlot.pVar != None:
            if paramPlot.pNum == None:
                print "Error: missing number of points for p variable."
                errors += 1
            else:
                pNum = checkNumber(paramPlot.pNum)
                if pNum == None:
                    print "Error: '%s' is not a number."%(paramPlot.pNum)
                    errors += 1
            if paramPlot.pStart == None:
                print "Error: missing start value of p variable."
                errors += 1
            else:
                pStart = checkNumber(paramPlot.pStart)
                if pStart == None:
                    print "Error: '%s' is not a number."%(paramPlot.pStart)
                    errors += 1
            if paramPlot.pStop == None:
                print "Error: missing stop value of p variable."
                errors += 1
            else:
                pStop = checkNumber(paramPlot.pStop)
                if pStop == None:
                    print "Error: '%s' is not a number."%(paramPlot.pStop)
                    errors += 1
        if errors == 0:
            if paramPlot.xMethod.lower() == 'lin':
                x = np.linspace(xStart, xStop, num = xNum)
            elif paramPlot.xMethod.lower() == 'log':
                x = np.geomspace(xStart, xStop, num = xNum)
            else:
                print "Error: unknown method '%s'."%(paramPlot.xMethod)
                errors +=1
        if errors == 0 and paramPlot.pVar != None:
            if paramPlot.pMethod.lower() == 'lin':
                p = np.linspace(pStart, pStop, num = pNum)
            elif paramPlot.xMethod.lower() == 'log':
                p = np.geomspace(pStart, pStop, num = pNum)
            else:
                print "Error: unknown method '%s'."%(paramPlot.pMethod)
                errors +=1
        if errors == 0:
            substitutions = {}
            for parName in self.circuit.parDefs.keys():
                if parName != sp.Symbol(paramPlot.xVar) and paramPlot.pVar != None and parName != sp.Symbol(paramPlot.pVar):
                    substitutions[parName] = self.circuit.parDefs[parName]
            f = fullSubs(self.circuit.parDefs[sp.Symbol(paramPlot.yVar)], substitutions)
            if paramPlot.pVar != None:
                for parValue in p:
                    fu = f.subs(sp.Symbol(paramPlot.pVar), parValue)
                    func = sp.lambdify(sp.Symbol(paramPlot.xVar), fu)
                    yValues[parValue] = [func(x[i]) for i in range(len(x))]
            else:
                func = sp.lambdify(sp.Symbol(paramPlot.xVar), f)
                yValues = [func(x[i] for i in range(len(x)))]
            paramPlot.yValues = yValues
            paramPlot.xValues = x
        return paramPlot

class paramPlot(object):
    """
    """
    def __init__(self):
        xVar    = None
        yVar    = None
        pVar    = None
        xStart  = None
        xStop   = None
        xNum    = None
        xMethod = 'lin'
        pStart  = None
        pStop   = None
        pNum    = None
        pMethod = 'lin'
        xScale  = None
        yScale  = None
        pScale  = None
        xUnits  = ''
        yUnits  = ''
        pUnits  = ''
        xValues = None
        yValues = None
        
if __name__ == '__main__':
    i = instruction()
    i.circuit = circuit()
    i.gainType = 'loopgain'
    i.dataType = 'zeros'
    i.simType = 'numeric'
    i.detector = 'V_11'
    i.source = 'V1'
    i.lgRef = 'G1'
    i.step = True
    i.stepMethod = 'lin'
    i.stepNum = '5a'
    i.execute()