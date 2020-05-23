#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from SLiCAPlex import *

# Globals
HIERARCHY   = []                # Check list for hierarchical loops
CONSTANTS   = {}                # Dictionary with global parameters taken from
                                # the ini file
MODELS      = {}                # Dictionary with SLiCAP built-in models
                                #   key   : model name
                                #   value : associated model object
DEVICES     = {}                # Dictionary with SLiCAP built-in devices
                                #   key   : device name
                                #   value : associated device object
CONTROLLED  = ['E', 'F', 'G', 'H']  # Types of controlled sources
INDEPSCRCS  = ['I', 'V']            # Types of independent sources

class circuit(object):
    # Circuit object for main circuit and for sub circuits
    def __init__(self):
        self.title      = ''    # Title of (sub) circuit
        self.file       = []    # Name of the netlist file
        self.lexer      = None  # Tokenized input file
        self.subCKT     = False # True if sub circuit
        self.elements   = {}    # Dictionary withthe circuit's element  objects
                                #   key   : element refDes
                                #   value : associated element object
        self.nodes      = []    # Connecting nodes to parent circuit
        self.params     = {}    # Parameters tat can be be passed from parent
                                # circuit (sub circuit only)
                                #   key   : model parameter name
                                #   value : parameter value or expression 
        self.parDefs    = {}    # Dictionary with paremeter definitions
                                #   key   : model parameter name
                                #   value : parameter value or expression
        self.modelDefs  = {}    # Dictionary with model definitions found in 
                                # the circuit:
                                #   key   : model name
                                #   value : modelDef object
        self.circuits   = {}    # Dict with sub circuit definitions found in
                                # the netlist (before expansion)
                                #   key   : sub circuit name
                                #   value : circuit object
        self.errors     = 0     # Number of errors found during checking
        self.libs       = []    # List with library files
        self.indepVars  = []    # List with independent sources;
                                # can be used as signal source
        self.depVars    = []    # List with dependent variables;
                                # can be used as detector
        self.controlled = []    # List with controlles sources;
                                # can be used as loop gain reference
        self.varIndex   = {}    # Dictionary with index of node or dependent
                                # current (speeds up the building of the matrix)
                                #   key   : node name of current name
                                #   value : position in the vactor with
                                #           dependent variables
    
    def delPar(self, parName):
        # single params and multiple.
        self.updateParams()
        return
        
    def defPar(self, parName):
        # single params and multiple.
        self.updateParams()
        return
        
    def getParValue(self, parName):
        # single params and multiple.
        return
    
    def updateParams(self):
        """
        Updates self.params (undefined parameters) after modification of 
        parameter definitions in self.parDefs or in elements: 
        self.elements[<refDes>].params[<parName>].
        """    
        self.params =[]
        for elmt in self.elements.keys():
            for par in self.elements[elmt].params:
                try:
                    self.params += list(self.elements[elmt].params[par].free_symbols)
                except:
                    pass
        self.params = list(set(self.params))
        undefined = []
        for par in self.params:
            if par != LAPLACE and par != FREQUENCY and par != OMEGA and par not in self.parDefs.keys():
                self.append(par)
        self.params = undefined
    
class element(object):
    # Circuit element object
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
    # Prototype for devices that can be used in SLiCAP
    def __init__(self):
        self.ID     = ''        # ID of the device, e.g. 'V' for voltage source
        self.nNodes     = 0     # Number of nodes of the device
        self.nRefs      = 0     # Number of IDs of referenced devices
        self.value      = True  # True if model or value is required
        self.models     = []    # list with valid models for the device. 
                                # Model names refer to model.name of a model
        
class model(object):
    # Protpotype for element models that can be used in SLiCAP
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
    # Protpotype for models that can be added to SLiCAP
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
    newModel.depVars        = 1 # can be set to 2 if independent depVar is used
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

initAll()