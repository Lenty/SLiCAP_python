#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
SLiCAP netlist parser: functions for converting a netlist into a circuit object.

Tokenizes the netlist and creates a 'flattened' circuit object.

Imported by the module **SLiCAPexecute.py**.
"""

from SLiCAPhtml import *

# Composite tokens
NODES       = ['NODEID', 'ID', 'INT']
VALEXPR     = ['FLT', 'EXPR', 'SCI', 'INT']
TITLE       = ['ID', 'QSTRING', 'FNAME']

# Commands with identical action
INC         = ['INC', 'LIB']
END         = ['END', 'ENDS']

# Lists with constrolled and independent sources
CONTROLLED  = ['E', 'F', 'G', 'H']  # Controlled sources
INDEPSCRCS  = ['I', 'V']            # Independent sources

# list with (sub)circuit titles for checking hierarchy
CIRTITLES = []

LIB = circuit()

def checkCircuit(fileName):
    """
    Checks a netlist and converts it into a circuit object.
    
    :param fileName: Name of the netlist file, relative to the circuit directory.
    :type param: str
    :return: cir
    :rtype: SLiCAPprotos.circuit
    """
    # Create in instance of the ciruit object
    cir = circuit()
    cir.file = fileName
    # Be sure the libraries are compiled withou errors.
    if LIB.errors == 0:        
        # tokenize the file and store the tokens with the object.
        cir.lexer = tokenize(ini.circuitPath + fileName)
        # Parse the tokenized netlist
        cir = makeCircuit(cir)
        # If no errors are found, create the html index page for the circuit
        if cir.errors == 0:
            cir = updateCirData(cir)
            ini.htmlPrefix = ('-'.join(cir.title.split()) + '_')
            ini.htmlIndex = 'index.html'
            htmlPage(cir.title, index = True)
            if cir.errors != 0:
                print """Errors found during updating of circuit data from '%s'.
    Instructions with this circuit will not be executed."""%(cir.title)
            else:
                print "No errors found for circuit: '%s' from file: '%s'.\n"%(cir.title, fileName)
    else:
        print "Errors found in library. Circuit '%s' will not be ckecked."%(fileName)
    return cir

def makeCircuit(cir):
    """
    Creates a nested circuit object from the tokens in cir.lexer.
    
    Called by: **checkCircuit()**
    
    :param cir: Circuit object with lexer data in cir.lexer to which data will
                be added
    :type cir: SLiCAP.protos.circuit
    :return: cir: circuit object with all data of the 'flattened' circuit.
    :rtype: SLiCAPprotos.circuit
    """
    global CIRTITLES
    
    lines = cir.lexer.lexdata.splitlines()
    tok = cir.lexer.token()
    if tok and tok.type in TITLE and cir.subCKT==False:
        # In this case, we a dealing with the main circuit
        cir.title = tok.value
        if tok.type == 'QSTRING':
            # Remove the double quotes, this conflicts with HTML files
            cir.title = cir.title[1:-1]
        tok = lexer.token()
    elif cir.subCKT == True:
        # In this case, we a dealing with a sub circuit
        # The first token  must be the title
        if tok:
            while tok.type == 'PLUS':
                tok = cir.lexer.token()
                if not tok:
                    break
            if tok and tok.type in TITLE:
                cir.title = tok.value
                if tok.type == 'QSRTING':
                    # Remove the double quotes, this conflicts with HTML files
                    cir.title = cir.title[1:-1]
                if tok.value in CIRTITLES:
                    print "Error: circuit '%s' has already been defined."%(cir.title)
                    cir.errors += 1
            else:
                printError("Error: expected a circuit title.", 
                           lines[cir.lexer.lineno], find_column(tok))
                cir.errors += 1
        else:
            print "Missing circuit title."
            cir.errors += 1
        tok = cir.lexer.token()
        # The number of nodes needs to be detected automatically. This is as 
        # follows:
        # 1. If the line number of the next 'ID' token differs from the
        #    preceeding and there was no 'PLUS' token before it, then
        #    all preceeding 'ID' tokens were node fields and the last
        #    one is the identifier of a new device.
        # 2. If a 'PARDEF' token is found before the ID token on a new
        #    line, all preceeding ID tokens were nodes.
        newLine = False   
        lineNo = cir.lexer.lineno
        newLineNo = lineNo
        nodesModel = []
        while (tok.type in NODES or tok.type == 'PLUS') and newLine == False:
            if tok.type == 'PLUS':
                pass
            else:
                cir.nodes.append(tok.value)
            lineNo = newLineNo
            tok = cir.lexer.token()
            if not tok:
                break
            newLineNo = cir.lexer.lineno
            if newLineNo != lineNo and tok.type != 'PLUS':
                newLine = True
        # Parameters that can be passed to the circuit have 'PARDEF' tokens
        while tok.type == 'PARDEF' or tok.type == 'PLUS':
            if tok.type == 'PLUS':
                pass
            else:
                cir.params[tok.value[0]]=tok.value[1]
            tok = cir.lexer.token()
            if not tok:
                break
        # Here we have the first token of the second line of the sub circuit
        # definition. Further checking is identical as with the main circuit,
        # except for a '.ends' command token at the end.
        #print tok,
    else:
        printError("Error: expected a circuit title.", 
                   lines[cir.lexer.lineno], find_column(tok))
        tok = cir.lexer.token()
        # Here we have the first token of the second line of the circuit 
        # definition. Further checking is identical as with the sub circuit,
        # except for a '.end' command token at the end.
    #print cir.title, cir.nodes, tok
    while tok:
        if tok.type == 'ID' and tok.value[0].upper() in DEVICES.keys():
            # We have an element definition line, the number of required fields
            # for nodes, references and value is taken from the prototype:
            # DEVICES
            if tok.value not in cir.elements.keys():
                newElement = element()
                newElement.refDes = tok.value
                newElement.type = tok.value[0].upper()
                nNodes = DEVICES[newElement.type].nNodes
                nRefs  = DEVICES[newElement.type].nRefs
                value  = DEVICES[newElement.type].value
                if nNodes != -1:
                    for i in range(nNodes):
                        tok = cir.lexer.token()
                        if tok:
                            while tok.type == 'PLUS':
                                tok = cir.lexer.token()
                                if not tok:
                                    break
                            if tok.type in NODES:
                                newElement.nodes.append(tok.value)
                            else:
                                # Wrong token!
                                printError("Error: expected a nodeID", 
                                           lines[cir.lexer.lineno], find_column(tok))
                                cir.errors += 1
                        else:
                            # Wrong token!
                            print "Error: missing node."
                            cir.errors += 1
                else:
                    # nNodes == -1, means we have a sub circuit, the number of
                    # nodes needs to be detected automatically. This is as follows:
                    # 1. If the line number of the next 'ID' token differs from the
                    #    preceeding and there was no 'PLUS' token before it, then
                    #    all preceeding 'ID' tokens were node fields and the last
                    #    one is the identifier of a new device.
                    # 2. If a 'PARDEF' token is found before the ID token on a new
                    #    line, the last 'ID' token is not a node but a model field.
                    newLine = False   
                    lineNo = cir.lexer.lineno
                    nodesModel = []
                    while tok.type != 'PARDEF' and newLine == False:
                        tok = cir.lexer.token()
                        if not tok:
                            break
                        newLineNo = cir.lexer.lineno
                        if newLineNo != lineNo and tok.type != 'PLUS':
                            newLine = True
                        else:
                            if tok.type in NODES:
                                nodesModel.append(tok.value)
                                nNodes += 1
                            else:
                                pass
                        newLineNo = lineNo
                    newElement.nodes = nodesModel[0:-1]
                    newElement.model = nodesModel[-1]                    
                    if nNodes < 2:
                        # We need at least two nodes per device!"
                        printError("Error: expected at least two nodes.", 
                                   lines[cir.lexer.lineno], find_column(tok))   
                        cir.errors += 1 
                for i in range(nRefs):
                    tok = cir.lexer.token()
                    if tok:
                        if tok.type == 'ID':
                            newElement.refs.append(tok.value)
                        elif tok.type == 'PLUS':
                            # Decrease counter i
                            i -= 1
                        else:
                            # Wrong token!
                            printError("Error: expected an element ID.", 
                                       lines[cir.lexer.lineno], find_column(tok))
                            cir.errors += 1
                if value:
                    tok = cir.lexer.token()
                    if tok:
                        while tok.type == 'PLUS':
                            tok = cir.lexer.token()
                            if not tok:
                                break
                        if tok.type in VALEXPR:
                            if tok.type == 'INT':
                                # Integers are still str and need to be converted
                                tok.value = int(tok.value)
                            newElement.params['value'] = tok.value
                            # If this field was numeric, we are missing the
                            # model and use the default model for this device
                            newElement.model = DEVICES[newElement.type].models[0]
                            tok = cir.lexer.token()
                        elif tok.type == 'ID':  
                            # If this token is 'ID' we have a model name 
                            newElement.model = tok.value 
                            if newElement.model in MODELS.keys():
                                validParams = MODELS[newElement.model].params.keys()                            
                            tok = cir.lexer.token()
                            while tok.type == 'PARDEF' or tok.type == 'PLUS':
                                if tok.type == 'PLUS':
                                    pass
                                elif tok.value[0] not in newElement.params.keys():
                                    if newElement.model not in MODELS.keys():
                                        newElement.params[tok.value[0]]=tok.value[1]
                                    else:
                                        newParam = tok.value[0]
                                        if newParam not in validParams:
                                            printError("Error: unknown parameter.", 
                                                       lines[cir.lexer.lineno], find_column(tok))
                                            cir.errors += 1
                                        else:
                                            newElement.params[tok.value[0]]=tok.value[1]
                                else:   
                                    # Parameter that must be passed to the 
                                    # element has already been pased to it!
                                    printError("Error: parameter has already been defined.", 
                                               lines[cir.lexer.lineno], find_column(tok))
                                    cir.errors += 1
                                tok = cir.lexer.token()
                                if not tok:
                                    break
                    else:
                        # Wrong token at this position!
                        printError("Error: expected a model, a value or an expression", 
                                   lines[cir.lexer.lineno], find_column(tok))
                        cir.errors += 1
                elif value == False:
                    newElement.model = DEVICES[newElement.type].models[0]
                    tok = cir.lexer.token()
                elif newElement.type == 'X':
                    # For sub circuits we already have the model and value=False
                    # Here we will process the parameters of the sub circuit
                    while (tok.type == 'PARDEF' or tok.type == 'PLUS'):
                        if tok.type == 'PLUS':
                            pass
                        elif tok.value[0] not in newElement.params.keys():
                            newElement.params[tok.value[0]]=tok.value[1]
                        else:
                            # Parameter that must be passed to the circuit has
                            # already been pased to it!
                            printError("Error: parameter has already been defined.", 
                                       lines[cir.lexer.lineno], find_column(tok))
                            cir.errors += 1
                        tok = cir.lexer.token()
                        if not tok:
                            break
                else:
                    # No value required, get the next token.
                    tok = cir.lexer.token()
                cir.elements[newElement.refDes] = newElement
            else:
                # Element with the same identifier in this circuit exists!
                printError("Error: element '%s' has already been defined.", 
                           lines[cir.lexer.lineno], find_column(tok))
                cir.errors += 1
                tok = cir.lexer.token()
        elif tok.type == 'CMD':
            if tok.value in END:
                cir.errors += cir.lexer.errCount
                if cir.errors != 0:
                    print "Errors found in '%s'. Instructions with it not be executed.\n"%(cir.file)
                break
            elif tok.value[0:3] in INC:
                tok = cir.lexer.token()
                while tok.type == 'FNAME':
                    cir.libs.append(tok.value)
                    tok = cir.lexer.token()
                    if not tok:
                        break
            elif tok.value == 'SUBCKT':
                # Recursively checking of sub circuits
                subCircuit = circuit()
                subCircuit.lexer = cir.lexer
                subCircuit.subCKT = True
                subCircuit = makeCircuit(subCircuit)
                cir.lexer = subCircuit.lexer
                tok = cir.lexer.token()
                cir.circuits[subCircuit.title] = subCircuit
                if subCircuit.errors !=0:
                    # Errors in sub circuit, this also raises an error in the parent circuit
                    print "Errors found in definition of sub circuit."
                    cir.errors += 1
            elif tok.value == 'MODEL':
                tok = cir.lexer.token()
                if tok:
                    if tok.type == 'ID':
                        newModel = modelDef()
                        newModel.params = {}
                        newModel.name = tok.value
                    else:
                        printError("Error: expected a model name.", 
                                   lines[cir.lexer.lineno], find_column(tok))
                    tok = cir.lexer.token()
                    if tok:
                        if tok.type == 'ID':
                            if tok.value in MODELS:
                                newModel.type = tok.value
                            else:
                                printError("Error: unknown model type.", 
                                           lines[cir.lexer.lineno], find_column(tok))
                                cir.errors += 1
                        else:
                            printError("Error: expected a model type.", 
                                       lines[cir.lexer.lineno], find_column(tok))
                            cir.errors += 1
                        tok = lexer.token()
                        while tok.type == 'PARDEF' or tok.type == 'PLUS':
                            if tok.type == 'PLUS':
                                pass
                            elif tok.value[0] not in newModel.params.keys():
                                newModel.params[tok.value[0]]=tok.value[1]
                            else:
                                # Parameter that must be passed to the circuit has
                                # already been pased to it!
                                printError("Error: parameter has already been defined.", 
                                            lines[cir.lexer.lineno], find_column(tok))
                                cir.errors += 1
                            tok = cir.lexer.token()  
                            if not tok:
                                break
                    cir.modelDefs[newModel.name] = newModel
                else:
                    print "Error: missing model dedinition."
            elif tok.value == 'PARAM':
                tok = cir.lexer.token()
                if tok:
                    if tok.type == 'PARDEF' or tok.type == 'PLUS':
                        # Here we have a parameter definition line
                        while tok.type == 'PARDEF' or tok.type == 'PLUS':
                            if tok.type == 'PLUS':
                                # Do nothing, just get a new token
                                pass
                            elif tok.value[0] not in cir.parDefs.keys():
                                cir.parDefs[tok.value[0]] = tok.value[1]
                            else:
                                # This parameter has already been defined!
                                #printError("Error: parameter has already been defined.", 
                                #           lines[cir.lexer.lineno], find_column(tok))
                                #cir.errors += 1
                                pass
                            tok = cir.lexer.token()
                            if not tok:
                                break
                    else:
                        # Wrong token at this position!
                        print("Error: expected a parameter definition.", 
                              lines[cir.lexer.lineno], find_column(tok))
                        cir.errors += 1
                        tok = cir.lexer.token()
                        if not tok:
                            break
                else:
                    print "Error: missing a parameter definition."
            elif tok.value == 'BACKANNO':
                tok = cir.lexer.token()
            else:
                # All what's left are tokens we don't expect at this position
                printError("Error: unexpected input.", lines[cir.lexer.lineno], 
                           find_column(tok))
                cir.errors += 1
                tok = cir.lexer.token()
                if not tok:
                    break
        else:
            # All what's left are tokens we don't expect at this position
            printError("Error: unexpected input.", lines[cir.lexer.lineno], 
                       find_column(tok))
            cir.errors += 1
            tok = cir.lexer.token()
            if not tok:
                break
    cir.errors += cir.lexer.errCount
    if cir.errors != 0:
        print "Errors found in '%s'. Instructions with it not be executed.\n"%(cir.file)
    else:
        needExpansion = False
        for refDes in cir.elements.keys():
            if cir.elements[refDes].model not in MODELS.keys():
                needExpansion = True
            elif MODELS[cir.elements[refDes].model].stamp == False:
                needExpansion = True
        if needExpansion:
            # First add the user libraries to the global library LIB
            addUserLibs(cir.libs)
            # Put the title of the circuit in the global CIRTITLES
            CIRTITLES.append(cir.title) 
            cir = expandModelsCircuits(cir)
        if cir.errors != 0:
            print """Errors found during expansion of '%s'.
Instructions with this circuit will not be executed."""%(cir.title)
    return cir

def expandModelsCircuits(circuitObject):
    """
    Expands the subcircuits and the models that require expansion.
    
    This proceeds as follows:
    
    #. Check if models and model parameters used with element definitions can
       be found in built-in models, models defined with the circuit, or in
       precompiled libraries.
    #. If element models are not 'stamp' models, expand them by using their
       prototype subcircuit.
    #. If element models refer to sub circuits, check for a hierarchical loop 
       and if this does not exists, expand them by using their prototype 
       subcircuit.
        
    :param circuitObject: Circuit object to which the data will be added.
    :type circuitObject: SLiCAPprotos.circuit
    :return: circuitObject with expanded circuits or models
    :rtype: SLiCAPprotos.circuit
    """
    global CIRTITLES, LIB
    # Check if model names and parameters can be found for all elements.
    for refDes in circuitObject.elements.keys():
        # Do this for all elements except sub circuits
        if circuitObject.elements[refDes].type != 'X':
            modelName = circuitObject.elements[refDes].model
            # Get the basic model type for this element
            if modelName in circuitObject.modelDefs.keys():
                # Get it from a local definition in the circuit
                basicModel = circuitObject.modelDefs[modelName].type
            elif modelName in LIB.modelDefs.keys():
                # Get it from a definition in the precompiled libraries
                basicModel = LIB.modelDefs[modelName].type
            elif modelName in MODELS.keys():
                # Get it from the built-in models
                basicModel = modelName
            else:
                basicModel = ''
                print "Cannot find basic model for '%s'"%(refDes)
                circuitObject.errors += 1
            if circuitObject.errors == 0:
                # Check for valid parameter names for this model.
                # These names are defined with the built-in models.
                modelParams = MODELS[basicModel].params.keys()
                for parName in circuitObject.elements[refDes].params.keys():
                    if parName not in modelParams:
                        print "Invalid parameter name '%s' for '%s'."%(parName, refDes)
                        circuitObject.errors += 1
                    else:
                        # Check if the ini.Laplace parameter is used in the
                        # expression for the model parameters and if this is allowed.
                        valExpr = circuitObject.elements[refDes].params[parName]
                        # valExpr is either an integer or a float of a sympy object
                        if isinstance(valExpr, tuple(sp.core.all_classes)):
                            exprParams = list(circuitObject.elements[refDes].params[parName].atoms(sp.Symbol))
                            if ini.Laplace in exprParams and MODELS[basicModel].params[parName] == False:
                                circuitObject.errors += 1
                                print "Error: Laplace variable not allowed in expression '%s' of parameter '%s' of element '%s'"%(valExpr, parName, refDes)
            if circuitObject.errors == 0:
                # Change the model name of the element to the basic model name
                circuitObject.elements[refDes].model = basicModel
                # Parse parameter values
                for parName in modelParams:
                    if parName in circuitObject.elements[refDes].params.keys():
                        # These parameters were defined with the element, keep them
                        pass
                    elif parName in circuitObject.modelDefs.keys():
                        # Take the value from the model definition from the circuit
                        circuitObject.elements[refDes].params[parName] = \
                        circuitObject.circuitObject.modelDefs[parName]
                    elif modelName not in MODELS.keys():
                        # Not a standard model
                        if modelName in circuitObject.modelDefs.keys() and parName in circuitObject.modelDefs[modelName].params.keys():
                            # See if there is a model definition with the circuit 
                            # and take the parameter value from there
                            circuitObject.elements[refDes].params[parName] = \
                            circuitObject.modelDefs[modelName].params[parName]
                        elif modelName in LIB.modelDefs.keys() and parName in LIB.modelDefs[modelName].params.keys():
                            # See if there is a model definition in the library
                            # and take the parameter value from there
                            circuitObject.elements[refDes].params[parName] = \
                            LIB.modelDefs[modelName].params[parName]
            if basicModel != '':
                stamp = MODELS[basicModel].stamp
                if stamp == False:
                    protoCircuit = LIB.circuits[basicModel]
        else:  
            # Now we have a sub circuit
            stamp = False
            # Do this for sub circuits
            modelName = circuitObject.elements[refDes].model
            if modelName in CIRTITLES:
                # We have an hierarchical loop
                print "Error: hierarchical loop involving '%s'."%(modelName)
                circuitObject.errors += 1
                # No expansion
                return circuitObject
            if modelName in circuitObject.circuits.keys() :
                protoCircuit = circuitObject.circuits[modelName]
            elif modelName in LIB.circuits.keys():
                protoCircuit = LIB.circuits[modelName]
            else:
                print "Error: cannot find sub circuit definition '%s' for '%s'."%(modelName, refDes)
                circuitObject.errors += 1                            
        if circuitObject.errors == 0:
            if stamp == False:
                # We need to expand the model
                elmt = circuitObject.elements[refDes]
                circuitObject = expandCircuit(elmt, circuitObject, protoCircuit)
            elif  circuitObject.elements[refDes].type == 'X':
                # We need to expand the subcircuit
                elmt = circuitObject.elements[refDes]
                circuitObject = expandCircuit(elmt, circuitObject, protoCircuit)
    CIRTITLES.pop(-1)
    return circuitObject

def expandCircuit(elmt, parentCircuit, childCircuit):
    """
    Expands an element 'elmt' of 'parentCircuit' based on the prototype 
    'childCircuit'.
    
    After expansion the element 'elmt' will be removed from 'parentCircuit'.
    
    This proceeds as follows:
        
    #. New circuit elements
    
       #. Each element of the child circuit will be added to the parent.
       #. The name (refdes) of this element childID_parentID, where
          'childID' is the name of the element of the child circuit and 
          'parentID is the name of the element of the parent circuit that
          needed to be expanded (e.g. Xnnn or Mnnn).
        
    #. Node names
        
       #. If a node ID of the child element is found in the connecting nodes of
          the child circuit, the corresponding node of the new element obtains 
          this node ID.
       #. If the node of the child element is the global ground node: '0', the 
          corresponding node of the new element is also '0'.
       #. In other case we have a local node. The corresponding node of the new 
          element will then be the node ID of the element of the child circuit
          with added suffix: '_parentID.
       
    #. Reference names
    
       #. References to other elements are always local. The names of referenced
          elements will obtain the suffix: '_parentID'.
    
    #. Parameter names

       #. Parameter definitions used in 'elmt' will be passed tho parameters
          of the child circuit
       #. All other parameter names used in both element definitions and 
          parameter definitions of the child circuit will obtain the suffix '_parentID'.
          
    :param elmt: Element of the parent circuit that requires expansion
    :type param: SLiCAP.protos.element
    :param parentCircuit: Circuit object of the circuit with the element 'elmt'
    :type parentCircuit: SLiCAP.protos.circuit
    :param childCircuit: Prototype circuit used for expansion of 'elmt'
    :type childCircuit: SLiCAP.protos.circuit
    :return: parentCircuit Circuit in which 'elmt' is replaced with elements
             of the child circuit.
    :rtype: SLiCAPprotos.circuit
    """
    # make the suffix for parameters and element IDs
    suffix = '_' + elmt.refDes
    # make a substitution dictionary for parameters
    substDict = {}
    # Put the names and values of the parameters of the parent element in this 
    # dictionary. These names should be passed to the child.
    for key in elmt.params.keys():
        substDict[sp.Symbol(key)] = elmt.params[key]
    # If they are not yet in, put the default values of the child circuit 
    # parameters in this dictionary.
    for key in childCircuit.params.keys():
        if sp.Symbol(key) not in substDict.keys():
            substDict[sp.Symbol(key)] = childCircuit.params[key]
    # Copy the parameter definitions of the child circuit to a new dict
    # The keys and entries of this dictionary will be modified
    newParDefs= {} # Temporary storage for new parameter definitions
    for key in childCircuit.parDefs.keys():
        newParDefs[key] = childCircuit.parDefs[key]
        if key not in LIB.parDefs.keys() and sp.Symbol(key) not in substDict.keys():
            substDict[sp.Symbol(key)] = sp.Symbol(key + suffix)
    newElements = {} # Temp storage for all the new elements
    for elName in childCircuit.elements.keys():
        # Create element with new refdes
        childElement = childCircuit.elements[elName]
        newElement = element()
        newElement.model = childCircuit.elements[elName].model
        newElement.type = elName[0].upper()
        newElement.refDes = elName + suffix
        # Connect it to the parent circuit
        for node in childElement.nodes:
            if node in childCircuit.nodes:
                # This is a connecting node 
                nodeIDX = childCircuit.nodes.index(node)
                newElement.nodes.append(elmt.nodes[nodeIDX])
            elif node == '0':
                # Node '0' is always global!
                newElement.nodes.append(node)
            else:
                # This is a local node
                newElement.nodes.append(node + suffix)
        # Make the list of referenced devices
        for ref in childElement.refs:
            newElement.refs.append(ref + suffix)
        # Add parameters and value of child element to the new element
        for key in childElement.params.keys():
            newElement.params[key] = childElement.params[key]
            # Add local parameters from expressions to the substitution dictionary
            if isinstance(newElement.params[key], tuple(sp.core.all_classes)):
                newParams = list(newElement.params[key].atoms(sp.Symbol))
                for newParam in newParams:
                    if str(newParam) not in LIB.parDefs.keys() and newParam not in substDict.keys() and newParam!= ini.Laplace and newParam != ini.frequency:
                        substDict[newParam] = sp.Symbol(str(newParam) + suffix)
        # Store the element, we still need to update its parameters and values
        newElements[newElement.refDes] = newElement
    # Update parameters and values of new elements
    # Pass the new elements to the parent circuit
    for key in newElements.keys():
        for param in newElements[key].params.keys():
            newElements[key].params[param] = fullSubs(newElements[key].params[param], substDict)
        parentCircuit.elements[key]=newElements[key]
    # Update parameters and values of circuit parameter definitions
    # Pass all the updated child circuit parameter definitions to the parent circuit
    for key in newParDefs.keys():
        newKey = fullSubs(sp.Symbol(key), substDict)
        newValue = fullSubs(newParDefs[key], substDict)
        parentCircuit.parDefs[str(newKey)] = newValue
    # Delete elmt from the parent circuit, it has now been replaced with
    # elements of the child
    del parentCircuit.elements[elmt.refDes]
    return(parentCircuit)
    
def updateCirData(mainCircuit):
    """
    Updates circuit data required for instructions.
    
    - Updates the lists with dependent variables (detectors), sources 
      (independent variables) and controlled sources (possible loop gain 
      references). 
    - If global parameters are used in the circuit, their definition is added
      to the '.parDefs' attribute of the circuit.
    - Checks if the global ground node '0' is used in the circuit.
    - Checks if the circuit has at least two nodes.
    - Checks if the referenced elements exist.
    
    :param mainCircuit: Main (fully expanded) circuit object.
    :type mainCircuit: SLiCAP.protos.circuit
    :return: mainCircuit: Main circuit with updated circuit information for instructions.
    :rtype: SLiCAPprotos.circuit
    """
    # Convert *char* keys in the .parDefs attribute into sympy symbols.
    for key in mainCircuit.parDefs.keys():
        newKey = sp.Symbol(key)
        mainCircuit.parDefs[newKey] = mainCircuit.parDefs[key]
        del(mainCircuit.parDefs[key])
    for key in LIB.parDefs.keys():
        if type(key) == str:
            newKey = sp.Symbol(key)
            LIB.parDefs[newKey] = LIB.parDefs[key]
            del(LIB.parDefs[key])
    # make the node list and check for the ground node
    # check the references (error)
    # make the list with IDs of independent variables
    # make the list with IDs of controlled sources
    # make the list with IDs of dependend variables
    # convert mainCircuit.params to list and put undefined params in it
    mainCircuit.params =[]
    mainCircuit.nodes = []
    varIndexPos = 0
    for elmt in mainCircuit.elements.keys():
        mainCircuit.nodes += mainCircuit.elements[elmt].nodes
        for refID in mainCircuit.elements[elmt].refs:
            if refID not in mainCircuit.elements.keys():
                print "Error: Could not find referenced element '%s'."%(refID)
                mainCircuit.errors += 1
        if mainCircuit.elements[elmt].type in INDEPSCRCS:
            mainCircuit.indepVars.append(elmt)
        elif mainCircuit.elements[elmt].type in CONTROLLED:
            mainCircuit.controlled.append(elmt)
        for i in range(len(MODELS[mainCircuit.elements[elmt].model].depVars)):
            depVar = MODELS[mainCircuit.elements[elmt].model].depVars[i]
            mainCircuit.depVars.append(depVar + '_' + elmt)
            mainCircuit.varIndex[depVar + '_' + elmt] = varIndexPos
            varIndexPos += 1
        # Add parameters used in element expressions to circuit.params
        for par in mainCircuit.elements[elmt].params.keys():
            try:
                mainCircuit.params += list(mainCircuit.elements[elmt].params[par].atoms(sp.Symbol))
            except:
                pass
    # Add parameters used in parDef expressions to circuit.params
    for par in mainCircuit.parDefs.keys():
        try:
            mainCircuit.params += list(mainCircuit.parDefs[par].atoms(sp.Symbol))
        except:
            pass
    mainCircuit.params = list(set(mainCircuit.params))
    # Try to find required global parameter definitions for undefined params
    undefined = []
    for par in mainCircuit.params:        
        if par != ini.Laplace and par != ini.frequency and par not in mainCircuit.parDefs.keys():
            if par in LIB.parDefs.keys():
                mainCircuit.parDefs = addGlobals(mainCircuit.parDefs, par)
            else:
                undefined.append(par)
    mainCircuit.params = undefined
    # check for two connections per node (warning)
    connections = {i:mainCircuit.nodes.count(i) for i in mainCircuit.nodes}
    for key in connections.keys():
        if connections[key] < 2:
            print "Warning less than two connections at node: '%s'."%(key)
    # Remove duplicate entries from node list and sort the list."
    mainCircuit.nodes = list(set(mainCircuit.nodes))
    mainCircuit.nodes.sort()
    if '0' not in mainCircuit.nodes:
        mainCircuit.errors += 1
        print "Error: could not find ground node '0'."
    for i in range(len(mainCircuit.nodes)):
        mainCircuit.depVars.append('V_' + mainCircuit.nodes[i])
        mainCircuit.varIndex[mainCircuit.nodes[i]] = varIndexPos
        varIndexPos += 1
    return mainCircuit

def addGlobals(parDefs, par):
    """
    Adds value or expression of the parameter 'par' as well as the parameters 
    in this expression given in the library to the parameter definitions in the
    dict 'parDefs'.
    
    :param parDefs: Dictionary with key-value pair of parameters to which the 
                    definition of the parameter 'par' needs to added.
    :type parDefs: dict
    :param par: Parameter of which the definition needs to be added to the dict
                'parDefs'.
    :type par: sympy.Symbol
    :return: parDefs: dict with added parameter definitions
    :rtype: dict
    """
    parDefs[par] = LIB.parDefs[par]
    params = LIB.parDefs[par].atoms(sp.Symbol)
    for param in params:
        if param in LIB.parDefs.keys() and param != ini.Laplace and param != ini.frequency:
            addGlobals(parDefs, param)
    return parDefs
    
def makeLibraries():
    """
    Compiles the library 'lib/SLiCAPmodels.lib'.
    
    Returns a circuit object with subcircuits, model definitions and parameter
    definitions from this library.
    
    :return: LIB: circuit object with subcircuits, model definitions and parameter
             definitions from  'lib/SLiCAPmodels.lib'.
    :rtype: SLiCAPprotos.circuit
    """
    global CIRTITLES, LIB
    CIRTITLES = []
    # This must be the first library: it contains the basic expansion models!
    fileName = ini.installPath + 'lib/SLiCAPmodels.lib'
    LIB = circuit()
    LIB.file = fileName
    LIB.lexer = tokenize(fileName)
    LIB = makeCircuit(LIB)
    if LIB.errors != 0:
        print "Errors found in library: '%s'. SLiCAP will not work!"%(fileName)
        return LIB
    else:
        # Do this also for other libs
        CIRTITLES = []
        fileName = ini.installPath + 'lib/SLiCAP.lib'
        cir = circuit()
        cir.file = fileName
        cir.lexer = tokenize(fileName)
        for cirModel in LIB.circuits.keys():
            cir.circuits[cirModel] = LIB.circuits[cirModel]
        for parDef in LIB.parDefs.keys():
            cir.parDefs[parDef] = LIB.parDefs[parDef]
        for modDef in LIB.modelDefs.keys():
            cir.modelDefs[parDef] = LIB.modelDefs[modDef]
        cir = makeCircuit(cir)
        
        if cir.errors != 0:
            print "Errors found in library: '%s'. SLiCAP will not work!"%(fileName)
            LIB.errors = cir.errors
            return LIB
        CIRTITLES = []
        LIB = cir
        return LIB
    
def addUserLibs(fileNames):
    """ 
    Adds pre compiled user libraries to LIB. 
    
    Overwrites existing keys in LIB.
    
    :param fileNames: List with file names (*str*) of user libraries.
    :type fileNames: list
    """
    global CIRTITLES, LIB
    for fi in fileNames:
        # The standard library "SLiCAP.lib" has already been included.
        libFile = fi.split('.')
        try:
            if libFile[0] != 'SLiCAP' and libFile[1].upper() != 'LIB':
                try:
                    # first libraries in circuit directory
                    f = open(ini.projectPath + CIRPATH + fi, "r")
                    fileName = ini.projectPath + CIRPATH + fi
                    f.close()
                except:
                    try:
                        # then libraries in the user library directory
                        f = open(ini.projectPath + LIBRARYPATH + fi, "r")
                        fileName = ini.projectPath + LIBRARYPATH + fi
                        f.close()
                    except:
                        try:
                            # then absolute path
                            f = open(fi, "r")
                            fileName = fi
                            f.close()
                        except:
                            print "Error: cannot find library file: '%s'."%(fi)
                            fileName = False
                if fileName != False:
                    cir = circuit()
                    cir.file = fi
                    cir.lexer = tokenize(fileName)
                    cir = makeCircuit(cir)
                    if cir.errors != 0:
                        print "Errors found in library: '%s'. Library will not be added!"%(fileName)
                    else:
                        for newCircuit in cir.circuits:
                            LIB.circuits[newCircuit.title] = newCircuit
                        for newModelDef in cir.modelDefs:
                            LIB.modelDefs[cir.modelDefs[newModelDef]] = cir.modelDefs[newModelDef]
                        for newParDef in cir.parDefs:
                            LIB.parDefs[newPardef] = cir.parDefs[newParDef]
                        for newLib in cir.libs:
                            LIB.libs.append(newLib)
        except:
            pass
    return()

if __name__ == '__main__':
    """
    Since we are not running a project, we need to define project data.
    """
    ini.projectPath = ini.installPath + 'testProjects/MOSamp/'
    ini.circuitPath = ini.projectPath + 'cir/'
    ini.htmlPath    = ini.projectPath + 'html/'
    ini.htmlIndex   = 'index.html'
    ini.lastUpdate  = datetime.now()
    t1=time()
    LIB = makeLibraries()
    t2=time()  
    fi = 'MOSamp.cir'
    print "\nCheking:", fi
    myCir = checkCircuit(fi)
    t3=time()
    keys = myCir.elements.keys()
    
    for key in keys:
        el = myCir.elements[key]
        print '\nElement    :', key
        print 'Nodes      :', el.nodes
        print 'Refs       :', el.refs
        print 'Model      :', el.model
        print 'Params     :'
        for par in el.params.keys():
            print ' ', par, '=', el.params[par]
    
    print '\nCircuit parameter definitions:'
    for par in myCir.parDefs.keys():
        print ' ', par, '=', myCir.parDefs[par]          
    t4=time()
    for el in myCir.elements.keys():
        for par in  myCir.elements[el].params.keys():
            parNum = fullSubs(myCir.elements[el].params[par], myCir.parDefs)
            print el,'\t', par, sp.N(parNum, ini.disp)
    
    t5=time()