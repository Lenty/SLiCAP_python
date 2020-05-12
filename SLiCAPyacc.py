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
from SLiCAPexpandModelsCircuits import *
    
# Composite tokens
NODES      = ['NODEID', 'ID', 'INT']
MODVALEXPR = ['FLT', 'EXPR', 'SCI', 'INT']
TITLE      = ['ID', 'QSTRING']

# Commands with identical action
INC        = ['INC', 'LIB']
END        = ['END', 'ENDS']

# list with (sub)circuit titles
CIRTITLES = []

def checkCircuit(fileName):
    CIRTITLES = []
    cir = circuit()
    cir.file = fileName
    cir.lexer = tokenize(fileName)
    cir = makeCircuit(cir)
    if cir.errors != 0:
        print "Errors found in '%s'. The circuit is incomplete and instructions with it not be executed.\n"%(fileName)
    else:
        cir = expandModelsCircuits(cir)
        if cir.errors != 0:
            print "Errors found, during expansion of circuit '%s'. Circuit data of '%s' will not be updated and instructions with this circuit will not be executed.\n"%(cir.title)
        else:
            cir = updateCirData(cir)
            if cir.errors != 0:
                print "Errors found during updating of circuit data from '%s'. Instructions with this circuit will not be executed.\n"%(cir.title)
            else:
                print "No errors found for circuit '%s' from file: '%s'.\n"%(cir.title, fileName)
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
            while tok and tok.type == 'PLUS':
                tok = cir.lexer.token()
            if tok and tok.type in TITLE:
                cir.title = tok.value       
                if tok.value in CIRTITLES:
                    print "Error: circuit '%s' has already been defined."%(cir.title)
                    cir.errors += 1
            else:
                printError("Error: expected a circuit title.", lines[cir.lexer.lineno], find_column(tok))
                cir.errors += 1
        else:
            print "Missing circuit title."
            cir.errors += 1
        tok = cir.lexer.token()
        nNodes = 0
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
        nodesModel = []
        while tok and tok.type != 'PARDEF' and newLine == False:
            tok = cir.lexer.token()
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
        circuit.nodes = nodesModel[0:-1]   
        # Parameters that can be passed to the circuit have 'PARDEF' tokens
        while tok.type == 'PARDEF' or tok.type == 'PLUS':
            if tok.type == 'PLUS':
                pass
            else:
                cir.params[tok.value[0]]=tok.value[1]
            tok = cir.lexer.token()
        # Here we have the first token of the second line of the sub circuit
        # definition. Further checking is identical as with the main circuit,
        # except for a '.ends' command token at the end.
    else:
        printError("Error: expected a circuit title.", lines[cir.lexer.lineno], find_column(tok))
        tok = cir.lexer.token()
        # Here we have the first token of the second line of the circuit 
        # definition. Further checking is identical as with the sub circuit,
        # except for a '.end' command token at the end.
    CIRTITLES.append(cir.title) 
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
                            while tok and tok.type == 'PLUS':
                                tok = cir.lexer.token()
                            if tok.type in NODES:
                                newElement.nodes.append(tok.value)
                            else:
                                # Wrong token!
                                printError("Error: expected a nodeID", lines[cir.lexer.lineno], find_column(tok))
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
                    while tok and tok.type != 'PARDEF' and newLine == False:
                        tok = cir.lexer.token()
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
                        printError("Error: expected at least two nodes.", lines[cir.lexer.lineno], find_column(tok))   
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
                            printError("Error: expected an element ID.", lines[cir.lexer.lineno], find_column(tok))
                            cir.errors += 1
                if value:
                    tok = cir.lexer.token()
                    if tok:
                        while tok and tok.type == 'PLUS':
                            tok = cir.lexer.token()
                        if tok.type in MODVALEXPR:
                            if tok.type == 'INT':
                                tok.value = int(tok.value)
                            newElement.params['value'] = tok.value
                            tok = cir.lexer.token()
                        elif tok.type == 'ID':
                            newElement.model = tok.value      
                            tok = cir.lexer.token()
                            while tok.type == 'PARDEF' or tok.type == 'PLUS':
                                if tok.type == 'PLUS':
                                    tok = cir.lexer.token()
                                elif tok.value[0] not in newElement.params.keys():
                                    newElement.params[tok.value[0]]=tok.value[1]
                                else:   
                                    # Parameter that must be passed to the 
                                    # element has already been pased to it!
                                    printError("Error: parameter has already been defined.", lines[cir.lexer.lineno], find_column(tok))
                                    cir.errors += 1
                                tok = cir.lexer.token()
                    else:
                        # Wrong token at this position!
                        printError("Error: expected a model, a value or an expression", lines[cir.lexer.lineno], find_column(tok))
                        cir.errors += 1
                elif newElement.type == 'X':
                    # For sub circuits we already have the model and value=False
                    # Here we will process the parameters of the sub circuit
                    while tok.type == 'PARDEF' or tok.type == 'PLUS':
                        if tok.type == 'PLUS':
                            tok = cir.lexer.token()
                        elif tok.value[0] not in newElement.params.keys():
                            newElement.params[tok.value[0]]=tok.value[1]
                        else:
                            # Parameter that must be passed to the circuit has
                            # already been pased to it!
                            printError("Error: parameter has already been defined.", lines[cir.lexer.lineno], find_column(tok))
                            cir.errors += 1
                        tok = cir.lexer.token()
                else:
                    # No value required, get the next token.
                    tok = cir.lexer.token()
                cir.elements[newElement.refDes] = newElement
            else:
                # Element with the same identifier in this circuit exists!
                printError("Error: element '%s' has already been defined.", lines[cir.lexer.lineno], find_column(tok))
                cir.errors += 1
                tok = cir.lexer.token()
        elif tok.type == 'CMD':
            if tok.value in END:
                break
            elif tok.value[0:3] in INC:
                tok = cir.lexer.token()
                while tok.type == 'FNAME':
                    cir.libs.append(tok.value)
                    tok = cir.lexer.token()
            elif tok.value == 'SUBCKT':
                # Recursive checking of sub circuits
                subCircuit = circuit()
                subCircuit.lexer = cir.lexer
                subCircuit.subCKT = True
                subCircuit = makeCircuit(subCircuit)
                cir.lexer = subCircuit.lexer
                tok = cir.lexer.token()
                cir.circuits[subCircuit.title] = subCircuit
                if subCircuit.errors !=0:
                    # Errors in sub circuit, this also raises an error in the parent circuit
                    printError("Errors found in definition of sub circuit.", "", 0)
                    cir.errors += 1                  
            elif tok.value == 'MODEL':
                tok = cir.lexer.token()
                if tok:
                    if tok.type == 'ID':
                        newModel = modelDef()
                        newModel.name = tok.value
                    else:
                        printError("Error: expected a model name.", lines[cir.lexer.lineno], find_column(tok))
                    tok = cir.lexer.token()
                    if tok:
                        if tok.type == 'ID':
                            if tok.value in MODELS:
                                newModel.type = tok.value
                            else:
                                printError("Error: unknown model type.", lines[cir.lexer.lineno], find_column(tok))
                                cir.errors += 1
                        else:
                            printError("Error: expected a model type.", lines[cir.lexer.lineno], find_column(tok))
                            cir.errors += 1
                        tok = lexer.token()
                        while tok.type == 'PARDEF' or tok.type == 'PLUS':
                            if tok.type == 'PLUS':
                                tok = cir.lexer.token()
                            elif tok.value[0] not in newModel.params.keys():
                                newModel.params[tok.value[0]]=tok.value[1]
                            else:
                                # Parameter that must be passed to the circuit has
                                # already been pased to it!
                                printError("Error: parameter has already been defined.", lines[cir.lexer.lineno], find_column(tok))
                                cir.errors += 1
                            tok = cir.lexer.token()
                    cir.modelDefs = newModel
                else:
                    printError("Error: missing model dedinition.", "", 0)
            elif tok.value == 'PARAM':
                tok = cir.lexer.token()
                if tok:
                    if tok.type == 'PARDEF' or tok.type == 'PLUS':
                        # Here we have a parameter definition line
                        while tok.type == 'PARDEF'or tok.type == 'PLUS':
                            if tok.type == 'PLUS':
                                # Do nothing, just get a new token
                                pass
                            elif tok.value[0] not in cir.parDefs.keys():
                                cir.parDefs[tok.value[0]] = tok.value[1]
                            else:
                                # This parameter has already been defined!
                                printError("Error: parameter has already been defined.", lines[cir.lexer.lineno], find_column(tok))
                                cir.errors += 1
                            tok = cir.lexer.token()
                    else:
                        # Wrong token at this position!
                        print("Error: expected a parameter definition.", lines[cir.lexer.lineno], find_column(tok))
                        cir.errors += 1
                        tok = cir.lexer.token()
                else:
                    printError("Error: missing a parameter definition.", "", 0)
        else:
            # All what's left are tokens we don't expect at this position
            printError("Error: unexpected input.", lines[cir.lexer.lineno], find_column(tok))
            cir.errors += 1
            tok = cir.lexer.token()
    cir.errors += cir.lexer.errCount
    return cir

if __name__ == '__main__':
    import os
    files = os.listdir('cir')
    
    for fi in files:
        [cirFileName, ext] = fi.split('.')
        if ext.lower() == 'cir':    
            #fi = 'testCircuit.cir'
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