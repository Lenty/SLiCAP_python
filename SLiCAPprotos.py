#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from SLiCAPmath import *

# Globals used by this script and by SLiCAPyacc.py:

HIERARCHY   = []                # Check list for hierarchical loops
MODELS      = {}                # Dictionary with SLiCAP built-in models
                                #   key   : model name
                                #   value : associated model object
DEVICES     = {}                # Dictionary with SLiCAP built-in devices
                                #   key   : device name
                                #   value : associated device object
class circuit(object):
    """
    Prototype (sub)circuit object. It has the following attributes with their
    default values:
        
    title      = ''    # Title of (sub) circuit
    file       = []    # Name of the netlist file
    lexer      = None  # Tokenized input file
    subCKT     = False # True if sub circuit
    elements   = {}    # Dictionary with the circuit's element  objects
                       #   key (str)  : element refDes
                       #   value (obj): associated element object
    nodes      = []    # Connecting nodes to parent circuit
    params     = {}    # Before expansion: Parameters that can be be passed 
                       # from parent circuit (sub circuit only)
                       # key (sympy.Symbol)                  : model parameter 
                       #                                       name
                       # value (sympy expression, int, float): parameter value 
                       #                                       or expression
                       # After expansion: List with undefined parameters 
                       # (sympy.Symbol) 
    parDefs    = {}    # Dictionary with paremeter definitions
                       # key (sympy.Symbol)                  : parameter name
                       # value (sympy expression, int, float): parameter value 
                       #                                       or expression                                      
    modelDefs  = {}    # Dictionary with model definitions found in 
                       # the circuit:
                       #   key (str)  : model name
                       #   value (obj): modelDef object
    circuits   = {}    # Dict with sub circuit definitions found in
                       # the netlist (before expansion)
                       #   key (str)  : sub circuit name
                       #   value (obj): circuit object
    errors     = 0     # Number of errors found during checking (int)
    libs       = []    # List with library files
    indepVars  = []    # List with sources that can be used as signal source
    depVars    = []    # List with dependent variables that can be used as 
                       # detector
    controlled = []    # List with controlles sources that can be used as loop
                       # gain reference
    varIndex   = {}    # Dictionary with index of node or dependent
                       # current (speeds up the building of the matrix)
                       #   key (str)  : node name or current name
                       #   value (int): row position in the vector with
                       #                dependent variables, before removal of
                       #                row with reference node
    """
    def __init__(self):
        """
        Initialization of the circuit object, see description above.
        """
        self.title      = '' 
        self.file       = []
        self.lexer      = None
        self.subCKT     = False
        self.elements   = {}
        self.nodes      = []
        self.params     = {}
        self.parDefs    = {}
        self.parUnits   = {}
        self.modelDefs  = {}
        self.circuits   = {}
        self.errors     = 0
        self.libs       = []
        self.indepVars  = []
        self.depVars    = []
        self.controlled = []
        self.varIndex   = {}
    
    def delPar(self, parName):
        """
        Deletes a parameter definition and updates the list 
        **circuit.params** with names (*sympy.Symbol*) of
        undefined parameters.
        
        :param parName: Name of the parameter.
        :type parName: str, sympy.Symbol
        
        :return: None
        :return type: None
        
        :Example:
            
        >>> # create my_circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_circuit = checkCircuit('myFirstRCnetwork.cir')
        >>> # Delete the definition for the parameter 'R':
        >>> my_circuit.delPar('R')
        """
        self.parDefs.pop(sp.Symbol(str(parName)), None)
        self.parUnits.pop(sp.Symbol(str(parName)), None)
        self.updateParams()
        return
        
    def defPar(self, parName, parValue, units = None):
        """
        Updates or adds a parameter definition and updates the list 
        **circuit.params** with names (*sympy.Symbol*) of undefined parameters.
        
        :param parName: Name of the parameter.
        :type parName: str, sympy.Symbol
        
        :param parValue: Value of the parameter.
        :type parValue: str, sympy.Symbol, sympy.Expr, int, float
        
        :param units: Value of the parameter, defaults to None
        :type units: str, sympy.Symbol, sympy.Expr, int, float
        
        :return: None
        :return type: None
        
        :Example:
            
        >>> # create my_circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_circuit = checkCircuit('myFirstRCnetwork.cir')
        >>> # Define the value of 'R' as 2000
        >>> my_circuit.defPar('R', '2k', )
        >>> # Or:
        >>> my_circuit.defPar('R', 2e3)
        """
        if checkNumber(parName) == None:
            parName = sp.Symbol(str(parName))
            parValue = sp.sympify(replaceScaleFactors(str(parValue)))
            self.parDefs[parName] = parValue
            if type(units) == str:
                # ToDo: checkUnits() calculate wir SI units.
                self.parUnits[parName] = units
            else:
                self.parUnits[parName] = ''
            self.updateParams()
        else:
            print "Error: cannot define a number as parameter."
        return
    
    def defParUnits(self, parDict):
        """
        Defines the units of a parameter.
        
        :param parDict: Dictionary with key-value pairs:
        
                        key(*str, sp.Symbol*): parameter name 
                        value(*str*): parameter units 
        :type parDict: dict
        
        :return: None
        :return type: None
        
        :Example:
            
        >>> # create my_circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_circuit = checkCircuit('myFirstRCnetwork.cir')
        >>> # Define the units of 'R' and 'C'
        >>> my_circuit.defParUnits({'R': 'Omega', C: F})
        """
        if type(parDict) == dict:
            for key in parDict.keys():
                if checkNumber(key) == None:
                    if type(parDict[key]) == str:
                        self.parUnits[key] = parDict[key]
                    else:
                        self.parUnits[key] = ''
                else:
                    print "Error: cannot use a number as parameter."
        else:
            print "Error: expected a dict type argument."
        return
    
    def defPars(self, parDict):
        """
        Adds or modifies multiple parameter definitions and updates the list 
        **circuit.params** with names (*sympy.Symbol*) of undefined parameters.
                
        :params parDict: Dictionary with key-value pairs:
                         key: parName (*str, sympy.Symbol*): name of the parameter.
                         value: parValue (*str, float, int, sp.Symbol*) : value 
                         or expression of the parameter.
        :type parDict:   dict
        
        :return: None
        :return type: None
        
        :Example:
        
        >>> # Create my_circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_circuit = checkCircuit('myFirstRCnetwork.cir')
        >>> # Define the value of 'R' as 2000 and 'C' as 5e-12:
        >>> my_circuit.defPars({'R': '2k', 'C': '5p')
        """
        if type(parDict) == dict:
            for key in parDict.keys():
                if checkNumber(key) == None:
                    parName = sp.Symbol(str(key))
                    parValue = str(parDict[key])
                    parValue = sp.sympify(replaceScaleFactors(str(parValue)))
                    self.parDefs[parName] = parValue
                else:
                    print "Error: cannot define a number as parameter."
        else:
            print "Error: expected a dict type argument."
        self.updateParams()
        return
        
    def getParValue(self, parNames, numeric = False):
        """
        Returns the value or expression of one or more parameters.
        
        If numeric == True it will perform a full recursive substitution of
        all circuit parameter definitions.
        
        :param parNames: name(s) of the parameter(s)
        :type parNames: str, sympy.Symbol, list 
        
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
        >>> my_instr.checkCircuit('myFirstRCnetwork.cir')
        >>> # Obtain the numeric parameter definitions of of 'R' and 'C':
        >>> my_instr.symType = 'numeric'
        >>> my_instr.getParValues(['R', 'C'])
        """
        if type(parNames) == list:
            parValues = {}
            for par in parNames:
                par = sp.Symbol(str(par))
                for key in self.parDefs.keys():
                    if par == key:
                        if numeric == True:
                            parValues[par] = fullSubs(self.parDefs[key], self.parDefs)
                        else:
                           parValues[par] = self.parDefs[key]          
            return parValues
        parNames = sp.Symbol(str(parNames))
        try:
            if numeric:
                parValue = sp.N(fullSubs(self.parDefs[parNames], self.parDefs))
            else:
                parValue = self.parDefs[parNames]
        except:
            print "Error: parameter '%s' has not been defined."%(str(parNames))
            parValue = None
        return parValue
    
    def getParUnits(self, parNames):
        """
        Returns the units of one or more parameters.
        
        :param parNames: name(s) of the parameter(s)
        :type parNames: str, sympy.Symbol, list 
        
        :return: if type(parNames) == list:
            
                 return value = list with units of the parameters
                 
                 else:
                 units (str)
                 
        :return type: list, str
        
        :Example:
         
        >>> # create an instance if a SLiCAP instruction
        >>> my_instr = instruction()  
        >>> # create my_instr.circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_instr.checkCircuit('myFirstRCnetwork.cir')
        >>> # Define and obtain the units of 'R' and 'C':
        >>> my_instr.symType = 'numeric'
        >>> my_instr.getParValues(['R', 'C'])
        """
        if type(parNames) == list:
            parValues = {}
            for par in parNames:
                par = sp.Symbol(str(par))
                for key in self.parDefs.keys():
                    if par == key:
                        if numeric == True:
                            parValues[par] = fullSubs(self.parDefs[key], self.parDefs)
                        else:
                           parValues[par] = self.parDefs[key]          
            return parValues
        parNames = sp.Symbol(str(parNames))
        try:
            if numeric:
                parValue = sp.N(fullSubs(self.parDefs[parNames], self.parDefs))
            else:
                parValue = self.parDefs[parNames]
        except:
            print "Error: parameter '%s' has not been defined."%(str(parNames))
            parValue = None
        return parValue

    def updateParams(self):
        """
        Updates self.params (list with undefined parameters) after modification 
        of parameter definitions in self.parDefs.
            
            return: None
        """    
        self.params =[]
        # Get all the parameters used in element values
        for elmt in self.elements.keys():
            for par in self.elements[elmt].params.keys():
                try:
                    self.params += list(self.elements[elmt].params[par].atoms(sp.Symbol))
                except:
                    pass
        # Get all the parameters used in parameter definitions
        for par in self.parDefs.keys():
            try:
                self.params += list(self.parDefs[par].atoms(sp.Symbol))
            except:
                pass
        # Remove duplicates
        self.params = list(set(self.params))
        undefined = []
        # If these parameters are not found in parDefs.keys, they are undefined.
        for par in self.params:
            if par != ini.Laplace and par != ini.frequency and par not in self.parDefs.keys():
                undefined.append(par)
            else:
                self.params.remove(par)
        self.params = undefined
        return
        
    def updateMdata(self):
        """
        Updates data for building matrices: self.depVars and self.varIndex.
        
        self.depVars    : vector with dependent variables
        self.varIndex   : dict with key-value pairs:
            key (str)   : name of the dependent variable
            value (int) : row position in the matrices before removing
                          the row and column that corresponds with node '0'.
        """
        self.depVars = []
        self.varIndex = {}
        varIndexPos = 0
        for elmt in self.elements.keys():
            for i in range(len(MODELS[self.elements[elmt].model].depVars)):
                depVar = MODELS[self.elements[elmt].model].depVars[i]
                self.depVars.append(depVar + '_' + elmt)
                self.varIndex[depVar + '_' + elmt] = varIndexPos
                varIndexPos += 1
        for i in range(len(self.nodes)):
            self.depVars.append('V_' + self.nodes[i])
            self.varIndex[self.nodes[i]] = varIndexPos
            varIndexPos += 1
        return

class element(object):
    """
    Prototype circuit element object. It has the following attributes:
        

    refDes     = ''    # Element reference designator (refdes)
    type       = ''    # First letter of refdes
    nodes      = []    # Node list
    refs       = []    # Reference list
    params     = {}    # Dictionary with model parameters
                       #   key   : model parameter name
                       #   value : parameter value or 
                       #           expression; value = [numer, denom] 
                       #           if Laplace rational
    model      = ''    # Model for this element
            
    """
    def __init__(self):
        self.refDes     = ''    # Element reference designator (refdes)
        self.type       = ''    # First letter of refdes
        self.nodes      = []    # Node list
        self.refs       = []    # Reference list
        self.params     = {}    # Dictionary with model parameters
                                #   key   : model parameter name
                                #   value : parameter value or 
                                #           expression; value = [numer, denom] 
                                #           if Laplace rational
        self.model      = ''    # Model for this element
        
class device(object):
    """
    Prototype for devices that can be used in SLiCAP. It has the following 
    attributes:
        
    ID     = ''        # ID of the device, e.g. 'V' for voltage source
    nNodes     = 0     # Number of nodes of the device
    nRefs      = 0     # Number of IDs of referenced devices
    value      = True  # True if model or value is required
    models     = []    # list with valid models for the device. 
                       # Model names refer to model.name of a model
    """
    def __init__(self):
        self.ID     = ''        # ID of the device, e.g. 'V' for voltage source
        self.nNodes     = 0     # Number of nodes of the device
        self.nRefs      = 0     # Number of IDs of referenced devices
        self.value      = True  # True if model or value is required
        self.models     = []    # list with valid models for the device. 
                                # Model names refer to model.name of a model
        
class model(object):
    """
    # Protpotype for element models that can be used in SLiCAP. It has the 
    following attributes:
        
    name       = ''    # Model name
    stamp      = True  # True if model has associated matrix stamp, 
                       # False if it requires expansion
    depVars    = []    # Namens of dependent vars. in matrix stamp
    params     = {}    # Dictionary with model parameters
                       #   key   : model parameter name
                       #   value : True: if Laplace is allowed in the
                       #           expression for this parameter,
                       #           else: False
    """
    def __init__(self):
        self.name       = ''    # Model name
        self.stamp      = True  # True if model has associated matrix stamp, 
                                # False if it requires expansion
        self.depVars    = []    # Namens of dependent vars. in matrix stamp
        self.params     = {}    # Dictionary with model parameters
                                #   key   : model parameter name
                                #   value : True: if Laplace is allowed in the
                                #           expression for this parameter,
                                #           else: False

class modelDef(object):
    """
    Protpotype for model definitions that can be added to SLiCAP. It has the 
    following attributes:
        
    name       = ''    # Model name
    type       = ''    # Must be a built-in model type
    params     = {}    # Dictionary with model parameters
                       #   key   : model parameter name
                       #   value : value or expression 
    """
    def __init__(self):
        self.name       = ''    # Model name
        self.type       = ''    # Must be a built-in model type
        self.params     = {}    # Dictionary with model parameters
                                #   key   : model parameter name
                                #   value : value or expression 
                                
def initAll():
    """
    Initializes the models and the devices.
    """
    global MODELS, DEVICES

    # Generate the dictionary with SLiCAP models
    # Capacitor
    newModel                = model()
    newModel.name           = 'C'
    newModel.stamp          = True
    newModel.depVars        = []
    newModel.params         = {'value': False}
    MODELS[newModel.name]   = newModel
    # Diode
    newModel                = model()
    newModel.name           = 'D'
    newModel.stamp          = False
    newModel.params         = {'rs': False, 'cd': False, 'gd': False}
    MODELS[newModel.name]   = newModel
    # VCVS
    newModel                = model()
    newModel.name           = 'E'
    newModel.stamp          = True
    newModel.depVars        = ['I_o']
    newModel.params         = {'value': True}
    MODELS[newModel.name]   = newModel
    # VCVS with series impedance
    newModel                = model()
    newModel.name           = 'EZ'
    newModel.stamp          = True
    newModel.depVars        = ['I_o']
    newModel.params         = {'value': True, 'zo': True}
    MODELS[newModel.name]   = newModel
    # CCCS
    newModel                = model()
    newModel.name           = 'F'
    newModel.stamp          = True
    newModel.depVars        = ['I_i']
    newModel.params         = {'value': True}
    MODELS[newModel.name]   = newModel
    # VCCS
    newModel                = model()
    newModel.name           = 'G'
    newModel.stamp          = True
    newModel.depVars        = ['I_o']
    newModel.params         = {'value': True}
    MODELS[newModel.name]   = newModel
    # VCCS no Laplace
    newModel                = model()
    newModel.name           = 'g'
    newModel.stamp          = True
    newModel.depVars        = []
    newModel.params         = {'value': False}
    MODELS[newModel.name]   = newModel
    # CCVS
    newModel                = model()
    newModel.name           = 'H'
    newModel.stamp          = True
    newModel.depVars        = ['I_o', 'I_i']
    newModel.params         = {'value': True}
    MODELS[newModel.name]   = newModel
    # CCVS with source impedance
    newModel                = model()
    newModel.name           = 'HZ'
    newModel.stamp          = True
    newModel.depVars        = ['I_o', 'I_i']
    newModel.params         = {'value': True, 'zo': True}
    MODELS[newModel.name]   = newModel
    # Independent current source
    newModel                = model()
    newModel.name           = 'I'
    newModel.stamp          = True
    newModel.depVars        = []
    newModel.params         = {'value': True, 'dc': False, 'dcvar': False, 'noise': False}
    MODELS[newModel.name]   = newModel
    # JFET
    newModel                = model()
    newModel.name           = 'J'
    newModel.stamp          = False          
    newModel.params         = {'cgs': False, 'cdg': False, 'gm': False, 'go': False}
    MODELS[newModel.name]   = newModel
    # Coupling factor
    newModel                = model()
    newModel.name           = 'K'
    newModel.stamp          = True
    newModel.depVars        = []
    newModel.params         = {'value': False}
    MODELS[newModel.name]   = newModel
    # Inductor
    newModel                = model()
    newModel.name           = 'L'
    newModel.stamp          = True
    newModel.depVars        = ['I']
    newModel.params         = {'value': False}
    MODELS[newModel.name]   = newModel
    # MOSFET
    newModel                = model()
    newModel.name           = 'M'
    newModel.stamp          = False          
    newModel.params         = {'cgs': False, 'cdg': False, 'cdb': False, 'csb': False, 'cgb': False, 'gm': False, 'gb': False, 'go': False}
    MODELS[newModel.name]   = newModel
    # MOS differential pair
    newModel                = model()
    newModel.name           = 'MD'
    newModel.stamp          = False          
    newModel.params         = {'cgg': False, 'cdg': False, 'cdd': False, 'gm': False, 'go': False}
    MODELS[newModel.name]   = newModel
    # Nullor
    newModel                = model()
    newModel.name           = 'N'
    newModel.stamp          = True
    newModel.depVars        = ['I_o']
    newModel.params         = {}
    MODELS[newModel.name]   = newModel
    # Current feedback operational amplifier
    newModel                = model()
    newModel.name           = 'OC'
    newModel.stamp          = False          
    newModel.params         = {'cp': False, 'gp': False, 'cpn': False, 'gpn': False, 'gm': False, 'zt': True, 'zo': True}
    MODELS[newModel.name]   = newModel
    # Voltage feedback operational amplifier
    newModel                = model()
    newModel.name           = 'OV'
    newModel.stamp          = False          
    newModel.params         = {'cd': False, 'cc': False, 'gd': False, 'gc': False, 'av': True, 'zo': True}
    MODELS[newModel.name]   = newModel
    # Vertical BJT
    newModel                = model()
    newModel.name           = 'QV'
    newModel.stamp          = False          
    newModel.params         = {'cpi': False, 'cbc': False, 'cbx': False, 'cs': False, 'gpi': False, 'gm': False, 'gbc': False, 'go': False, 'rb': False}
    MODELS[newModel.name]   = newModel
    # Lateral BJT
    newModel                = model()
    newModel.name           = 'QL'
    newModel.stamp          = False          
    newModel.params         = {'cpi': False, 'cbc': False, 'cbx': False, 'cs': False, 'gpi': False, 'gm': False, 'gbc': False, 'go': False, 'rb': False}
    MODELS[newModel.name]   = newModel
    # BJT differential pair
    newModel                = model()
    newModel.name           = 'QD'
    newModel.stamp          = False          
    newModel.params         = {'cbb': False, 'cbc': False, 'gbb': False, 'gm': False, 'go': False, 'gbc': False}
    MODELS[newModel.name]   = newModel
    # Resistor (resistance cannot be zero)
    newModel                = model()
    newModel.name           = 'R'
    newModel.stamp          = True
    newModel.depVars        = []
    newModel.params         = {'value': False}
    MODELS[newModel.name]   = newModel
    # Resistor (resistance can be zero)
    newModel                = model()
    newModel.name           = 'r'
    newModel.stamp          = True
    newModel.depVars        = ['I']
    newModel.params         = {'value': False, 'dcvar': False, 'noise': False}
    MODELS[newModel.name]   = newModel
    # Ideal transformer
    newModel                = model()
    newModel.name           = 'T'
    newModel.stamp          = True
    newModel.depVars        = ['I_o']
    newModel.params         = {'value': False}
    MODELS[newModel.name]   = newModel
    # Independent voltage source
    newModel                = model()
    newModel.name           = 'V'
    newModel.stamp          = True
    newModel.depVars        = ['I']
    newModel.params         = {'value': True, 'dc': False, 'dcvar': False, 'noise': False}
    MODELS[newModel.name]   = newModel
    # Gyrator
    newModel                = model()
    newModel.name           = 'W'
    newModel.stamp          = True
    newModel.depVars        = []
    newModel.params         = {'value': False}
    MODELS[newModel.name]   = newModel
    
    # Generate the dictionary with SLiCAP devices
    # Capacitor
    newDev                  = device()
    newDev.ID               = 'C'
    newDev.nNodes           = 2
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['C']
    DEVICES[newDev.ID]  = newDev
    # Diode
    newDev                  = device()
    newDev.ID               = 'D'
    newDev.nNodes           = 2
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['D']
    DEVICES[newDev.ID]  = newDev
    # VCVS
    newDev                  = device()
    newDev.ID               = 'E'
    newDev.nNodes           = 4
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['E', 'EZ']
    DEVICES[newDev.ID]  = newDev
    # CCCS
    newDev                  = device()
    newDev.ID               = 'F'
    newDev.nNodes           = 4 # 4 if independent input voltage source
    newDev.nRefs            = 0 # 0 if independent input voltage source
    newDev.value            = True
    newDev.models           = ['F']
    DEVICES[newDev.ID]  = newDev
    # VCCS
    newDev                  = device()
    newDev.ID               = 'G'
    newDev.nNodes           = 4
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['G', 'g']
    DEVICES[newDev.ID]  = newDev
    # CCVS
    newDev                  = device()
    newDev.ID               = 'H'
    newDev.nNodes           = 4 # 4 if independent input voltage source
    newDev.nRefs            = 0 # 4 if independent input voltage source
    newDev.value            = True
    newDev.models           = ['H', 'HZ']
    DEVICES[newDev.ID]  = newDev
    # Independent current source
    newDev                  = device()
    newDev.ID               = 'I'
    newDev.nNodes           = 2
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['I']
    DEVICES[newDev.ID]  = newDev
    # JFET
    newDev                  = device()
    newDev.ID               = 'J'
    newDev.nNodes           = 3
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['J']
    DEVICES[newDev.ID]  = newDev
    # Coupling factor
    newDev                  = device()
    newDev.ID               = 'K'
    newDev.nNodes           = 0
    newDev.nRefs            = 2
    newDev.value            = True
    newDev.models           = ['K']
    DEVICES[newDev.ID]  = newDev
    # Inductor
    newDev                  = device()
    newDev.ID               = 'L'
    newDev.nNodes           = 2
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['L']
    DEVICES[newDev.ID]  = newDev
    # MOSFET
    newDev                  = device()
    newDev.ID               = 'M'
    newDev.nNodes           = 4
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['M', 'MD']
    DEVICES[newDev.ID]  = newDev
    # Nullor
    newDev                  = device()
    newDev.ID               = 'N'
    newDev.nNodes           = 4
    newDev.nRefs            = 0
    newDev.value            = False
    newDev.models           = ['N']
    DEVICES[newDev.ID]  = newDev
    # Operational amplifier
    newDev                  = device()
    newDev.ID               = 'O'
    newDev.nNodes           = 4
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['OC', 'OV']
    DEVICES[newDev.ID]  = newDev
    # BJT
    newDev                  = device()
    newDev.ID               = 'Q'
    newDev.nNodes           = 4
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['QV', 'QD', 'QL']
    DEVICES[newDev.ID]  = newDev
    # Resistor
    newDev                  = device()
    newDev.ID               = 'R'
    newDev.nNodes           = 2
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['R', 'r']
    DEVICES[newDev.ID]  = newDev
    # Ideal transformer
    newDev                  = device()
    newDev.ID               = 'T'
    newDev.nNodes           = 4
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['T']
    DEVICES[newDev.ID]  = newDev
    # Independent voltage source
    newDev                  = device()
    newDev.ID               = 'V'
    newDev.nNodes           = 2
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['V']
    DEVICES[newDev.ID]  = newDev
    # Gyrator
    newDev                  = device()
    newDev.ID               = 'W'
    newDev.nNodes           = 4
    newDev.nRefs            = 0
    newDev.value            = True
    newDev.models           = ['W']
    DEVICES[newDev.ID]  = newDev
    # Sub circuit
    newDev                  = device()
    newDev.ID               = 'X'
    newDev.nNodes           = -1   # More than two nodes!
    newDev.nRefs            = 0
    newDev.value            = None # Only model name
    newDev.models           = []   # No models
    DEVICES[newDev.ID]  = newDev
    return

initAll() # Initialize all models, devices, etc.

#### Return structure for instruction
        
class allResults(object):
    """
    Return  structure for results, has attributes for all data types and
    instruction data. It has the following attributes:
    
    # Instruction results:
    
    DCvalue     = []   # Zero-frequency value in case of 
                            # dataType 'pz'
    poles       = []   # Complex frequencies in [rad/s] or [Hz]
    zeros       = []   # Complex frequencies in [rad/s] or [Hz]
    svarTerms   = {}   # Dict with lists with source variances
    ivarTerms   = {}   # Dict with lists with contributions to 
                            # source-referred variance
    ovarTerms   = {}   # Dict with lists with contributions to 
                            # detector-referred variance
    ivar        = []   # Total source-referred variance
    ovar        = []   # Total detector-referred variance
    dcSolve     = []   # DC solution of the network
    dc          = []   # DC solution at the detector
    snoiseTerms = {}   # Dict with lists with source noise spectra
    inoiseTerms = {}   # Dict with lists with contributions
                            # to source-referred noise
    onoiseTerms = {}   # Dict with lists with contributions
                            # to detector-referred noise
    inoise      = []   # Total source-referred noise spectral density
    onoise      = []   # Total detector-referred noise spectral 
    Iv          = None # Vector with independent variables
    M           = None # MNA matrix
    Dv          = None # Vector with dependent variables
    denom       = []   # Laplace poly of denominator
    numer       = []   # Laplace poly of numerator
    laplace     = []   # Laplace transfer functions
    solve       = []   # Laplace solutions of the network
    time        = []   # Time-domain responses
    impulse     = []   # Unit impulse responses
    stepResp    = []   # Unit step responses
    
    # instruction settings:
    
    simType     = None # Simulation type: 'symbolic' or 'numeric'
    gainType    = None # Gain type  : 'gain', 'asymptotic', 'loopgain', 'servo'
                       #              'direct', or 'vi'
    dataType    = None # Data type  : 'dc', 'dcsolve', 'dcvar', 'denom', 
                                      'impulse', 'laplace', 'matrix', 'noise',
                                      'numer', 'poles', 'pz', 'solve', 'step', 
                                      'time','zeros' or 'param'
    sweepVar    = None # Sweep parameter for data type 'param'
    step        = None # True       : enables parameter stepping
    stepVar     = None # Step variable for step types 'lin', 'log' and 'list'
    stepVars    = None # List with step variables for 'array' type stepping
    stepMethod  = None # Step method: 'lin', 'log', 'list', 'array'
    stepStart   = None # Start value for step methods 'lin' and 'log'
    stepStop    = None # Stop value for step methods 'lin' and 'log'
    stepNum     = None # Number of steps for step methods 'lin' and 'log'
    stepList    = []   # List with values for step method 'list'
    stepArray   = []   # Array with values for step method array:
                       # Nested list: list[i] carries the values for the step 
                       # variable in stepVars[i]. The lists should have equal
                       # lengths.
    source      = None # Refdes of the source (independent v or i source)
    detector    = None # Names of one or two nodal voltages or names of one
                       # or two dependent currents (see detector specification)
    lgRef       = None # Refdes of controlled source that is assigned as loop
                       # gain reference
    circuit     = None # Circuit object used for this instruction
    parDefs     = None # Parameter definitions used for this instruction
    numeric     = None # Variable used during analysis an presentation of 
                       # analysis results
    errors      = 0    # Number of errors found in the definition of this 
                       # instruction
    detUnits    = None # Detector units 'V' or 'A' (automatically detected)
    srcUnits    = None # Source units 'V' or 'A' (automatically detected)
    detLabel    = None # Name to be used in expressions or plots
    """
    def __init__(self):
        self.DCvalue     = []   # Zero-frequency value in case of 
                                # dataType 'pz'
        self.poles       = []   # Complex frequencies in [rad/s] or [Hz]
        self.zeros       = []   # Complex frequencies in [rad/s] or [Hz]
        self.svarTerms   = {}   # Dict with lists with source variances
        self.ivarTerms   = {}   # Dict with lists with contributions to 
                                # source-referred variance
        self.ovarTerms   = {}   # Dict with lists with contributions to 
                                # detector-referred variance
        self.ivar        = []   # Total source-referred variance
        self.ovar        = []   # Total detector-referred variance
        self.dcSolve     = []   # DC solution of the network
        self.dc          = []   # DC solution at the detector
        self.snoiseTerms = {}   # Dict with lists with source noise spectra
        self.inoiseTerms = {}   # Dict with lists with contributions
                                # to source-referred noise
        self.onoiseTerms = {}   # Dict with lists with contributions
                                # to detector-referred noise
        self.inoise      = []   # Total source-referred noise spectral density
        self.onoise      = []   # Total detector-referred noise spectral 
        self.Iv          = None # Vector with independent variables
        self.M           = None # MNA matrix
        self.Dv          = None # Vector with dependent variables
        self.denom       = []   # Laplace poly of denominator
        self.numer       = []   # Laplace poly of numerator
        self.laplace     = []   # Laplace transfer functions
        self.solve       = []   # Laplace solutions of the network
        self.time        = []   # Time-domain responses
        self.impulse     = []   # Unit impulse responses
        self.stepResp    = []   # Unit step responses
        self.params      = {}   # Results of parameter sweep (dataType = 'param')
        # instruction settings
        self.simType     = None
        self.gainType    = None
        self.dataType    = None
        self.sweepVar    = None
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
        self.detUnits    = None
        self.srcUnits    = None
        self.detLabel    = None # Name to be used in expressions or plots
        
def makeDir(dirName):
    """
    Creates the directory 'dirName' if it does not yet exist.
    """
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    return

def copyNotOverwrite(src, dest):
    """
    Copies the file 'src' to 'dest' if the latter one does not exist.
    """
    if not os.path.exists(dest):
        cp(src, dest)
    return