#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
SLiCAPyacc.py

Compiler for SLiCAP netlist files

Created on Mon May  4 12:32:13 2020

@author: anton
"""

from SLiCAPlex import *
from SLiCAPprotos import *  
import os  

LAPLACE = Symbol(LAPLACE)
FREQUENCY = Symbol(FREQUENCY)
OMEGA = Symbol(OMEGA)

# Composite tokens
NODES      = ['NODEID', 'ID', 'INT']
VALEXPR    = ['FLT', 'EXPR', 'SCI', 'INT']
TITLE      = ['ID', 'QSTRING']

# Commands with identical action
INC        = ['INC', 'LIB']
END        = ['END', 'ENDS']

# list with (sub)circuit titles
CIRTITLES = []
LIB = circuit()

def checkCircuit(fileName):
    global CIRTITLES, LIB
    cir = circuit()
    cir.file = fileName
    if LIB.errors == 0:
        cir.lexer = tokenize(fileName)
        cir = makeCircuit(cir)
        if cir.errors == 0:
            cir = updateCirData(cir)
            if cir.errors != 0:
                print( """Errors found during updating of circuit data from '%s'.
    Instructions with this circuit will not be executed."""%(cir.title))
            else:
                print("No errors found for circuit: '%s' from file: '%s'.\n"%(cir.title, fileName))
    else:
        print("Errors found in library. Circuit '%s' will not be ckecked."%(fileName))
    return cir

def makeCircuit(cir):
    """
    Creates a nested circuit object from the tokens in cir.lexer and checks 
    for syntax errors:
        - Unexpected tokens
        - Errors in expressions
        - Double definitions of circuit elements
        - Double parameter definitions in element definition lines
        - Double parameter definitions in .param lines
        - Double parameter definitions in .model lines
        - Double parameter definitions in .subckt lines
    """
    global CIRTITLES
    
    lines = cir.lexer.lexdata.splitlines()
    tok = cir.lexer.token()
    if tok and tok.type in TITLE and cir.subCKT==False:
        # In this case, we a dealing with the main circuit
        cir.title = tok.value
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
                if tok.value in CIRTITLES:
                    print("Error: circuit '%s' has already been defined."%(cir.title))
                    cir.errors += 1
            else:
                printError("Error: expected a circuit title.", 
                           lines[cir.lexer.lineno], find_column(tok))
                cir.errors += 1
        else:
            print("Missing circuit title.")
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
    CIRTITLES.append(cir.title) 
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
                            print("Error: missing node.")
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
                            tok = cir.lexer.token()
                            while tok.type == 'PARDEF' or tok.type == 'PLUS':
                                if tok.type == 'PLUS':
                                    pass
                                elif tok.value[0] not in newElement.params.keys():
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
                            tok = cir.lexer.token()
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
                    print("Errors found in '%s'. Instructions with it not be executed.\n"%(cir.file))
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
                    print("Errors found in definition of sub circuit.")
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
                    print("Error: missing model dedinition.")
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
                    print("Error: missing a parameter definition.")
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
        print("Errors found in '%s'. Instructions with it not be executed.\n"%(cir.file))
    else:
        needExpansion = False
        for refDes in cir.elements.keys():
            if cir.elements[refDes].model not in MODELS.keys():
                needExpansion = True
        if needExpansion:
            cir = expandModelsCircuits(cir)
        if cir.errors != 0:
            print("""Errors found during expansion of '%s'.
                  Instructions with this circuit will not be executed.""" %(cir.title))
    return cir

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
        - all other, except the built-in parameters, used in the child element
          that were not defined by the parent will be renamed by adding the
          suffix: _< parent element refDes >
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
    # Check if names of sub circuits and models are given and can be found
    # and parse parameter values
        
    for refDes in circuitObject.elements.keys():
        if circuitObject.elements[refDes].type != 'X':
            # Do this for all elements except sub circuits
            modelName = circuitObject.elements[refDes].model
            if modelName in circuitObject.modelDefs.keys():
                basicModel = circuitObject.modelDefs[modelName].type
            elif modelName in LIB.modelDefs.keys():
                basicModel = LIB.modelDefs[modelName].type
            elif modelName in MODELS:
                basicModel = modelName
            else:
                basicModel = ''
                print("Cannot find basic model for '%s'"%(refDes))
                circuitObject.errors += 1
            if circuitObject.errors == 0:
                # Check for valid parameter names
                modelParams = MODELS[basicModel].params.keys()
                for parName in circuitObject.elements[refDes].params.keys():
                    if parName not in modelParams:
                        print("Invalid parameter name '%s' for '%s'."%(parName, refDes))
                        circuitObject.errors += 1
                    else:
                        # Check if the LAPLACE parameter is used in the
                        # expression and if this is allowed.
                        valExpr = circuitObject.elements[refDes].params[parName]
                        # valExpr is either an integer or a float of a sympy object
                        if type(valExpr) != float and type(valExpr) != int and type(valExpr) != str:
                            exprParams = circuitObject.elements[refDes].params[parName].free_symbols
                            if LAPLACE in exprParams and MODELS[basicModel].params[parName] == False:
                                circuitObject.errors += 1
                                print("Error: Laplace variable not allowed in expression '%s' of parameter '%s' of element '%s'"%(valExpr, parName, refDes))
            if circuitObject.errors == 0:
                # Change the model name to the basic model name
                circuitObject.elements[refDes].model = basicModel
                # Parse parameter values
                # ToDo: user library before SLiCAP library
                for parName in modelParams:
                    if parName in circuitObject.elements[refDes].params.keys():
                        # These parameters were already defined
                        pass
                    elif modelName not in MODELS.keys() and modelName in circuitObject.modelDefs.keys() and parName in circuitObject.modelDefs[modelName].params.keys():
                        # Not a basic model: check if there is a model definition
                        # with the circuit and take parameters from there
                        circuitObject.elements[refDes].params[parName] = \
                        circuitObject.modelDefs[modelName].params[parName]
                    elif modelName not in MODELS.keys() and modelName in LIB.modelDefs.keys() and parName in LIB.modelDefs[modelName].params.keys():
                        # Not a basic model: check if there is a library
                        # model and take the value from it
                        circuitObject.elements[refDes].params[parName] = \
                        LIB.modelDefs[modelName].params[parName]
                    elif parName in circuitObject.modelDefs.keys():
                        # Take this value 
                        circuitObject.elements[refDes].params[parName] = \
                        circuitObject.circuitObject.modelDefs[parName]
            if basicModel != '':
                stamp = MODELS[basicModel].stamp
                if stamp == False:
                    protoCircuit = LIB.circuits[basicModel]
        else:  
            stamp = False
            # Do this for sub circuits
            modelName = circuitObject.elements[refDes].model
            if modelName in circuitObject.circuits.keys() :
                protoCircuit = circuitObject.circuits[modelName]
            elif modelName in LIB.circuits.keys():
                protoCircuit = LIB.circuits[modelName]
            else:
                print("Error cannot find sub circuit definition '%s' for '%s'."%(modelName, refDes))
                circuitObject.errors += 1                            
        if circuitObject.errors == 0:
            if stamp == False or circuitObject.elements[refDes].type == 'X':
                elmt = circuitObject.elements[refDes]
                circuitObject = expandCircuit(elmt, circuitObject, protoCircuit)
    return circuitObject

def expandCircuit(elmt, parentCircuit, childCircuit):
    """
    The parsing of nodes to new elements of the expanded circuit will be as
    follows:
        
    For each element in the child circuit, create an element object that will
    be added to the parent circuit.
    If a node ID of the child element is found in the connecting nodes of the
    child circuit (.nodes attribute), then the corresponding node of the new 
    element obtains this node ID.
    If the node of the child element is the global ground node: '0', the 
    corresponding node of the new element is also '0'.
    In other case we have a local node. The corresponding node of the new 
    element will then be the node ID of the element of the child circuit with
    added suffix: '_< elmt.refDes >.
    
    The parsing of element model parameters and parameter definitions in the
    child circuit will be as follows:
    Create a substitution dicionary:
    The keys of the dictionary are 
    
    """
    # make the suffix for parameters and element IDs
    suffix = '_' + elmt.refDes
    # make a substitution dictionary for parameters
    substDict = {}
    # Put the names and values of the parameters of the parent element in this 
    # dictionary
    for key in elmt.params.keys():
        substDict[Symbol(key)] = elmt.params[key]
    # If they are not yet in, put the default values of the child circuit 
    # parameters in this dictionary
    for key in childCircuit.params.keys():
        if Symbol(key) not in substDict.keys():
            substDict[Symbol(key)] = childCircuit.params[key]
    # Copy the parameter definitions of the child circuit to a new dict
    # The keys and entries of this dictionary will be modified
    newParDefs= {} # Temporary storage for new parameter definitions
    for key in childCircuit.parDefs.keys():
        newParDefs[key] = childCircuit.parDefs[key]
        if key not in LIB.parDefs.keys() and Symbol(key) not in substDict.keys():
            substDict[Symbol(key)] = Symbol(key + suffix)
    newElements = {} # Temp storage for all the new elements
    for elName in childCircuit.elements.keys():
        # Create element with new refdes
        childElement = childCircuit.elements[elName]
        newElement = element()
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
            newParams = newElement.params[key].free_symbols
            for newParam in newParams:
                if str(newParam) not in LIB.parDefs.keys() and newParam not in substDict.keys():
                    substDict[newParam] = Symbol(str(newParam) + suffix)
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
        newKey = fullSubs(Symbol(key), substDict)
        newValue = fullSubs(newParDefs[key], substDict)
        parentCircuit.parDefs[newKey] = newValue
    # Delete elmt from the parent circuit, it has now been replaced with
    # elements of the child
    del parentCircuit.elements[elmt.refDes]
    return(parentCircuit)
    
def fullSubs(valExpr, parDefs):
    """
    Returns the valExpr after all parameters of parDefs have been substituted
    recursively into valExpr.
    parDefs is a dictionary in which the keys are sympy symbols. The type of 
    the value fields may be any sympy type, integer or float.
    """
    strValExpr = str(valExpr)
    i = 0
    newvalExpr = 0
    while valExpr != newvalExpr and i < MAXRECSUBST and type(valExpr) != int and type(valExpr) != float:
        # create a substitution dictionary with the smallest number of entries (this speeds up the substitution)
        substDict = {}
        params = valExpr.free_symbols
        for param in params:
            if param in parDefs.keys():
                substDict[param] = parDefs[param]
        # perform the substitution
        newvalExpr = valExpr
        valExpr = newvalExpr.subs(substDict)
        i += 1
    if i == MAXRECSUBST:
        print("Warning: reached maximum number of substitutions for expression '%s'"%(strValExpr))
    return valExpr
    
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
    # Add global parameters
    for parName in LIB.parDefs.keys():
        if parName not in mainCircuit.parDefs.keys():
            mainCircuit.parDefs[parName] = LIB.parDefs[parName]
    # Convert *char* keys in the .parDefs attribute into sympy symbols.
    # make the node list and check for the ground node
    # check the references (error)
    # make the list with IDs of independent variables
    # make the list with IDs of dependend variables
    # make the list with IDs of controlled sources
    # check for two connections per node (warning)
    return mainCircuit

def makeLibraries():
    global CIRTITLES, LIB
    CIRTITLES = []
    # This must be the first library: it contains the basic expansion models!
    fileName = 'lib/SLiCAPmodels.lib'
    LIB = circuit()
    LIB.file = fileName
    LIB.lexer = tokenize(fileName)
    LIB = makeCircuit(LIB)
    if LIB.errors != 0:
        print("Errors found in library: '%s'. SLiCAP will not work!"%(fileName))
        return LIB
    else:
        # Do this also for other libs
        CIRTITLES = []
        fileName = 'lib/SLiCAP.lib'
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
            print("Errors found in library: '%s'. SLiCAP will not work!"%(fileName))
            LIB.errors = cir.errors
            return LIB
        return cir

if __name__ == '__main__':
    LIB = makeLibraries()
    
    import os
    files = os.listdir('cir')
    
    for fi in files:
        [cirFileName, ext] = fi.split('.')
        if ext.lower() == 'cir':   
    
            #fi = 'MOSamp.cir'
            print("\nCheking:", fi)
            myCir = checkCircuit('cir/' + fi )
            """
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
            """