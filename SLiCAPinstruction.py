#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 23:14:38 2020

@author: anton
"""
from SLiCAPexecute import *

GAINTYPES = ['vi', 'gain', 'loopgain', 'servo', 'asymptotic', 'direct',]
DATATYPES = ['matrix', 'noise', 'solve', 'time', 'dcvar', 'dcsolve', 'numer',
             'denom', 'laplace', 'zeros', 'poles', 'pz', 'impulse', 'step']

class instruction(object):
    """
    Prototype Instruction object, with execute and check methods.
    """
    def __init__(self):
        self.circuit    = False
        self.simType    = False
        self.gainType   = False
        self.dataType   = False
        self.step       = False
        self.stepVar    = False
        self.stepVars   = False
        self.stepMethod = False
        self.stepStart  = False
        self.stepStop   = False
        self.stepNum    = False
        self.stepList   = []
        self.stepArray  = []
        self.source     = False
        self.detector   = False
        self.lgRef      = False
        self.results    = False
        self.MNA_I      = False # Vector with independent variables, adjusted for instruction.gainType
        self.MNA_V      = False # Vector with dependent variables, adjusted for instruction.gainType
        self.MNA_M      = False # MNA matrix, adjusted for instruction.gainType
        self.G          = False # Conductance matrix (not implemented)
        self.C          = False # Capacitance matrix (not implemented)
        self.R          = False # Inverse of the conductance matrix (not implemented)
        self.TAU        = False # dot porduct of self.R and self.C
        self.errors     = 0
        self.results    = False
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
        if self.circuit == False:
            self.errors += 1
            print "Error: missing circuit definition."
        elif type(self.circuit) != type(circuit()):
            self.errors += 1
            print "Error: not SLiCAP a circuit object."
        if self.gainType == False:
            self.errors += 1
            print "Error: missing gainType specification."
        elif self.gainType.lower() not in GAINTYPES:
            self.errors += 1
            print "Error: unknown gainType: '%s'."%(self.gainType)
        else:
            self.gainType = self.gainType.lower()
        if self.dataType == False:
            self.errors += 1
            print "Error: missing dataType specification."
        elif self.dataType.lower() not in DATATYPES:
            self.errors += 1
            print "Error: unknown dataType: '%s'."%(self.dataType)
        else:
            self.dataType = self.dataType.lower()
        if self.simType == False:
            self.errors += 1
            print "Error: missing simType specification."
        elif self.simType.lower() != 'numeric' and self.simType != 'symbolic':
            self.errors += 1
            print "Error: unknown simType: '%s'."%(self.simType)
        else:
            self.simType = self.simType.lower()
        if self.errors == 0:
            if self.gainType == 'vi':
                if self.dataType == 'laplace':
                    # need detector
                    self.checkDetector()
                    result = functionResult()
                elif self.dataType == 'numer':
                    # need detector
                    self.checkDetector()
                    result = lfunctionResult()
                elif self.dataType == 'denom':
                    # need nothing
                    result = functionResult()
                elif self.dataType == 'noise':
                    # need detector
                    self.checkDetector()
                    result = noiseResult()
                elif self.dataType == 'matrix':
                    # need nothing
                    result = matrixResult()
                elif self.dataType == 'solve':
                    # need nothing
                    result = functionResult()
                elif self.dataType == 'time':
                    # need detector
                    self.checkDetector()
                    result = functionResult()
                elif self.dataType == 'dcvar':
                    # need detector
                    self.checkDetector()
                    result = dcVarResult()
                elif self.dataType == 'dcsolve':
                    # need nothing
                    result = functionResult()
                else:
                    self.errors += 1
                    print "Error: dataType '%s' not available for gainType: '%s'."%(self.dataType, self.gainType)
            else:
                if self.dataType == 'laplace':
                    # need source and detector
                    self.checkDetector()
                    self.checkSource()
                    result = functionResult()
                elif self.dataType == 'numer':
                    # need source and detector
                    self.checkDetector()
                    self.checkSource()
                    result = functionResult()
                elif self.dataType == 'denom':
                    # need nothing
                    pass
                elif self.dataType == 'impulse':
                    # need source and detector
                    self.checkDetector()
                    self.checkSource()
                    result = functionResult()
                elif self.dataType == 'step':
                    # need source and detector
                    self.checkDetector()
                    self.checkSource()
                    result = functionResult()
                elif self.dataType == 'poles':
                    # need numeric
                    self.checkNumeric()
                    result = pzResult()
                elif self.dataType == 'zeros':
                    # need numeric, source and detector
                    self.checkNumeric()
                    self.checkDetector()
                    self.checkSource()
                    result = pzResult()
                elif self.dataType == 'pz':
                    # need numeric source and detector
                    self.checkNumeric()
                    self.checkDetector()
                    self.checkSource()
                    result = pzResult()
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
            # Check step parameters
            self.checkStep()
        return
    
    def checkNumeric(self):
        if self.simType != 'numeric':
            self.errors += 1
            print "Error: dataType '%s' not available for simType: '%s'."%(self.dataType, self.simType)
        return
    
    def checkSource(self):
        if type(self.source) == bool:
            self.errors += 1
            print "Error: missing source definition."
        elif self.source not in self.circuit.indepVars:
            self.errors += 1
            print "Error: unkown source: '%s'."%(self.source)
        return
    
    def checkLGref(self):
        if type(self.lgRef) == bool:
            self.errors += 1
            print "Error: missing loop gain reference definition."
        elif self.source not in self.circuit.controlled:
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
        if type(self.detector) != bool:
            # detector has two nodes or two voltage sources
            if type(self.detector) == str:
                # Change the detector definition
                self.detector = [self.detector, False]
            detP = self.detector[0]
            detN = self.detector[1]
            # detectors must be of the same type
            if detP == False or detN == False:
                pass
            elif detP[0] != detN[0]:
                self.errors += 1
                print "Error: two detectors must be of the same type."
            if detP != False and detP not in self.circuit.depVars:
                self.errors += 1
                print "Error: unkown detector: '%s'."%(detP)
            if detN != False and detN not in self.circuit.depVars:
                self.errors += 1
                print "Error: unkown detector: '%s'."%(detN)
        else:
            self.errors += 1
            print "Error: missing detector definition."
        return
    
    def checkStep(self):
        # Check stepMethod
        if type(self.stepMethod) == bool:
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
        if type(self.stepVar) == bool:
            print "Error: missing step variable."
        else:
            if not isinstance(stepVar, tuple(sp.core.all_classes)):
                self.stepVar = sp.Symbol(self.stepVar)
            if self.stepVar not in self.circuit.parDefs.keys() and \
            self.stepVar not in self.circuit.params:
                print "Warning: unknown step parameter '%s'."%(self.stepVar)
        return
    
    def checkStepStart(self):
        """
        Assuming: False, float, int or str as input type.
        """
        if type(self.stepStart) == bool:
            self.errors += 1
            print "Error: missing stepStart value."
        else:
            value = checkNumber(self.stepStart)
            if type(value) == bool:
                self.errors += 1
                print "Error: cannot determine numeric value of stepStart."
            else:
                self.stepStart = value
        return
        
    def checkStepStop(self):
        """
        Assuming: False, float, int or str as input type.
        """
        if type(self.stepStop) == bool:
            self.errors += 1
            print "Error: missing stepStop value."
        else:
            value = checkNumber(self.stepStop)
            if type(value) == bool:
                self.errors += 1
                print "Error: cannot determine numeric value of stepStop."
            else:
                self.stepStop = value
        return
    
    def checkStepNum(self):
        """
        Assuming: False, float, int or str as input type.
        """
        if type(self.stepNum) == bool:
            self.errors += 1
            print "Error: missing stepNum value."
        else:
            value = checkNumber(self.stepNum)
            if type(value) == bool:
                self.errors += 1
                print "Error: cannot determine numeric value of stepSNum."
            else:
                self.stepNumt = value
        return
    
    def checkStepVars(self):
        if type(self.stepVars) == bool:
            self.errors += 1
            print "Error: missing list stepVars."
        elif type(self.stepVars) == list:
            if len(self.stepVars) == 0:
                self.errors += 1
                print "Error: empty stepVars."
            for stepVar in self.stepVars:
                self.checkStepVar(stepVar)
        else:
            self.errors += 1
            print "Error: expected a list type for 'stepVar'."
        return
    
    def checkStepList(self):
        if type(self.stepList) == bool:
            self.errors += 1
            print "Error: missing stepList."
        elif type(self.stepList) == list:
            if len(self.stepList) == 0:
                self.errors += 1
                print "Error: empty stepList."
            for i in range(len(self.stepList)):
                value = checkNumber(stepVal)
                if type(value) == bool:
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
        number of step variables. All lists should have equal lengths.
        """
        if type(self.stepArray) == bool:
            self.errors += 1
            print "Error: missing stepArray."
        elif type(self.stepArray) == list:
            numVars = len(self.stepArray)
            if numVars != len(self.stepVars):
                self.errors += 1
                print "Error: mismatch between dimensions of stepArray and stepVars."
            else:
                numsteps = len(stepArray[0])
                for i in range(len(stepArray)):
                    if len(stepArray[i]) != numSteps:
                        self.errors += 1
                        print "Error: unequal number of steps for step variables."
                        if self.errors == 0:
                            for j in range(len(stepArray[i])):
                                value = checkNumber(stepArray[i][j])
                                if type(value) == bool:
                                    self.errors += 1
                                    print "Error: cannot determine numeric value of stepArray[%s, %s]."%(i, j)
                                else:
                                    stepList[i][j] = value   
        return
    
    def execute(self):
        self.check()
        if self.errors != 0:
            print "Errors found. Instruction will not be executed."
            return
        else:
            doInstruction(self)
        return
    
    def delPar(self, parName):
        # single params and multiple.
        self.circuit.delPar(parName)
        return
        
    def defPar(self, parName):
        # single params and multiple.
        self.circuit.defPar(parName)
        return
        
    def getParValue(self, parName):
        # single params and multiple.
        self.circuit.getParValue(parName)
        return
    
    def indepVars(self):
        print self.circuit.indepVars
        return
    
    def depVars(self):
        print self.circuit.depVars
        return
    
    def controlled(self):
        print self.circuit.controlled
        return
    
    def stepParams(self):
        return
    
#### Return structures depend on data type
        
class functionResult(object):
    """
    Return structure for dataType 'solve', 'Laplace', 'impulse', 'step',
    'time'.
    """
    def __init__(self):
        self.results     = False # Solution vector
        
class matrixResult(object):
    """
    Return structure for dataType 'matrix'
    """
    def __init__(self):
        self.Iv          = False # Vector with independent variables
        self.M           = False # MNA matrix
        self.Dv          = False # Vector with dependent variables
        
class noiseResult(object):
    """
    Return structure for dataType 'noise'
    """
    def __init__(self):
        self.sources     = False # Names of the noise sources
        self.srcTerms    = False # Dict with respective noise spectra
        self.inoiseTerms = False # Dict with respective spectral contributions
                                 # to source-referred noise
        self.onoiseTerms = False # Dict with espective spectral contributions
                                 # to detector-referred noise
        self.inoise      = False # Total source-referred noise spectral density
        self.onoise      = False # Total detector-referred noise spectral 
                                 # density
        
class dcVarResult(object):
    """
    Return structure for dataType 'dcVar'
    """
    def __init__(self):
        self.sources     = False # Names of the sources with dc variance
        self.srcTerms    = False # Dict with respective variance
        self.ivarTerms   = False # Dict with respective contributions to 
                                 # source-referred variance
        self.ovarTerms   = False # Dict with respective contributions to 
                                 # detector-referred variance
        self.ivar        = False # Total source-referred variance
        self.ovar        = False # Total detector-referred variance
        self.dcSolve     = False # DC solution of the network

class pzResult(object):
    """
    Return structure for pole-zero analysis.
    """
    def __init__(self):
        self.DCvalue     = False # Zero-frequency value in case of 
                                 # dataType 'pz'
        self.poles       = False # Complex frequencies in [rad/s] or [Hz]
        self.zeros       = False # Complex frequencies in [rad/s] or [Hz]
        
DATATYPES = ['matrix', 'noise', 'solve', 'time', 'dcvar', 'dcsolve', 'numer',
             'denom', 'laplace', 'zeros', 'poles', 'pz', 'impulse', 'step']

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
    i.execute()