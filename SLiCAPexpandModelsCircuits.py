#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 22:02:14 2020

@author: anton
"""
from SLiCAPexpansionModels import EXPANSIONMODELS
from SLiCAPprotos import *

def expandModelsCircuits(circuitObject):
    """
    - For each element of which the element type differs from 'X', check
      if the model parameters can be obtained from the element definition. 
      If not try to find them from:
      - local model definitions in the circuitObject.modelDefs attribute
      - model definitions from precompiled user libraries
      - model definitions from built-in models
    
    - For each element with an expansion model try to find the required 
      child circuit definition for its model in:
      - The circuitObject.circuits dictionary
      - The dictionary LIBRARYMODELS with circuits from the the pre-compiled 
        user libraries
      - The dictionary: EXPANSIONMODELS, with precompiled built-in circuits
    - Create a working copy 'childCircuit' from this prototype.
    - For all elements of this childCircuit:
      - Update the refDes attributes by adding a suffix: 
        _< parent element refDes >
      - Update the values of the model parameters in the .params dict:
        - substitute parameters that need to be passed from the parent element
          in the corresponsing value of the child parameter
        - parameters used in the child element that were not defined by the 
          parent will be renamed by adding the suffix:
        _< parent element refDes >
    - For all .parDefs fields of the child circuit:
      - Substitute the values of the parameters that should be passed to the 
        child in all the expressions of the value fields in the .parDefs
        dictionary and keep their name in the keys 
      - For all other (local)parameters add the suffix:
        _< parent element refDes > to their name (key) and substitute them in
        all value value fields with: 
        sympy.Symbol(< parameter name >_< parent element refDes >)
    - Add all elements from the childCircuit to circuitObject
    - Add all entries from the .parDefs dict of the childCircuit to
      circuitObject.
    """
    return CircuitObject

def updateCirData(mainCircuit):
    """
    - Updates the lists with dependent variables (detectors), sources 
      (independent variables) and controlled sources (possible loop gain 
      references). 
    - If global parameters are used in the circuit, their definition is added
      to the '.parDefs' attribute of the circuit.
    - Checks if the global ground node '0' is used in the circuit.
    - Checks if the circuit has at least two nodes.
    - Checks if the referenced elements exist.
    """
    return mainCircuit

if __name__ == '__main__':
    pass