#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLiCAP module with basic SLiCAP classes and functions.

Imported by the module **SLiCAPmatrices.py**.
"""

from dataclasses import dataclass, field

from SLiCAP.SLiCAPmath import *

# Globals used by this script and by SLiCAPyacc.py:

MODELS      = {}                # Dictionary with SLiCAP built-in models
                                #   key   : model name
                                #   value : associated model object
DEVICES     = {}                # Dictionary with SLiCAP built-in devices
                                #   key   : device name
                                #   value : associated device object
class circuit(object):
    """
    Prototype (sub)circuit object.
    """
    def __init__(self):
        """
        Initialization of the circuit object, see description above.
        """
        self.title      = None
        """
        Title (*str*) of the circuit. Defautls to None.
        """

        self.file       = None
        """
        Name (*str*) of the netlist file. Defaults to None.
        """

        self.subCKT     = False
        """
        (*bool*) True if the circuit is a sub circuit. Defaults to False.
        """

        self.elements   = {}
        """
        (*dict*) with key-value pairs:

        - key: Reference designator (*str*) of the element.
        - value: Element object (*SLiCAPprotos.element*)
        """

        self.nodes      = []
        """
        (*list*) with names (*str*) of circuit nodes.
        """

        self.params     = {}
        """
        - If SLiCAPcircuit.subCKT == True:

          (*dict*) with key-value pairs:

          - key: Name (*sympy.core.symbol.Symbol*) of a parameter that can be passed to the
            sub circuit.
          - value: Default value (*sympy object*, float, int) of the parameter.

        - Else:

          - (*list*) with names (*sympy.core.symbol.Symbol*) of undefined parameters.
        """

        self.parDefs    = {}
        """
        (*dict*) with key-value pairs:

        - key: Name (*sympy.core.symbol.Symbol*) of a circuit parameter.
        - value: Value (*sympy object*, float, int) of the parameter.
        """

        self.parUnits   = {}
        """
        (*dict*) with key-value pairs:

        - key: Name (*sympy.core.symbol.Symbol*) of a circuit parameter.
        - value: Units (*str*) of the parameter.
        """

        self.modelDefs  = {}
        """
        (*dict*) with key-value pairs:

        - key: Name (*sympy.core.symbol.Symbol*) of a model.
        - value: Associated model object (*SLiCAPprotos.model*).
        """
        self.circuits   = {}
        """
        (*dict*) with key-value pairs:

        - key: Name (*str*) of a subcircuit.
        - value: Associated circuit object (*SLiCAPprotos.circuit*).
        """

        self.errors     = 0
        """
        Number (*int*) of errors found during checking of the circuit.
        Defaults to 0.
        """

        self.libs       = []
        """
        (*list*) with names (*str*) of library files found in netlist lines
        starting with ',lib' or '.inc'.
        """

        self.indepVars  = []
        """
        (*list*) with reference designators (*str*) of independent variables:

        - independent voltage sources
        - independent current sources.
        """

        self.depVars    = []
        """
        (*list*) with names (*str*) of independent variables:

        - nodal voltages:

          A nodal voltage will be named as: 'V_<node name>'

        - branch currents. Branch current will be named ad follows:

          - Current through a two-terminal element:

            - Vxxx: 'I_Vxxx'
            - Rxxx with model 'r': 'I_Rxxx'
            - Lxxx: 'I_Lxxx'

          - Currents through the input port or the output port of controlled
            sources:

            - Exxx output port: 'Io_Exxx'
            - Fxxx input port: 'Ii_Fxxx'
            - Gxxx, model = 'G', output port: 'Io_Gxxx'
            - Hxxx, input port: 'Ii_Hxxx', output port: 'Io_xxx'
        """

        self.controlled = []
        """
        (*list*) with reference designators (*str*) of controlled sources.
        """

        self.varIndex   = {}
        """
        (*dict*) with key-value pairs:

        - key (*str*): node name or name of branch current.
        - value(*int*) : row position in the vector with independent variables,
          before elemination of the row anmd column associated with the
          reference node '0'.
        """

    def delPar(self, parName):
        """
        Deletes a parameter definition and updates the list
        **SLiCAPprotos.circuit.params** with names (*sympy.core.symbol.Symbol*) of
        undefined parameters.

        :param parName: Name of the parameter.
        :type parName: str, sympy.core.symbol.Symbol

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
        **SLiCAPprotos.circuit.params** with names (*sympy.Symbol*) of
        undefined parameters.

        :param parName: Name of the parameter.
        :type parName: str, sympy.Symbol

        :param parValue: Value of the parameter.
        :type parValue: str, sympy.Symbol, sympy.Expr, int, float

        :param units: Value of the parameter, defaults to None
        :type units: str, sympy.Symbol, sympy.Expr, int, float

        :Example:

        >>> # create my_circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_circuit = checkCircuit('myFirstRCnetwork.cir')
        >>> # Define the value of 'R' as 2000
        >>> my_circuit.defPar('R', '2k', )
        >>> # Or:
        >>> my_circuit.defPar('R', 2e3)
        """
        errors = 0
        try:
            eval(parName)
            errors += 1
            print("Error: Parameter name cannot be a number.")
        except BaseException:
            pass
        if errors == 0:
            parName = sp.Symbol(str(parName))
            parValue = checkExpression(parValue)
            self.parDefs[parName] = parValue
            if type(units) == str:
                # ToDo: checkUnits() calculate wir SI units.
                self.parUnits[parName] = units
            else:
                self.parUnits[parName] = ''
            self.updateParams()
        return

    def defPars(self, parDict):
        """
        Adds or modifies multiple parameter definitions and updates the list
        **circuit.params** with names (*sympy.Symbol*) of undefined parameters.

        :params parDict: Dictionary with key-value pairs:

                         - key: parName (*str, sympy.Symbol*): name of the
                           parameter.
                         - value: parValue (*str, float, int, sympy object*):
                           value or expression of the parameter.
        :type parDict:   dict

        :Example:

        >>> # Create my_circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_circuit = checkCircuit('myFirstRCnetwork.cir')
        >>> # Define the value of 'R' as 2000 and 'C' as 5e-12:
        >>> my_circuit.defPars({'R': '2k', 'C': '5p')
        """
        errors = 0
        if type(parDict) == dict:
            for key in list(parDict.keys()):
                try:
                    eval(key)
                    print("Error: parameter name cannot be a number.")
                    errors += 1
                except BaseException:
                    pass
                if errors == 0:
                    parName = sp.Symbol(str(key))
                    parValue = str(parDict[key])
                    parValue = checkExpression(parValue)
                    self.parDefs[parName] = parValue
                else:
                    print("Error: cannot define a number as parameter.")
        else:
            print("Error: expected a dict type argument.")
        self.updateParams()
        return

    def getParValue(self, parNames, numeric = False):
        """
        Returns the value or expression of one or more parameters.

        If numeric == True it will perform a full recursive substitution of
        all circuit parameter definitions.

        :param parNames: name(s) of the parameter(s)
        :type parNames: str, sympy.Symbol, list

        :return: If type(parNames) == list:

                 (*dict*) with key-value pairs:

                 - key (*sympy.Symbol*): name of the parameter

                 - value (*int, float, sympy object*): value of the parameter

                 Else: value or expression (*int, float, sympy object*).

        :rtype: dict, float, int, sympy obj

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
                for key in list(self.parDefs.keys()):
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
        except BaseException:
            exc_type, value, exc_traceback = sys.exc_info()
            print('\n', value)
            print("Error: parameter '{0}' has not been defined.".format(str(parNames)))
            parValue = None
        return parValue

    def updateParams(self):
        """
        Updates self.params (list with undefined parameters) after modification
        of parameter definitions in self.parDefs.
        """
        self.params =[]
        # Get all the parameters used in element values
        for elmt in list(self.elements.keys()):
            for par in list(self.elements[elmt].params.keys()):
                try:
                    self.params += list(self.elements[elmt].params[par].atoms(sp.Symbol))
                except BaseException:
                    pass
        # Get all the parameters used in parameter definitions
        for par in list(self.parDefs.keys()):
            try:
                self.params += list(self.parDefs[par].atoms(sp.Symbol))
            except BaseException:
                pass
        # Remove duplicates
        self.params = list(set(self.params))
        undefined = []
        # If these parameters are not found in parDefs.keys, they are undefined.
        for par in self.params:
            if par != ini.Laplace and par != ini.frequency and par not in list(self.parDefs.keys()):
                undefined.append(par)
        self.params = undefined
        return

    def getElementValue(self, elementID, param, numeric):
        """
        Returns the value or expression of one or more circuit elements.

        If instruction.numeric == True it will perform a full recursive
        substitution of all circuit parameter definitions.

        This method is called by instruction.circuit.getElementValue() with
        keyword arg numeric = True if instruction.simType is set to 'numeric'.

        :param elementID: name(s) of the element(s)
        :type elementID: str, list

        :param param: name of the parameter (equal for all elements):

                      - 'value': Laplace value
                      - 'dc': DC value (independent sources only)
                      - 'noise': Noise spectral density (independent sources only)
                      - 'dcvar': DC variance (independent sources only)

        :type param: str

        :return: if type(parNames) == list:

                 return value = dict with key-value pairs: key (*sympy.core.symbol.Symbol*):
                 name of the parameter, value (*int, float, sympy expression*):
                 value of the parameter

                 else:
                 value or expression

        :rtype: dict, float, int, sympy.Expr

        :Example:

        >>> # Create an instance if a SLiCAP instruction
        >>> my_instr = instruction()
        >>> # Create my_instr.circuit from the netlist 'myFirstRCnetwork.cir'
        >>> my_instr.setCircuit('myFirstRCnetwork.cir')
        >>> # Obtain the numeric value of 'R1' and 'C1':
        >>> my_instr.symType = 'numeric'
        >>> print my_instr.getElementValue(['R1', 'C1'])
        {'C1': 5.0e-7/pi, 'R1': 1000.00000000000}
        """
        if type(elementID) == list:
            elementValues = {}
            for elID in elementID:
                if elID in list(self.elements.keys()):
                    if param in list(self.elements[elID].params.keys()):
                        value = self.elements[elID].params[param]
                        if numeric:
                            value = fullSubs(value, self.parDefs)
                        elementValues[elID] = value
                    else:
                        print("Error: Parameter '{0}' undefined for element '{1}'.".format(param, elID))
                else:
                    print("Error: Unknown circuit element '{0}'.".format(elID))
        else:
            elementValues = None
            if elementID in list(self.elements.keys()):
                if param in list(self.elements[elementID].params.keys()):
                    value = self.elements[elementID].params[param]
                    if numeric:
                        value = fullSubs(value, self.parDefs)
                    elementValues = value
                else:
                    print("Error: Parameter '{0}' undefined for element '{1}'.".format(param, elementID))
            else:
                print("Error: Unknown circuit element '{0}'.".format(elementID))
        return elementValues

class element(object):
    """
    Prototype circuit element object.
    """
    def __init__(self):
        self.refDes     = ''
        """
        Element reference designator (*str*), defaults to ''.
        """

        self.type       = ''
        """
        Element type: First letter of refdes (*str*).
        """

        self.nodes      = []
        """
        (*list*) with names (*str*) of the nodes to which the element is
        connected.
        """

        self.refs       = []
        """
        (*list*) with reference designators of elements (*str*) that are
        referenced to by the element.
        """

        self.params     = {}
        """
        (*dict*) with key-value pairs:

        - key (*sympy.core.symbol.Symbol*): Name of an element parameter.
        - value (*sympy object*, float, int): Value of the parameter.
        """
        self.model      = ''
        """
        Name (*str*) of the model of the element.
        """


@dataclass(frozen=True)
class Device:
    """
    Prototype for devices that can be used in SLiCAP.

    ID: ID of the device, e.g. 'V' for voltage source. Defaults to ''.
    nNodes: Number (*int*) of nodes of the device. Defaults to 0.
    nRefs: Number (*int*) of reference designators of referenced devices.
    value: (*bool*) True if model or value is required. Defaults to True.
    models: (*list*) with names (*str*) of valid models for the device.
    """

    ID: str = ""
    nNodes: int = 0
    nRefs: int = 0
    value: bool = True
    models: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Model:
    """
    Prototype for element models that can be used in SLiCAP.

    name: Name (*str*) of the model.
    stamp: (*bool*) True if model has associated matrix stamp,
        False if it requires expansion.
    depVars: (*list*) with names of dependent variables to be used in the
        vector with dependent variables.
    params: (*dict*) with key-value pairs:
    - key (*str*): Name  of the model parameter.
    - value (*bool*): True if the Laplace variable is allowed in the
          expression for this parameter, else False.
    """

    name: str = ""
    stamp: bool = True
    depVars: list[str] = field(default_factory=list)
    params: dict[str, bool] = field(default_factory=dict)


class modelDef(object):
    """
    Protpotype for model definitions that can be added to SLiCAP.
    """
    def __init__(self):
        self.name       = ''
        """
        Name (*str*) of the model.
        """
        self.type       = ''
        """
        Name (*str*) of the built-in model type that should be used for this
        model.
        """

        self.params     = {}
        """
        (*dict*) with key-value pairs:

        - key (*str*): Model parameter name
        - value (*sympy object*, float, int): Value or expression
        """

def initAll():
    """
    Creates the SLiCAP built-in models and devices.
    """
    global MODELS, DEVICES

    # Generate the dictionary with SLiCAP models
    # Capacitor
    MODELS["C"] = Model("C", True, [], {"value": False, "vinit": False})

    # Diode
    MODELS["D"] = Model("D", False, [], {"rs": False, "cd": False, "gd": False})

    # VCVS
    MODELS["E"] = Model("E", True, ["Io"], {"value": True})

    # VCVS with series impedance
    MODELS["EZ"] = Model("EZ", True, ["Io"], {"value": True, "zo": True})

    # CCCS
    MODELS["F"] = Model("F", True, ["Ii"], {"value": True})

    # VCCS
    MODELS["G"] = Model("G", True, ["Io"], {"value": True})

    # VCCS no Laplace
    MODELS["g"] = Model("g", True, [], {"value": False})

    # CCVS
    MODELS["H"] = Model("H", True, ["Io", "Ii"], {"value": True})

    # CCVS with source impedance
    MODELS["HZ"] = Model("HZ", True, ["Io", "Ii"], {"value": True, "zo": True})

    # Independent current source
    MODELS["I"] = Model(
        "I", True, [], {"value": True, "dc": False, "dcvar": False, "noise": False}
    )

    # JFET
    MODELS["J"] = Model(
        "J", False, [], {"cgs": False, "cdg": False, "gm": False, "go": False}
    )

    # Coupling factor
    MODELS["K"] = Model("K", True, [], {"value": False})

    # Inductor
    MODELS["L"] = Model("L", True, ["I"], {"value": False, "iinit": False})

    # MOSFET
    MODELS["M"] = Model(
        "M",
        False,
        [],
        {
            "cgs": False,
            "cdg": False,
            "cdb": False,
            "csb": False,
            "cgb": False,
            "gm": False,
            "gb": False,
            "go": False,
        },
    )

    # MOS differential pair
    MODELS["MD"] = Model(
        "MD",
        False,
        [],
        {
            "cgg": False,
            "cdg": False,
            "cdd": False,
            "gm": False,
            "go": False,
        },
    )

    # Nullor
    MODELS["N"] = Model("N", True, ["Io"], {})

    # Current feedback operational amplifier
    MODELS["OC"] = Model(
        "OC",
        False,
        [],
        {
            "cp": False,
            "gp": False,
            "cpn": False,
            "gpn": False,
            "gm": False,
            "zt": True,
            "zo": True,
        },
    )

    # Voltage feedback operational amplifier
    MODELS["OV"] = Model(
        "OV",
        False,
        [],
        {
            "cd": False,
            "cc": False,
            "gd": False,
            "gc": False,
            "av": True,
            "zo": True,
        },
    )

    # Vertical BJT
    MODELS["QV"] = Model(
        "QV",
        False,
        [],
        {
            "cpi": False,
            "cbc": False,
            "cbx": False,
            "cs": False,
            "gpi": False,
            "gm": False,
            "gbc": False,
            "go": False,
            "rb": False,
        },
    )

    # Lateral BJT
    MODELS["QL"] = Model(
        "QL",
        False,
        [],
        {
            "cpi": False,
            "cbc": False,
            "cbx": False,
            "cs": False,
            "gpi": False,
            "gm": False,
            "gbc": False,
            "go": False,
            "rb": False,
        },
    )

    # BJT differential pair
    MODELS["QD"] = Model(
        "QD",
        False,
        [],
        {
            "cbb": False,
            "cbc": False,
            "gbb": False,
            "gm": False,
            "gcc": False,
            "gbc": False,
            "rb": False,
        },
    )

    # Resistor (resistance cannot be zero)
    MODELS["R"] = Model(
        "R",
        True,
        [],
        {
            "value": False,
            "dcvar": False,
            "noisetemp": False,
            "noiseflow": False,
        },
    )

    # Resistor (resistance can be zero)
    MODELS["r"] = Model(
        "r",
        True,
        ["I"],
        {
            "value": False,
            "dcvar": False,
            "noisetemp": False,
            "noiseflow": False,
        },
    )

    # Ideal transformer
    MODELS["T"] = Model("T", True, ["Io"], {"value": False})

    # Independent voltage source
    MODELS["V"] = Model(
        "V", True, ["I"], {"value": True, "dc": False, "dcvar": False, "noise": False}
    )

    # Gyrator
    MODELS["W"] = Model("W", True, [], {"value": False})

    # Generate the dictionary with SLiCAP devices
    # Capacitor
    DEVICES["C"] = Device("C", 2, 0, True, ["C"])

    # Diode
    DEVICES["D"] = Device("D", 2, 0, True, ["D"])

    # VCVS
    DEVICES["E"] = Device("E", 4, 0, True, ["E", "EZ"])

    # CCCS
    DEVICES["F"] = Device("F", 4, 0, True, ["F"])

    # VCCS
    DEVICES["G"] = Device("G", 4, 0, True, ["G", "g"])

    # CCVS
    DEVICES["H"] = Device("H", 4, 0, True, ["H", "HZ"])

    # Independent current source
    DEVICES["I"] = Device("I", 2, 0, True, ["I"])

    # JFET
    DEVICES["J"] = Device("J", 3, 0, True, ["J"])

    # Coupling factor
    DEVICES["K"] = Device("K", 0, 2, True, ["K"])

    # Inductor
    DEVICES["L"] = Device("L", 2, 0, True, ["L"])

    # MOSFET
    DEVICES["M"] = Device("M", 4, 0, True, ["M", "MD"])

    # Nullor
    DEVICES["N"] = Device("N", 4, 0, False, ["N"])

    # Operational amplifier
    DEVICES["O"] = Device("O", 4, 0, True, ["OC", "OV"])

    # BJT
    DEVICES["Q"] = Device("Q", 4, 0, True, ["QV", "QD", "QL"])

    # Resistor
    DEVICES["R"] = Device("R", 2, 0, True, ["R", "r"])

    # Ideal transformer
    DEVICES["T"] = Device("T", 4, 0, True, ["T"])

    # Independent voltage source
    DEVICES["V"] = Device("V", 2, 0, True, ["V"])

    # Gyrator
    DEVICES["W"] = Device("W", 4, 0, True, ["W"])

    # Sub circuit
    DEVICES["X"] = Device("X", -1, 0, None, [])


class allResults(object):
    """
    Return  structure for results, has attributes with
    instruction data and execution results.
    """
    def __init__(self):
        self.DCvalue     = []
        """
        Zero-frequency value in case of dataType 'pz'.
        """
        self.poles       = []
        """
        Complex frequencies in [rad/s] or [Hz]
        """

        self.zeros       = []
        """
        Complex frequencies in [rad/s] or [Hz]
        """
        self.svarTerms   = {}
        """
        Dict with lists with source variances
        """

        self.ivarTerms   = {}
        """
        Dict with lists with contributions to source-referred variance.
        """

        self.ovarTerms   = {}
        """
        Dict with lists with contributions to detector-referred variance.
        """

        self.ivar        = []
        """
        Total source-referred variance.
        """

        self.ovar        = []
        """
        Total detector-referred variance.
        """

        self.solve       = []
        """
        Laplace solution of the network.
        """

        self.dcSolve     = []
        """
        DC solution of the network.
        """

        self.timeSolve   = []
        """
        Time-domain solution of the network.
        """

        self.dc          = []
        """
        DC solution at the detector.
        """

        self.snoiseTerms = {}
        """
        Dict with lists with source noise spectra.
        """

        self.inoiseTerms = {}
        """
        Dict with lists with contributions to source-referred noise.
        """
        self.onoiseTerms = {}
        """
        Dict with lists with contributions to detector-referred noise.
        """

        self.inoise      = []
        """
        Total source-referred noise spectral density.
        """

        self.onoise      = []
        """
        Total detector-referred noise spectral.
        """

        self.Iv          = None
        """
        Vector with independent variables.
        """

        self.M           = None
        """
        MNA matrix.
        """

        self.A           = None
        """
        Base conversion matrix.
        """

        self.Dv          = None
        """
        Vector with dependent variables.
        """

        self.denom       = []
        """
        Laplace poly of denominator.
        """

        self.numer       = []
        """
        Laplace poly of numerator.
        """

        self.laplace     = []
        """
        Laplace transfer functions.
        """

        self.time        = []
        """
        Time-domain responses.
        """

        self.impulse     = []
        """
        Unit impulse responses.
        """

        self.stepResp    = []
        """
        Unit step responses.
        """

        self.params      = {}
        """
        Results of parameter sweep (dataType = 'param').
        """

        # Instruction settings

        self.simType = 'numeric'
        """
        Defines the simulation gain type.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.gainType = None
        """
        Defines the simulation gain type.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.convType = None
        """
        Defines the circuit conversion type.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.dataType = None
        """
        Defines the simulation data type.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.step = None
        """
        Setting for parameter stepping.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.stepVar = None
        """
        Defines the step variable (*str*) for step types 'lin', 'log' and 'list'.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.stepVars = None
        """
        Defines the step variables for 'array' type parameter stepping.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.stepMethod = None
        """
        Step method for parameter stepping.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.stepStart = None
        """
        Start value for stepping methods 'lin' and 'log'.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.stepStop = None
        """
        Stop value for stepping methods 'lin' and 'log'.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.stepNum = None
        """
        Number of steps for step methods 'lin' and 'log'.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.stepList = []
        """
        List with values for step method 'list'.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction. This instance will be a deep copy.
        """

        self.stepArray = []
        """
        Array (*list of lists*) with values for step method array.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction. This instance will be a deep copy.
        """

        self.source = None
        """
        Refdes of the signal source (independent v or i source).

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.detector = None
        """
        Names of the positive and negative detector.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.lgRef = None
        """
        Refdes of the controlled source that is assigned as loop gain reference.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.circuit = None
        """
        Circuit (*SLiCAPprotos.circuit*) used for this instruction.

        Will be copied from **SLiCAPinstruction.instruction.circuit** at the
        start of the execution of the instruction. This instance will not be a
        deep copy.
        """

        self.numeric = None
        """
        Variable used during analysis an presentation of analysis results.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.errors = 0
        """
        Number of errors found in the definition of this instruction.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.detUnits = None
        """
        Detector units 'V' or 'A'.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.srcUnits = None
        """
        Source units 'V' or 'A'.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.detLabel = None
        """
        Name for the detector quantity to be used in expressions or plots.

        Will be generated by **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction.
        """

        self.label = ''
        """
        Label to be used in plots.
        """

        self.parDefs = None
        """
        Parameter definitions for the instruction.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction. This instance will be e deep copy.
        """
        self.pairedVars   = None
        """
        Extension of paired nodes and branches for base transformation of the circuit.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction. This instance will be e deep copy.
        """
        self.pairedCircuits = None
        """
        Identifiers of paired subcircuits for base transformation of the circuit.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction. This instance will be e deep copy.
        """
        self.removePairSubName = False
        """
        Setting for changing the parameter names of paired subcircuits.

        Will be copied from **SLiCAPinstruction.instruction** at the start of
        the execution of the instruction. This instance will be e deep copy.
        """

    def depVars(self):
        """
        Returns the list of detecors available AFTER execution of an instruction.
        """
        return [str(var) for var in self.Dv]

def makeDir(dirName):
    """
    Creates the directory 'dirName' if it does not yet exist.

    :param dirName: Name of the ditectory.
    :type dirName: str
    """

    if not os.path.exists(dirName):
        os.makedirs(dirName)
    return

def copyNotOverwrite(src, dest):
    """
    Copies the file 'src' to 'dest' if the latter one does not exist.

    :param src: Name of the source file.
    :type src: str

    :param dest: Name of the desitination file.
    :type dest: str
    """
    if not os.path.exists(dest):
        cp(src, dest)
    return

initAll() # Initialize all models, devices, etc.
