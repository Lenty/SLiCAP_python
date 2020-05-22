#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 23:14:38 2020

@author: anton
"""
from SLiCAPpythonMaxima import *

GAINTYPES = ['vi', 'gain', 'loopgain', 'servo', 'asymptotic', 'direct',]
DATATYPES = ['matrix', 'noise', 'solve', 'time', 'dcvar', 'dcsolve', 'numer',
             'denom', 'laplace', 'zeros', 'poles', 'pz', 'impulse', 'step']

class instruction(object):
    # prototype instruction
    def __init__(self):
        self.circuit    = False
        self.simType    = False
        self.gainType   = False
        self.dataType   = False
        self.step       = False
        self.stepVar    = False
        self.stepMethod = False
        self.stepStart  = False
        self.stepStop   = False
        self.stepNum    = 1
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
    def check(self):
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
                elif self.dataType == 'numer':
                    # need detector
                    self.checkDetector()
                elif self.dataType == 'denom':
                    # need nothing
                    pass
                elif self.dataType == 'noise':
                    # need detector
                    self.checkDetector()
                elif self.dataType == 'matrix':
                    # need nothing
                    pass
                elif self.dataType == 'solve':
                    # need nothing
                    pass
                elif self.dataType == 'time':
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
            # Check step parameters
            self.checkStep()
        return
    
    def checkNumeric(self):
        if self.simType != 'numeric':
            self.errors += 1
            print "Error: dataType '%s' not available for simType: '%s'."%(self.dataType, self.simType)
        return
    
    def checkSource(self):
        if self.source == False:
            self.errors += 1
            print "Error: missing source definition."
        elif self.source not in self.circuit.indepVars:
            self.errors += 1
            print "Error: unkown source: '%s'."%(self.source)
        return
    
    def checkLGref(self):
        if self.lgRef == False:
            self.errors += 1
            print "Error: missing loop gain reference definition."
        elif self.source not in self.circuit.controlled:
            self.errors += 1
            print "Error: unkown loop gain reference: '%s'."%(self.lgRef)
        return
    
    def checkDetector(self):
        if self.detector != False:
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
        # if lin:
          # Check stepVar
          # Check stepNum
          # Check stepStart
          # Check stepStop
          # Generate stepList
        # if log:
          # Check stepVar
          # Check stepNum
          # Check stepStart
          # Check stepStop
          # Check step including zero
            # stepStart * stepStop should be positive
          # Generate stepList
        # if list:
          # Check stepVar
          # Check stepList
            # numeric
        # if array:
          # Check stepVars
          # Check stepArray:
            # dimension
            # numeric
        return
    
    def execute(self):
        self.check()
        if self.errors != 0:
            print "Errors found. Instruction will not be executed."
            return
        return

if __name__ == '__main__':
    i = instruction()
    i.circuit = circuit()
    i.gainType = 'loopgain'
    i.dataType = 'zeros'
    i.simType = 'numeric'
    i.detector = 'V_11'
    i.source = 'V1'
    i.lgRef = 'G1'
    i.execute()