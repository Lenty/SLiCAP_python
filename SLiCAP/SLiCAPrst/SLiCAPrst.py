#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 17:14:37 2023

@author: anton
"""
from SLiCAP.SLiCAPdesignData import specList2dict
from SLiCAP.SLiCAPhtml import roundN
from SLiCAP.SLiCAPmath import fullSubs
from SLiCAP import ini
import sympy as sp
from shutil import copyfile

# Snippets that can be stored as RST files to be included by other RST files.

def netlist2RST(netlistFile, lineRange=None, firstNumber=None, position=0):
    copyfile(ini.circuitPath + netlistFile, ini.sphinxPath + 'SLiCAPdata/' + netlistFile)
    spaces = makeSpaces(position)
    RST = spaces +'.. literalinclude:: ../SLiCAPdata/' + netlistFile + '\n'
    RST += spaces + '    :linenos:\n'
    if lineRange != None:
        RST += spaces + '    :lines: ' + lineRange + '\n'
        if firstNumber != None:
            RST += spaces + '    :lineno-start: ' + str(firstNumber) + '\n'
    return RST

def elementData2RST(circuitObject, position=0, label=''):
    spaces     = makeSpaces(position)
    name       = 'Expanded netlist of: ' + circuitObject.title
    headerList = ["ID", "Nodes", "Refs", "Model", "Param", "Symbolic", "Numeric"]
    linesList   = []
    for key in circuitObject.elements.keys():
        el = circuitObject.elements[key] 
        line = [key]
        
        lineItem = ''
        nodes = ''
        for node in el.nodes:
            lineItem += node + ' '
        line.append(lineItem)
        
        lineItem = ''
        for ref in el.refs:
            lineItem += ref + ' '
        line.append(lineItem)
        line.append(el.model)
        if len(el.params.keys()) == 0:
            line += ['','','']
        else:
            keys = list(el.params.keys())
            for i in range(len(keys)):
                if i == 0:
                    line.append(keys[i])
                    line.append(el.params[keys[i]])
                    line.append(fullSubs(el.params[keys[i]], circuitObject.parDefs))
                    linesList.append(line)
                else:
                    line = ['','','','']
                    line.append(keys[i])
                    line.append(el.params[keys[i]])
                    line.append(fullSubs(el.params[keys[i]], circuitObject.parDefs))
        linesList.append(line)
    RST = RSTcreateCSVtable(name, headerList, linesList, position=position, label=label)
    return RST

def parDefs2RST(circuitObject, position=0, label=''):
    if len(circuitObject.parDefs) > 0:
        spaces     = makeSpaces(position)
        name       = 'Parameter defnitions in: ' + circuitObject.title
        headerList = ["Name", "Symbolic", "Numeric"]
        linesList   = []
        for parName in circuitObject.parDefs.keys():
            line = [parName, 
                circuitObject.parDefs[parName], 
                fullSubs(circuitObject.parDefs[parName], circuitObject.parDefs)]
            linesList.append(line)
        RST = RSTcreateCSVtable(name, headerList, linesList, position=position, label=label) 
    else:
        RST = "**No parameter definitions in: " +  circuitObject.title + '**\n\n'        
    return RST

def params2RST(circuitObject, position=0, label=''):
    if len(circuitObject.params) > 0:
        spaces     = makeSpaces(position)
        name       = 'Undefined parameters in: ' + circuitObject.title
        headerList = ["Name"]
        linesList   = []
        for parName in circuitObject.params:
            lineList.append([parName])
        RST = RSTcreateCSVtable(name, headerList, linesList, position=position, label=label) 
    else:
        RST = '**No undefined parameters in: ' +  circuitObject.title + '**\n\n'                          
    return RST

def pz2RST(resultObject, position=0, label = ''):
    RST = ''
    if resultObject.errors != 0:
        print("pz2RST: Errors found in instruction.")
    elif resultObject.dataType != 'poles' and resultObject.dataType != 'zeros' and resultObject.dataType != 'pz':
        print("pz2RST: Error: 'pz2RST()' expected dataType: 'poles', 'zeros', or 'pz', got: '{0}'.".format(instObj.dataType))
    elif resultObject.step == True :
        print("pz2RST: Error: parameter stepping not implemented for 'pz2RST()'.")
    else:
        if resultObject.dataType == 'poles':
            name = 'Poles of: ' + resultObject.gainType
        elif resultObject.dataType == 'zeros':
            name = 'Zeros of: ' + resultObject.gainType
        elif resultObject.dataType == 'pz':
            name = 'Poles and zeros of: ' + resultObject.gainType + '. DC gain = :math:`' + sp.latex(roundN(resultObject.DCvalue)) + '`'
        if resultObject.simType == 'numeric':
            if ini.Hz == True:
                headerList = ['#', 'Re [Hz]', 'Im [Hz]', ':math:`f` [Hz]', 'Q']
            else:
                headerList = ['#', 'Re [rad/s]', 'Im [rad/s]', ':math:`\omega` [rad/s]', 'Q']  
        else:
            if ini.Hz == True:
                headerList = ['#', ':math:`f` [Hz]']
            else:
                headerList = ['#', ':math:`\omega` [rad/s]']
        linesList = []        
        if resultObject.dataType == 'poles' or resultObject.dataType == 'pz':
            if resultObject.simType == 'numeric':
                linesList += numRoots2RST(resultObject.poles, ini.Hz, 'p')
            else:
                linesList += symRoots2RST(resultObject.poles, ini.Hz, 'p')
            
        if resultObject.dataType == 'zeros' or resultObject.dataType == 'pz':
            if resultObject.simType == 'numeric':
                linesList += numRoots2RST(resultObject.zeros, ini.Hz, 'z')
            else:
                linesList += symRoots2RST(resultObject.zeros, ini.Hz, 'z')
                
        RST += RSTcreateCSVtable(name, headerList, linesList, position=position, label=label)   
    return RST

def noiseContribs2RST(resultObject, position=0):
    if resultObject.dataType == 'noise' and resultObject.step == False:
        detunits = sp.sympify(resultObject.detUnits + '**2/Hz')
        if resultObject.srcUnits != None:
            srcunits = sp.sympify(resultObject.srcUnits + '**2/Hz')
        # Add a table with noise contributions
        linesList = []
        headerList = ['', 'Value' , 'Units']
        name = "Source contributions"
        for src in resultObject.onoiseTerms.keys():
            if src[0].upper() == 'I':
                units = 'A**2/Hz'
            elif src[0].upper() == 'V':
                units = 'V**2/Hz'
            units = sp.sympify(units)
            line = [src + ': Source value', resultObject.snoiseTerms[src], units]
            linesList.append(line)
            if resultObject.srcUnits != None:
                line = [src + ': Source-referred', resultObject.inoiseTerms[src], srcunits]
                linesList.append(line)
            line = [src + ': Detector-referred', resultObject.onoiseTerms[src], detunits]
            linesList.append(line)
        RST = RSTcreateCSVtable(name, headerList, linesList, unitpos=2)
    else:
        RST = ''
        print('noise2RST: Error: wrong data type, or stepped analysis.')
    return RST

def dcvarContribs2RST(resultObject, position=0):
    if resultObject.dataType == 'dcvar' and resultObject.step == False:
        detunits = sp.sympify(resultObject.detUnits + '**2')
        if resultObject.srcUnits != None:
            srcunits = sp.sympify(resultObject.srcUnits + '**2')
        # Add a table with dcvar contributions
        linesList = []
        headerList = ['', 'Value' , 'Units']
        name = "Source contributions"
        for src in resultObject.ovarTerms.keys():
            if src[0].upper() == 'I':
                units = 'A**2'
            elif src[0].upper() == 'V':
                units = 'V**2'
            units = sp.sympify(units)
            line = [src + ': Source value', resultObject.svarTerms[src], units]
            linesList.append(line)
            if resultObject.srcUnits != None:
                line = [src + ': Source-referred', resultObject.ivarTerms[src], srcunits]
                linesList.append(line)
            line = [src + ': Detector-referred', resultObject.ovarTerms[src], detunits]
            linesList.append(line)
        RST = RSTcreateCSVtable(name, headerList, linesList, unitpos=2)
    else:
        RST = ''
        print('dcvar2RST: Error: wrong data type, or stepped analysis.')
    return RST

def specs2RST(specs, types=[], position=0, label=''):
    """
    Converts a list with specifications into an RST CSVtable. 
    If a list with specification types is provided, it creates tables 
    for specified types only. By default, tables for all types will be created.
    
    :param specs: List with spec items. 
    :type specs:  list
    
    :param types: List with specification types to be placed on the html page,
                  defaults to [].
    :type types: str
    
    :return: html code
    :rtype: str
    """
    dictWithSpecs = specList2dict(specs)
    keys = sorted(list(dictWithSpecs.keys()))
    # Create an HTML dict with a key for each spec type
    typesDone = {}
    for key in keys:
        if dictWithSpecs[key].specType not in list(typesDone.keys()):
            typesDone[dictWithSpecs[key].specType] = [dictWithSpecs[key].rstLine()]
        else:
            typesDone[dictWithSpecs[key].specType].append(dictWithSpecs[key].rstLine())
    RST = ''
    # Copy rst code for desired type to output csvlines
    csvlines = []
    if len(types):
        for specType in types:
            try:
                linesList = typesDone[specType]
                name       = specType + ' specification'
                headerList = ["name", "Description", "minValue", "typValue", "maxValue", "units", "type"]
                RST += RSTcreateCSVtable(name, headerList, linesList, position=position, label=label + '-' +specType) + '\n'
            except BaseException:
                pass
    else:
        for specType in list(typesDone.keys()):
            try:
                linesList = typesDone[specType]
                name       = specType + ' specification'
                headerList = ["name", "Description", "minValue", "typValue", "maxValue", "units", "type"]
                RST += RSTcreateCSVtable(name, headerList, linesList, position=position, label=label + '-' +specType) + '\n'
            except BaseException:
                pass
    return RST

def eqn2RST(LHS, RHS, units='', position=0, label=''):
    spaces = makeSpaces(position)
    RST = spaces + '.. math::\n'
    if label != '':
        RST += spaces + '    :label: ' + label + '\n'
    RST += '\n'
    try:
        units = sp.latex(sp.sympify(units))
    except:
        units = ' '
    RST += spaces + '    ' + sp.latex(roundN(LHS)) + ' = ' + sp.latex(roundN(RHS)) + '\,\,\\left[\\mathrm{' + units + '}\\right]\n\n'
    return RST

def matrices2RST(Iv, M, Dv, position=0, label=''):
    spaces = makeSpaces(position)
    RST = spaces + '.. math::\n'
    if label != '':
        RST += spaces + '    :label: ' + label + '\n'
    RST += '\n'
    RST += spaces + '    ' + sp.latex(roundN(Iv)) + '=' + sp.latex(roundN(M)) + '\\cdot ' + sp.latex(roundN(Dv)) + '\n\n'
    return RST

def stepArray2rst(stepVars, stepArray, name, position=0, label=''):
    RST = ''
    numVars = len(stepVars)
    numRuns = len(stepArray[0])
    headerList = [sp.sympify(stepVar) for stepVar in stepVars]
    linesList = []
    for i in range(numRuns):
        line = []
        for j in range(numVars):
            line.append(stepArray[i][j])
        linesList.append(line)
    RST = RSTcreateCSVtable(name, headerList, linesList, position=position, label=label) + '\n\n'
    return RST

# Convert the dictionary into an RST data base to be imported for inline substitutions
# Save the output like the above functions and inport it in the document for
# substitutions

def save2RSTinline(vardict, fileName):
    RST = ''
    for key in vardict.keys():
        RST += '.. |' + key + '| replace:: ' + vardict[key] + '\n'
    saveRST(RST, fileName)

# Function saveRST() for including RST files in the report. The files are saved
# as: <ini.sphinxPath>SLiCAPdata/<fileName>.rst

def saveRST(RST, fileName):
    f = open(ini.sphinxPath + 'SLiCAPdata/' + fileName + '.rst', 'w')
    f.write(RST)
    f.close()
    
# Functions for generating nippets to be put in a dictionary for inline 
# substitutions in an RST file.

def expr2RST(expr, units=''):
    try:
        units = sp.latex(sp.sympify(units))
    except:
        pass
    RST = ':math:`' + sp.latex(roundN(expr)) + '\\, \\left[ \\mathrm{' + units + '} \\right]`'
    return RST

def eqn2RSTinline(LHS, RHS, units=''):
    try:
        units = sp.latex(sp.sympify(units))
    except SympifyError:
        pass
    RST = ':math:`' + sp.latex(roundN(LHS)) + '=' + sp.latex(roundN(RHS)) + '\\, \\left[ \\mathrm{' + units + '} \\right]`'
    return RST

# General non-public functions for creating table elements and sequences of spaces
    
def RSTcreateCSVtable(name, headerList, linesList, position=0, unitpos=None, label=''):
    RST = ''
    spaces = makeSpaces(position)
    if label != '':
        RST += spaces + '.. _' + label + ':\n'
    RST += spaces + '.. csv-table:: ' + name + '\n'
    RST += spaces + '    :header: '
    for item in headerList:
        if type(item) == str:
            RST += '"' + item + '", '
        else:
            RST += ':math:`' + sp.latex(roundN(item)) + '`, '
    RST = RST[:-2] + '\n'
    RST +=  spaces + '    :widths: auto\n'
    for line in linesList:
        i = 0
        RST += '\n' + spaces + '    '
        for item in line:
            if type(item) == str:
                RST += '"' + item + '", '
            elif i == unitpos:
                RST += ':math:`\\mathrm{' + sp.latex(item) + '}`, '
            else:
                RST += ':math:`' + sp.latex(roundN(sp.N(item))) + '`, '
            i += 1
        RST = RST[:-2]
    RST += '\n\n'
    return RST

def numRoots2RST(roots, Hz, pz):
    lineList = []
    i = 0
    for root in roots:
        i += 1
        realpart  = sp.re(root)
        imagpart  = sp.im(root)
        frequency = sp.Abs(root)
        Q = roundN(sp.N(frequency/(2*sp.Abs(realpart))))
        if Hz == True:
            realpart = roundN(sp.N(realpart/2/sp.pi))
            imagpart = roundN(sp.N(imagpart/2/sp.pi))
            frequency = roundN(sp.N(frequency/2/sp.pi))
            if Q <= 0.5:
                line = [sp.Symbol(pz + '_' + str(i)), realpart, imagpart, frequency, ]
            else:
                line = [sp.Symbol(pz + '_' + str(i)), realpart, imagpart, frequency, Q]
        lineList.append(line)
    return lineList

def symRoots2RST(roots, Hz, pz):
    lineList = []
    i = 0
    for root in roots:
        i += 1
        if Hz == True:
            line = [sp.Symbol(pz + '_' + str(i)), root/2/sp.pi]
        else:
            line = [sp.Symbol(pz + '_' + str(i)), root]
        lineList.append(line)
    return lineList

def makeSpaces(position):
    spaces = ''
    if position > 0:
        for i in range(position):
            spaces += ' '
    return spaces