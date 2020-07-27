#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Module with definition of the SLiCAP instruction class. 

This module is imported by SLiCAP.py
"""
from SLiCAPexecute import *

GAINTYPES = ['vi', 'gain', 'loopgain', 'servo', 'asymptotic', 'direct',]
DATATYPES = ['matrix', 'noise', 'solve', 'time', 'dc', 'dcvar', 'dcsolve', 
             'numer', 'denom', 'laplace', 'zeros', 'poles', 'pz', 'impulse', 
             'step', 'param']

class instruction(object):
    """
    Prototype Instruction object.
    """ 
    def __init__(self):

        self.simType = 'numeric'
        """
        Defines the simulation gain type.
        
        See **instruction.setSimType(<simType>)** for specification of *instruction.simType*.
        """

        self.gainType = None       
        """
        Defines the simulation gain type.
        
        See **instruction.setGainType(<gainType>)** for specification of *instruction.gainType*.
        """
        
        self.dataType = None
        """
        Defines the simulation data type.
        
        See **instruction.setDataType(<dataType>)** for specification of *instruction.dataType*.
        """
        
        self.sweepVar = None
        """
        Defines the sweep variable for parameter sweeping.
        
        See **instruction.setSweepVar(<sweepVar>)** for specification of *instruction.sweepVar*.
        """
        
        self.step = None
        """        
        Setting for parameter stepping.
        
        See **instruction.setStepOn()** and **instruction.setStepOff()** for specification of *instruction.step*.
        """
        
        self.stepVar = None
        """
        Defines the step variable (*str*) for step types 'lin', 'log' and 'list'.
        
        See **instruction.setStepVar(<stepVar>)** for specification of *instruction.stepVar*.
        """
        
        self.stepVars = None
        """
        Defines the step variables for 'array' type parameter stepping.
        
        See **instruction.setStepArray(<stepArray>)** for specification of *instruction.stepArray*.
        """
        
        self.stepMethod = None
        """
        Step method for parameter stepping.
        
        See **instruction.setStepMethod(<stepMethod>)** for specification of *instruction.stepMethod*.
        """
        
        self.stepStart = None
        """
        Start value for stepping methods 'lin' and 'log'.
        
        See **instruction.setStepStart(<stepStart>)** for specification of *instruction.stepStart*.
        """
        
        self.stepStop = None
        """
        Stop value for stepping methods 'lin' and 'log'.
        
        See **instruction.setStepStop(<stepStop>)** for specification of *instruction.stepStop*.
        """
        
        self.stepNum = None
        """
        Number of steps for step methods 'lin' and 'log'.
        
        See **instruction.setStepNum(<stepNum>)** for specification of *instruction.stepNum*.
        """
        
        self.stepList = []
        """
        List with values for step method 'list'. 
        
        See **instruction.setStepList(<stepList>)** for specification of *instruction.stepList*.
        """
        
        self.stepArray = []
        """
        Array (*list of lists*) with values for step method array.
        
        See **instruction.setStepArray(<stepArray>)** for specification of *instruction.stepArray*.
        """
        
        self.source = None 
        """
        Refdes of the signal source (independent v or i source).
        
        See **instruction.setSource(<source>)** for specification of the source.
        """
        
        self.detector = None
        """
        Names of the positive and negative detector.
        
        See **instruction.setDetector(<detector>)** for specification of the detector.
        """
        
        self.lgRef = None
        """
        Refdes of the controlled source that is assigned as loop gain reference.
        
        See **instruction.setLGref(<detector>)** for specification of the loop
        gain reference.
        """
        
        self.circuit = None
        """
        Circuit (*obj*) used for this instruction. Can be assigned by setting
        this attribute, or is will be defined by running:
        instruction.setCircuit(<fileName>).
        
        :Example:
            
        >>> # Create an instance of a circuit object by checking a netlist:
        >>> my_circuit = checkCircuit('my_circuit.cir')
        >>> # create an instance of an instruction object:
        >>> my_instruction = instruction()
        >>> Use the circuit 'my_circuit' or the instruction 'my_instruction'.
        >>> my_instruction.circuit = my_circuit
        
        :Example:
        
        >>> # create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')
        """
        
        self.parDefs = None
        """
        Parameter definitions (*dict*) used for this instruction.
        
        
        This dictionary hold key-value pairs of parameter definitions in the
        circuit (netlist entries: .param parName = parValue). Keys are sympy
        symbols and values are either numeric or sympy expressions.
        
        The dictionary is updated when executing an instruction, and when using 
        the methods instruction.delPar(<parName>) and instruction.defPar(<parName>, 
        <parValue | parExpr>).
        
        :note: 
        
        The contents of this dict is determinedduring the checking of the 
        circuit and it should not be modified directly by the user. 
        
        Use the method **instruction.delPar(<parName>)** or the method
        **instruction.defPar(<parName>, <parValue | parExpr>)** to alter
        definitions of circuit parameters.
        """
        
        self.numeric = None
        """
        Variable used during analysis an presentation of analysis results.
        
        :note:
            
        The instruction.numeric attribute should not be modified
        directly by the user. Use the method **instruction.setSimType(<simTipe>)**
        to alter the simulation method!
        """
        
        self.errors = 0
        """
        Number of errors found in the definition of this instruction.
        
        :note:
            
        The instruction.errors attribute should not be modified
        directly by the user. It is determined automatically when executing
        the instruction.
        """
        
        self.detUnits = None
        """
        Detector units 'V' or 'A' (automatically detected in **instruction.chekDetector()**).
        """
        
        self.srcUnits = None
        """
        Source units 'V' or 'A' (automatically detected in **instruction.chekDetector()**).
        """
        
        self.detLabel = None
        """
        Name for the detector quantity to be used in expressions or plots 
        (automatically determined in **instruction.chekDetector()**).
        """
    
    def setSweepVar(self, sweepVar):
        """
        Defines the sweep variable for parameter sweeping
        
        :param sweepVar: Name of the parameter
        :type simType: str
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # Set the simulation type to numeric:
        >>> my_instr.setSimType('numeric')
        >>> # Set the data type to 'params'
        >>> my_instr.setDataType('params')
        >>> # Define the sweep parameter
        >>> my_instr.setSweepVar(<my_par_name>)        
        """
        self.simType = simType
        self.checkSimType()
        return
    
    def setSimType(self, simType):
        """
        Defines the simulation type for the instruction.
        
        :param simType: Simulation type: 'symbolic' or 'numeric'
        :type simType: str
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # Set the simulation type to numeric:
        >>> my_instr.setSimType('numeric')
        >>> # Set the simulation type to symbolic:
        >>> my_instr.setSimType('symbolic')
        
        :note:
        
        SLiCAP always uses symbolic calculation methods. Only in a limited
        number of cases SLiCAP calulates with floats (pole-zero analysis).
        
        With the simulation type set to 'numeric' SLiCAP recursively 
        substitutes all circuit parameter definitions into expressions used for
        element values. Hence, expressions can still have symbolic parameters.
        
        The default number of recursive substitutions is 10. It is defined by 
        ini.recSubst and can be changed by the user.
        
        :Example:
            
        >>> ini.recSubst = 12 # For deeply nested expressions!
        
        """
        self.simType = simType
        self.checkSimType()
        return
    
    def checkSimType(self):
        """
        Checks if the simulation type is defined correctly."
        
        Called by **instruction.check()** and by **setSimType(<simType>)**.
        """
        if type(self.simType) == str:
            if self.simType.lower() == 'symbolic':
                self.simType = 'symbolic'
                self.numeric = False
            elif self.simType.lower() == 'numeric':
                self.simType = 'numeric'
                self.numeric = True
            else:
                print "Error: unknown simulation type: '%s'."%(str(self.symType))
                self.errors += 1
        else:
            print "Error: argument type must be type 'str'."
            self.errors += 1
            
    def setGainType(self, gainType):       
        """
        Defines the gain type for the instruction.
        
        :param gainType: gain type for the instruction'gain', 'asymptotic', 
                         'loopgain', 'servo', 'direct', or 'vi'.
        :type gainType: str
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # Set gain type to 'gain':
        >>> my_instr.setGainType('gain')
        """
        self.gainType = gainType
        self.checkGainType()
    
    def checkGainType(self):
        """
        Checks if the gain type is defined correctly."
        
        Called by **instruction.check()** and by **setGainType(<gainType>)**.
        """
        if type(self.gainType) == str:
            if self.gainType.lower() in GAINTYPES:
                self.gainType = self.gainType.lower()
            else:
                print "Error: unknown gain type: '%s'."%(str(self.gainType))
                self.errors += 1
        elif self.gainType == None:
            print "Error: missing gain type."
        else:
            print "Error: argument type must be type 'str'."
            self.errors += 1
        return  

    def setDataType(self, dataType):
        """
        Defines the data type for the instruction.
        
        :param dataType: data type for the instruction: 'dc', 'dcsolve', 'dcvar', 
                         'denom', 'impulse', 'laplace', 'matrix', 'noise', 'numer', 
                         'poles', 'pz', 'solve', 'step', 'time' or 'zeros'.
        :type dataType: str
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # Set data type to 'laplace':
        >>> my_instr.setDataType('laplace')
        """
        self.dataType = dataType
        self.checkDataType()
        return  
    
    def checkDataType(self):
        """
        Checks if the data type is defined correctly."
        
        Called by **instruction.check()** and by **setDataType(<dataType>)**.
        """
        if type(self.dataType) == str:
            if self.dataType.lower() in DATATYPES:
                self.dataType = self.dataType.lower()
            else:
                print "Error: unknown data type: '%s'."%(str(dataType))
                self.errors += 1
        elif self.dataType == None:
            self.errors += 1
            print "Error: missing data type specification."
        else:
            print "Error: data type must be type 'str' or 'None'."
    
    def stepOn(self):
        """        
        Enables parameter stepping.
        
        Does not change other settings for parameter stepping.
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # Enable parameter stepping
        >>> my_instruction.stepOn()
        """
        self.step = True
        return
    
    def stepOff(self):
        """        
        Disables parameter stepping.
        
        Does not change other settings for parameter stepping.
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # Disable parameter stepping
        >>> my_instruction.stepOff()
        """
        self.step = False
        return

    def setStepVar(self, stepVar):
        """
        Defines the step variable for step types 'lin', 'log' and 'list'.
        
        :param stepVar: step variable
        :type stepVar: str, sympy.symbol.Symbol
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # Define circuit parameter 'alpha' as step variable:
        >>> my_instr.setStepVar('alpha')
        >>> # Enable parameter stepping
        >>> my_instr.stepOn()
        
        :note:
            
        A list with names (*sympy.symbol.Symbol*) that can be used as stepping
        parameter is obtained as follows:
            
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')
        >>> # print the list with names of all parameters that can be stepped:
        >>> print instr.circuit.params + instr.circuit.parDefs.keys()
        """
        self.stepVar = stepVar
        self.checkStepVar
        return
    
    def checkStepVar(self):
        """
        Checks if the step variable is defined correctly.
        
        Called by **instruction.checkStep()** and by **setStepVar(<stepVar>)**.
        """
        if self.stepVar == None:
            self.errors += 1
            print "Error: missing step variable."
        elif checkNumber(self.stepVar) == None:
            if isinstance(self.stepVar, sp.symbol.Symbol):
                pass
            elif type(self.stepVar) == str:
                self.stepVar = sp.Symbol(self.stepVar)
            else:
                self.errors += 1
                print "Error: argument type must be 'str' or 'sympy.symbol.Symbol'."
            if self.stepVar not in self.circuit.parDefs.keys() and self.stepVar not in self.circuit.params:
                print "Warning: unknown step parameter '%s'."%(self.stepVar)
        return

    def setStepVars(self, stepVars):
        """
        Defines the step variables for 'array' type stepping.
        
        :param stepVars: List with names (*str, sympy.symbol.Symbol*) of step
                         variables for array type stepping.
        :type stepVars: list
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')
        >>> # Define 'array' type stepping:
        >>> my_instr.stepMethod = 'array'
        >>> # Define circuit parameters 'R_a' and 'C_a' as step variables:
        >>> my_instr.setStepVars(['R_a', 'C_a'])
        >>> Define the step values for 'R_a and 'C_a':
        >>> my_instr.setStepArray ([['1k', 1200, 1.2e3],['1u', 10e-6, 0.0001]])
        >>> # Enable parameter stepping
        >>> my_instruction.stepOn()
        
        :note:
            
        A list with names (*sympy.symbol.Symbol*) that can be used as stepping
        parameter is obtained as follows:
            
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')
        >>> # print the list with names of all parameters that can be stepped:
        >>> print instr.circuit.params + instr.circuit.parDefs.keys()
        """
        self.stepVars = stepVars
        self.check(stepVars)
        return
    
    def checkStepVars(self):
        """
        Checks if the step variables for array stepping are defined correctly.
        
        Called by **instruction.checkStep** and by **instruction.setStepVars(<stepVars>)**.
        """
        if self.stepVars == None:
            self.errors += 1
            print "Error: missing list stepVars."
            return
        errors = 0
        if type(self.stepVars) == list:
            if len(self.stepVars) != 0:
                for stepVar in self.stepVars:
                    if checkNumber(stepVar) == None:
                        if type(stepVar) == str:
                            try:
                                stepVar = sp.Symbol(stepVar)
                            except:
                                errors += 1
                                print "Error: step variable '%s' is not a parameter."%(stepVar)
                        if isinstance(stepVar, sp.symbol.Symbol) and stepVar not in self.circuit.parDefs.keys() and stepVar not in self.circuit.params:
                            print "Warning: unknown step parameter '%s'."%(str(stepVar))
                        else:
                            errors += 1
                            print "Error: argument type must be 'str' or 'sympy.symbol.Symbol'."
                    else:
                        errors += 1
                        print "Error: step variable cannot be numeric."
            else:  
                errors += 1
                print "Error: empty stepVars." 
        else:
            print "Error: argument should be a list."
            errors += 1
        self.errors += errors 
        return

    def setStepMethod(self, stepMethod):
        """
        Defines the parameter stepping method.
        
        :param stepMethod: 'lin', 'log', 'list' or 'array'.
        :type stepMethod: str
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')
        >>> # Define 'linear' type stepping:
        >>> my_instr.setStepMethod('lin')
        >>> # Enable parameter stepping
        >>> my_instr.stepOn()
        """
        self.stepMethod = stepMethod
        self.checkStepMethod()
        return
    
    def checkStepMethod(self):
        """
        Checks if the step method is defined correctly.
        
        Called by **instruction.checkStep** and by **instruction.setStepVMethod(<stepMethod>)**.
        """
        if self.stepMethod == None:
            self.errors += 1
            print "Error: missing step method definition."
        elif type(self.stepMethod) != str:
            self.errors += 1
            print "Error: stepMethod should be type 'str'."
        else:
            stepMethods = ['lin', 'log', 'list', 'array']
            if self.stepMethod.lower() not in stepMethods:
                self.errors += 1
                print "Error: unknown step method '%s',"%(self.stepMethod)
            else:
                self.stepMethod == self.stepMethod.lower()
        return
    
    def setStepStart(self, stepStart):
        """
        Start value for parameter stepping methods 'lin' and 'log'.
        
        :param stepStart: Start value for parameter stepping methods 'lin' and 'log'.
        :type stepStart: str, int, float
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')
        >>> # Define linear stepping:
        >>> my_instr.stepMethod = 'lin'
        >>> # Define the start value
        >>> my_instr.setStepStart('1k')  # 1E3
        >>> my_instr.setStepStart(1000)  # 1E3
        >>> my_instr.setStepStart(1e3)   # 1E3
        >>> # Enable parameter stepping
        >>> my_instr.stepOn()
        """
        self.stepStart = stepStart
        self.checkStepStart()
        return
    
    def checkStepStart(self):
        """
        Checks if the start value for parameter steping is defined correctly.
        
        Called by **instruction.checkStep()** and by **instruction.stepStart(<stepStart>)**.
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
    
    def setStepStop(self, stepStop):
        """
        End value for parameter stepping methods 'lin' and 'log'.
        
        :param stepStop: End value for parameter stepping methods 'lin' and 'log'.
        :type stepStop: str, int, float
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')
        >>> # Define linear stepping:
        >>> my_instr.stepMethod = 'lin'
        >>> # Define the start value
        >>> my_instr.setStepStop('1M')  # 1E6
        >>> my_instr.setStepStop(1e6)   # 1E6
        >>> # Enable parameter stepping
        >>> my_instr.stepOn()
        """
        self.stepStop = stepStop
        self.checkStepStop()
        return
    
    def checkStepStop(self):
        """
        Checks if the end value for parameter steping is defined correctly.
        
        Called by **instruction.checkStep()** and by **instruction.stepStop(<stepStop>)**.
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
    
    def setStepNum(self, stepNum):
        """
        Defines the number of steps for 'lin' and 'log' parameter stepping.
        
        :param stepNumber: Number of steps for stepping methods 'lin' and 'log'.
        :type stepStop: int
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')
        >>> # Define linear stepping:
        >>> my_instr.stepMethod = 'lin'
        >>> # Define the start value
        >>> my_instr.setStepStop('1M')  # 1E6
        >>> my_instr.setStepStop(1e6)   # 1E6
        >>> # Enable parameter stepping
        >>> my_instr.stepOn()
        """
        self.stepNum = stepNum
        self.checkStepNum()
        return
        
    def checkStepNum(self):
        """
        Checks if the numper of steps is defined properly.
        
        Called by :**instruction.checkStep()** and by **instruction.setStepNum(<stepNum>)**.
        
        Also called by and by **instruction.setStepNum(<stepNum>)**.
        """
        if self.stepNum == None:
            self.errors += 1
            print "Error: missing stepNum value."
        else:
            if type(self.stepNum) == int:
                if self.stepNum <= 0:
                    self.errors += 1
                    print "Error: step number must be a positive nonzero integer."
            else:
                self.errors += 1
                print "Error: step number type must be 'int'."
        return
    
    def setStepList(self, stepList):
        """
        Defines the list with step values for step method 'list'. 
        
        :param stepList: List with step values for the step parameter.
        :type stepList: list
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')
        >>> # Define 'list' type stepping:
        >>> my_instr.setStepMethod('list')
        >>> # Define the circuit parameter 'alpha' as step parameter:
        >>> my_instr.setStepVar('alpha')
        >>> # Define a list of step values for this parameter.
        >>> my_instr.setStepList(['10m', '20m', '50m', 0.1, 0.2, 0.5, 1, 2, 5])
        >>> # Enable parameter stepping
        >>> my_instr.stepOn()
        """
        self.stepList = stepList
        self.checkStepList()
        return
    
    def checkStepList(self):
        """
        Checks if the list with step values is defined properly.
        
        Called by **instruction.checkStep()** and by **instruction.setStepList(<stepList>)**.
        
        :return: None
        :return type: None
        """
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
    
    
    def setStepArray(self, stepArray):
        """
        Defines the array with values for step method array.
        
        :param stepArray: Nested list: list[i] carries the step values for the 
                          step variable in instruction.stepVars[i]. 
                          The lists should have equal lengths.
        :type stepArray: list
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')
        >>> # Define 'array' type stepping:
        >>> my_instr.setStepMethod('array')
        >>> # Define circuit parameters 'R_a' and 'C_a' as step variables:
        >>> my_instr.setStepVars(['R_a', 'C_a'])
        >>> Define the step values for 'R_a and 'C_a':
        >>> my_instr.setStepArray([['1k', 1200, 1.2e3],['1u', 10e-6, 0.0001]])
        >>> # Enable parameter stepping
        >>> my_instr.stepOn()
        """
        self.stepArray = stepArray
        self.checkStepArray()
        return
   
    def checkStepArray(self):
        """
        Checks if the array with step values is defined properly.
        
        Called by **instruction.checkStep()** and by **instruction.setStepArray(<stepArray>)**.
        
        The step array is a list of lists. The number of lists must equal the
        number of step variables. The numbers in the lists are subsequent 
        values of the associated step variable. All lists should have equal 
        lengths.
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
    
    
    def setSource(self, source):
        """
        Defines the signal source.
        
        :param source: Name of an independent voltage or current source that
                       exists in the circuit.
        :type source: str
        
        :return: None
        :return type: None

        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')
        >>> # Define the voltage source 'V1' as signal source:
        >>> my_instr.setSource('V1')
        
        :note:
            
        A list with names of independent voltage and current sources that can be 
        assigned as signal source can be obtained from the method: 
        **instruction.idepVars()**:
        
        :Example:
        
        >>> # Create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')
        >>> # Obtaine a list with names of independent sources:
        >>> my_instr.circuit.idepVars()
        """
        self.source = source
        self.checkSource(need = False)
        return    

    def checkSource(self, need = True):
        """
        Checks if the source has been defined and if it exists in the circuit.
        
        Called by **instruction.check()** and by **instruction.setSource(<source>)**.
        
        
        :param need: If True, a source is required and an error message will be
                     given if it missing. If False, only the presence of the
                     indicated independent source in the circuit will be 
                     verified.
                     
        :type need: bool
        """
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
    
    def setDetector(self, detector):
        """
        Defines the signal detector
        
        :param detector: Name(s) of one or two nodal voltages or of one or two 
                         dependent currents.
        :type detector: list, str
        
        :return: None
        :return type: None
        
        detector can defined as:
            
        - bool: None: no detector has been defined
        - str:  a single detector, name of a nodal voltage or a branch current
        - list: with two either two nodal voltages or two branch currents
        
        instruction.checkDetector converts the detector definition into a list 
        with a positive and a negative detector [<detP>, <detN>], where detP 
        and detN are the names (str) of either two nodal voltages or two branch
        currents. One of those can be 'None'.
        
        A list with names of dependent variables that can be used as signal 
        detector is returned by the method: **instruction.depVars()**.
        
        :Example:
        
        >>> # create an instance if a SLiCAP instruction
        >>> my_instr = instruction()  
        >>> # create my_instr.circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_instr.setCircuit('myFirstRCnetwork.cir')
        >>> # Display a list with names of nodal voltages and branch currents
        >>> # that can be assigned to the detector.
        >>> my_instr.depVars()
        ['I_V1', 'V_0', 'V_N001', 'V_out']
        >>> # Define 'V_out' as detector
        >>> my_instr.setDetector('V_out')
        
        :note:
            
        The voltage 'V_0' at the reference node '0' equals zero. 
        """
        self.detector = detector
        self.checkDetector()
        return

    def checkDetector(self):
        """
        
        Checks if the detector has been defined and if it exists in the circuit.
        
        Called by **instruction.check()** and by **instruction.setDetector(<detector>)**.
        
        """
        if self.detector != None:
            self.detLabel = ''
            # detector has two nodes or two voltage sources
            if type(self.detector) == str:
                # Change the detector definition
                self.detector = [self.detector, None]
            elif type(self.detector) == list:
                numDets = len(self.detector)
                if numDets == 0:
                    self.errors += 1
                    print "Error: missing detector specification"
                elif numDets == 1:
                    self.detector = [self.detector[0], None]
                elif numDets > 2:
                    self.errors += 1
                    print "Error: to many detectors."
            if self.errors !=0:
                return
            detP = self.detector[0]
            detN = self.detector[1]
            if detP == None and detN == None:
                self.errors += 1
                print "Error: missing detector specification."
                return
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
                self.detLabel += detP
            elif self.detector[1] != None:
                self.detUnits = detN[0].upper()
                self.detLabel += '-' + detN
            if self.detUnits == 'I':
                self.detUnits = 'A'
        else:
            self.errors += 1
            print "Error: missing detector definition."
        return
    
    def setLGref(self, lgRef):
        """
        Defines the loop gain reference (name of a controlled source).
        
        A list with names of dependent (controlled) sources is returned by the
        method **instruction.controlled()**.
        
        :param lgRef: Name of the loop gain reference.
        :type lgRef: str, sympy.Symbol
        
        :return: None
        :return type: None
            
        :Example:
            
        >>> # create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')   
        >>> # Display a list with controlled sources of the circuit:
        >>> my_instr.controlled()
        """
        self.lgRef = lgRef
        self.checkLGref()
        return
    
    def checkLGref(self):
        """
        Called by **instruction.check()** and by **instruction.setLGref(<lgRef>)**.
        
        Checks if the loop gain reference has been defined and if it exists in 
        the circuit.
        """
        if type(self.lgRef) == bool:
            self.errors += 1
            print "Error: missing loop gain reference definition."
        elif self.lgRef not in self.circuit.controlled:
            self.errors += 1
            print "Error: unkown loop gain reference: '%s'."%(self.lgRef)
        return

    def delPar(self, parName):
        """
        Deletes a parameter definition
        
        After deletion it updates the list **instruction.circuit.params** with 
        names (*sympy.Symbol*) of undefined parameters.
        
        :param parName: Name of the parameter.
        :type parName: str, sympy.Symbol
        
        :return: None
        :return type: None
        
        :Example:
            
        >>> # create an instance if a SLiCAP instruction
        >>> my_instr = instruction()  
        >>> # create my_instr.circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_instr.setCircuit('myFirstRCnetwork.cir')
        >>> # Delete the definition for the parameter 'R':
        >>> my_instr.delPar('R')
        >>> # Or:
        >>> my_instr.circuit.delPar('R')
        """
        self.circuit.delPar(parName)
        return
        
    def defPar(self, parName, parValue):
        """
        Adds or modifies a parameter definition and updates the list 
        **instruction.circuit.params** with names (*sympy.Symbol*) of undefined 
        parameters.
        
        :param parName: Name of the parameter.
        :type parName: str, sympy.Symbol
        :param parValue: Value or expression.
        :type parName: str, sympy.Symbol
        
        :return: None
        :return type: None
        
        :Example:
            
        >>> # create an instance if a SLiCAP instruction
        >>> my_instr = instruction()  
        >>> # create my_instr.circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_instr.setCircuit('myFirstRCnetwork.cir')
        >>> # Define the value of 'R' as 2000
        >>> my_instr.defPar('R', '2k')
        >>> # Or:
        >>> my_instr.defPar('R', 2e3)
        
        :note: 
            
        Do not enter a number as parameter name, this will not be checked!
        """
        self.circuit.defPar(str(parName), parValue)
        return
    
    def defPars(self, parDict):
        """
        Adds or modifies multiple parameter definitions and updates the list 
        **instruction.circuit.params** with names (*sympy.Symbol*) of undefined 
        parameters.
                
        :params parDict: Dictionary with key-value pairs:
                         key: parName (*str, sympy.Symbol*): name of the parameter.
                         value: parValue (*str, float, int, sp.Symbol*) : value 
                         or expression of the parameter.
        :type parDict:   dict
        
        :return: None
        :return type: None
        
        :Example:
            
        >>> # create an instance if a SLiCAP instruction
        >>> my_instr = instruction()  
        >>> # create my_instr.circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_instr.setCircuit('myFirstRCnetwork.cir')
        >>> # Define the value of 'R' as 2000 and 'C' as 5e-12:
        >>> my_instr.defPars({'R': '2k', 'C': '5p')
        
        :note: 
            
        Do not enter a number as parameter name, this will not be checked!
        """
        # define multiple parameters.
        self.circuit.defPars(parDict)
        return
    
    def getParValue(self, parName):
        """
        Returns the value or expression of one or more parameters.
        
        If instruction.numeric == True it will perform a full recursive 
        substitution of all circuit parameter definitions.
        
        This method calls instruction.circuit.getParValue() with keyword arg
        numeric = True if instruction.simType == 'numeric'.
        
        :param parName: name(s) of the parameter(s)
        :type parName: str, sympy.Symbol, list 
        
        :return: if type(parNames) == list:
            
                 return value = dict with key-value pairs: key (*sympy.Symbol*): 
                 name of the parameter, value (*int, float, sympy expression*): 
                 value of the parameter
                 
                 else:
                 value or expression
                 
        :return type: dict, float, int, sympy obj
        
        :Example:
         
        >>> # create an instance if a SLiCAP instruction
        >>> my_instr = instruction()  
        >>> # create my_instr.circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_instr.setCircuit('myFirstRCnetwork.cir')
        >>> # Obtain the numeric parameter definitions of of 'R' and 'C':
        >>> my_instr.symType = 'numeric'
        >>> my_instr.getParValues(['R', 'C'])
        
        :note: 
        
        Do not enter a number as parameter name, this will not be checked!
        """
        if self.simType == 'numeric':
            self.numeric = True
        else:
            self.numeric = False
        return self.circuit.getParValue(parName, self.numeric)
    
    def indepVars(self):
        """
        Returns a list with names of independent sources in **instruction.circuit**
        
        :return: list with names of independent sources in **instruction.circuit**
        :return type: list
        
        :Example:
            
        >>> # create an instance if a SLiCAP instruction
        >>> my_instr = instruction()  
        >>> # create my_instr.circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_instr.setCircuit('myFirstRCnetwork.cir')
        >>> # Obtain a list with names of independent sources:
        >>> my_instr.indepVars()
        ['V1']
        """
        return self.circuit.indepVars
    
    def depVars(self):
        """
        Returns a list with names of nodal voltages and branch currents that can
        be used as detector.
        
        :return: list with names of nodal voltages and branch currents
        :return type: list
        
        :Example:
            
        >>> # create an instance if a SLiCAP instruction
        >>> my_instr = instruction()  
        >>> # create my_instr.circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_instr.setCircuit('myFirstRCnetwork.cir')
        >>> # Obtain a list with names of dependent variables:
        >>> my_instr.depVars()
        ['I_V1', 'V_0', 'V_N001', 'V_out']
        """
        return self.circuit.depVars
    
    def controlled(self):
        """
        Returns a list with names of controlled sources in **instruction.circuit** 
        that can be used as loop gain reference.
        
        :return: list with names of controlled sources in **instruction.circuit**
        :return type: list
        :Example:
            
        >>> # create an instance if a SLiCAP instruction
        >>> my_instr = instruction()  
        >>> # create my_instr.circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_instr.setCircuit('myFirstRCnetwork.cir')
        >>> # Obtain a list with names of controlled sources:
        >>> my_instr.controlled()
        []
        """
        return self.circuit.controlled
    
    def stepParams(self, paramPlot):
        """
        TBD
        """
        parNames = self.circuit.parDefs.keys() + self.circuit.params
        errors = 0
        xValues = {}
        yValues = {}
        # check the input
        if paramPlot.xVar == None:
             print "Error: missing x variable."
             errors +=1
        elif sp.Symbol(paramPlot.xVar) not in parNames:
            print "Error: unknown parameter: '%s'."%(paramPlot.xVar)
            errors += 1
        if paramPlot.sVar == None:
             paramPlot.svar = paramPlot.xVar
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
        if paramPlot.sNum == None:
            print "Error: missing number of points for x variable."
            errors += 1
        else:
            sNum = checkNumber(paramPlot.sNum)
            if sNum == None:
                print "Error: '%s' is not a number."%(paramPlot.sNum)
                errors += 1
        if paramPlot.sStart == None:
            print "Error: missing start value for x variable."
            errors += 1
        else:
            sStart = checkNumber(paramPlot.sStart)
            if sStart == None:
                print "Error: '%s' is not a number."%(paramPlot.sStart)
                errors += 1
        if paramPlot.sStop == None:
            print "Error: missing stop value for x variable."
            errors += 1
        else:
            sStop = checkNumber(paramPlot.sStop)
            if paramPlot.sStop == None:
                print "Error: '%s' is not a number."%(paramPlot.sStop)
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
            if paramPlot.sMethod.lower() == 'lin':
                s = np.linspace(sStart, sStop, num = sNum)
            elif paramPlot.xMethod.lower() == 'log':
                s = np.geomspace(sStart, sStop, num = sNum)
            else:
                print "Error: unknown method '%s'."%(paramPlot.sMethod)
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
                if parName != sp.Symbol(paramPlot.sVar) and paramPlot.pVar != None and parName != sp.Symbol(paramPlot.pVar):
                    substitutions[parName] = self.circuit.parDefs[parName]
            f = fullSubs(self.circuit.parDefs[sp.Symbol(paramPlot.yVar)], substitutions)
            g = fullSubs(self.circuit.parDefs[sp.Symbol(paramPlot.xVar)], substitutions)
            if paramPlot.pVar != None:
                for parValue in p:
                    y = f.subs(sp.Symbol(paramPlot.pVar), parValue)
                    yfunc = sp.lambdify(sp.Symbol(paramPlot.sVar), y)
                    yValues[parValue] = np.array([yfunc(s[i]) for i in range(len(s))])
                    if paramPlot.xVar != paramPlot.sVar:
                        x = g.subs(sp.Symbol(paramPlot.pVar), parValue)
                        xfunc = sp.lambdify(sp.Symbol(paramPlot.sVar), x)
                        xValues[parValue] = np.array([xfunc(s[i]) for i in range(len(s))])
            else:
                y       = sp.lambdify(sp.Symbol(paramPlot.sVar), f)
                yValues = np.array([func(s[i] for i in range(len(s)))])
                if paramPlot.xVar != paramPlot.sVar:
                    x       = sp.lambdify(sp.Symbol(paramPlot.sVar), g)
                    xValues = np.array([func(s[i] for i in range(len(s)))])
            if paramPlot.xVar == paramPlot.sVar:
                xValues = s
            paramPlot.yValues = yValues
            paramPlot.xValues = xValues
        return paramPlot
    
    def setCircuit(self, fileName):
        """
        Defines the circuit for this instruction.
        
        - Checks the netlist file 'fileName'
        - Creates a circuit object from it
        - Makes it the (local) ciruit object for this instruction.
        
        :param fileName: Name of the netlist file.
        :type fileName: str
        
        :return: None
        :return type: None
        
        :Example:
            
        >>> # create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')            
        """
        self.circuit = checkCircuit(fileName)
        return
        
    def checkCircuit(self):
        """
        Checks if the circuit for this instruction is a check :c;ass:`SLiCAPprotos.circuit()` object.
        """
        if self.circuit == None:
            self.errors += 1
            print "Error: missing circuit definition."
        elif type(self.circuit.params) == dict:
            self.errors += 1
            print "Error: empty circuit object for this instruction."
        elif type(self.circuit) != type(circuit()):
            self.errors += 1
            print "Error: not SLiCAP a circuit object for this instruction."
        return
        
    def check(self):
        """
        Checks the completeness and consistancy of the instruction data.  
        Will be called by **self.execute()**. 
        
        :return: None
        :return type: None
                
        :Example:
        
        >>> # create an instance of the instruction object
        >>> my_instr = instruction() 
        >>> # check a netlist file and use the circuit from this file for this
        >>> # instruction:
        >>> my_instr.setCircuit('my_circuit.cir')
        """
        self.errors = 0
        self.checkCircuit()
        self.checkSimType()
        self.checkGainType()
        self.checkDataType()
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
            elif self.gainType != 'loopgain':
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
            if self.gainType == 'asymptotic' or self.gainType == 'direct' or self.gainType == 'loopgain' or self.gainType == 'servo':
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
        """
        Called by **instruction.check()** in cases in which a numeric 
        simulation is required.
        
        Checks if the simulation type is set to 'numeric'. This is required for
        pole-zero analysis.
        
        :return: None
        :return type: None
        """
        if not self.numeric:
            self.errors += 1
            print "Error: dataType '%s' not available for simType: '%s'."%(self.dataType, self.simType)
        return
    
    def checkStep(self):
        """
        Called by **instruction.check()** in cases in which 
        instruction.step == True
        
        This method will check the completeness and the consistency of the 
        instruction data for parameter stepping, before executing the 
        instruction.
        
        :return: None
        :return type: None
        """
        self.checkStepMethod()
        if self.errors == 0:
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
                # We need a list without errors before we can check the array
                if self.errors == 0:
                    self.checkStepArray()
        return
    
    def execute(self):
        """
        Checks the instruction and executes it in case no errors have been found.
        
        if no errors are found it returns a :class:`allResults` object with the 
        results of the instruction.
        
        :return: :class:`allResults` object with results of the execution
        :return type: obj
        :Example:
        
        >>> # create an instance if a SLiCAP instruction
        >>> my_instr = instruction()  
        >>> # create my_instr.circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_instr.setCircuit('myFirstRCnetwork.cir')
        >>> # Assign 'V1' signal source:
        >>> my_instr.source = 'V1'
        >>> # Assign 'V_out' detector:
        >>> my_instr.detector = 'V_out'
        >>> # Set the simulation type to 'symbolic'
        >>> my_instr.simType = 'symbolic'
        >>> # Set the gain type to 'gain'
        >>> my_instr.gainType = 'gain'
        >>> # Set the data type to 'laplace'
        >>> my_instr.dataType = 'laplace'
        >>> result = my_instr.execute()
        >>> print result.laplace
        """
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
            r.sweepVar       = self.sweepVar
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
            r.detLabel       = self.detLabel
            return doInstruction(r)
        
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