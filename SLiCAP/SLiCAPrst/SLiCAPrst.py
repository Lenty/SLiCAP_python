#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 17:14:37 2023

@author: anton
"""
from SLiCAP.SLiCAPmath import fullSubs, roundN
from SLiCAP import ini
import sympy as sp
from shutil import copyfile

# Public functions for generating snippets that can be stored as RST files
# to be included by other RST files.

def netlist2RST(netlistFile, lineRange=None, firstNumber=None, position=0):
    """
    Converts a SLiCAP netlist into an RST string that can be included in
    a ReStructuredText document and returns this string.

    :param netlistFile: Name of the netlist file that resides in the
                        ini.circuitPath directory
    :type netListFile: str

    :param lineRange: Range of lines to be displayed; e.g. '1-7,10,12'. Defaults
                      to None (display all lines)
    :type lineRange: str

    :param firstNumber: Number of the first line to be displayed
    :type firstNumber: int, float, str

    :param position: Number of spaces indention from the left margin, defaults to 0
    :type position: int

    :return: RST snippet to be included in a ReStructuredText document
    :rtype: str
    """
    copyfile(ini.circuitPath + netlistFile, ini.sphinxPath + 'SLiCAPdata/' + netlistFile)
    spaces = makeSpaces(position)
    RST = spaces + '.. literalinclude:: ../SLiCAPdata/' + netlistFile + '\n'
    RST += spaces + '    :linenos:\n'
    if lineRange != None:
        RST += spaces + '    :lines: ' + lineRange + '\n'
        if firstNumber != None:
            RST += spaces + '    :lineno-start: ' + str(firstNumber) + '\n'
    return RST

def elementData2RST(circuitObject, label='', append2caption='', position=0):
    """
    Creates and returns an RST table snippet that can be included in a ReStructuredText document.
    The table comprises the data of all elements of the expanded nelist of <circuitObject>.

    The caption reads 'Expanded netlist of: <circuitObject.title>. <append2caption>.

    A label can be given as reference.

    :param circuitObject: SLiCAP circuit object.
    :type circuitObject: SLiCAP.SLiCAPprotos.circuit

    :param label: Reference to this table, defaults to ''
    :type label: str

    :param append2caption: Test string that will be appended to the caption,
                           Defaults to ''
    :type append2caption: str

    :param position: Number of spaces indention from the left margin, defaults to 0
    :type position: int

    :return: RST snippet to be included in a ReStructuredText document
    :rtype: str
    """
    spaces     = makeSpaces(position)
    name       = 'Expanded netlist of: ' + circuitObject.title + '. ' + append2caption
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

def parDefs2RST(circuitObject, label='', append2caption='', position=0):
    """
    Creates and returns an RST table snippet that can be included in a ReSturucturedText document.
    The table comprises the parameter definitions of <circuitObject>.

    The caption reads 'Parameter defnitions in: : <circuitObject.title>. <append2caption>.

    A label can be given as reference.

    :param circuitObject: SLiCAP circuit object.
    :type circuitObject: SLiCAP.SLiCAPprotos.circuit

    :param label: Reference to this table, defaults to ''
    :type label: str

    :param append2caption: Test string that will be appended to the caption,
                           Defaults to ''
    :type append2caption: str

    :param position: Number of spaces indention from the left margin, defaults to 0
    :type position: int

    :return: RST snippet to be included in a ReSturucturedText document
    :rtype: str
    """
    if len(circuitObject.parDefs) > 0:
        spaces     = makeSpaces(position)
        name       = 'Parameter defnitions in: ' + circuitObject.title + '. ' + append2caption
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

def params2RST(circuitObject, label='', append2caption='', position=0):
    """
    Creates and returns an RST table snippet that can be included in a ReStructuredText document.
    The table comprises a column with names of undefined parameters of <circuitObject>.

    The caption reads 'Undefined parameters in: : <circuitObject.title>. <append2caption>.

    A label can be given as reference.

    :param circuitObject: SLiCAP circuit object.
    :type circuitObject: SLiCAP.SLiCAPprotos.circuit

    :param label: Reference to this table, defaults to ''
    :type label: str

    :param append2caption: Test string that will be appended to the caption,
                           Defaults to ''
    :type append2caption: str

    :param position: Number of spaces indention from the left margin, defaults to 0
    :type position: int

    :return: RST snippet to be included in a ReStructuredText document
    :rtype: str
    """
    if len(circuitObject.params) > 0:
        spaces     = makeSpaces(position)
        name       = 'Undefined parameters in: ' + circuitObject.title + '. ' + append2caption
        headerList = ["Name"]
        linesList   = []
        for parName in circuitObject.params:
            lineList.append([parName])
        RST = RSTcreateCSVtable(name, headerList, linesList, position=position, label=label)
    else:
        RST = '**No undefined parameters in: ' +  circuitObject.title + '**\n\n'
    return RST

def pz2RST(resultObject, label = '', append2caption='', position=0):
    """
    Creates and return an RST table with poles, zeros, or poles and zeros that
    can be included in a ReStructuredText document. If the data type is 'pz' the zero-
    frequency value of the gain will be displayed in the caption of the table.

    The caption reads as follows:

    - data type = 'poles': 'Poles of: <resultObject.gainType>. <append2caption>'
    - data type = 'zeros': 'Zeros of: <resultObject.gainType>. <append2caption>'
    - data type = 'pz': 'Poles and zeros of: <resultObject.gainType>; DC value = <resultObject,DCvalue>. <append2caption>.'

    A label can be given as reference.

    :param label: Reference to this table, defaults to ''
    :type label: str

    :param append2caption: Test string that will be appended to the caption,
                           Defaults to ''
    :type append2caption: str

    :param position: Number of spaces indention from the left margin, defaults to 0
    :type position: int

    :return: RST snippet to be included in a ReStructuredText document
    :rtype: str
    """
    RST = ''
    if resultObject.errors != 0:
        print("pz2RST: Errors found in instruction.")
    elif resultObject.dataType != 'poles' and resultObject.dataType != 'zeros' and resultObject.dataType != 'pz':
        print("pz2RST: Error: 'pz2RST()' expected dataType: 'poles', 'zeros', or 'pz', got: '{0}'.".format(instObj.dataType))
    elif resultObject.step == True :
        print("pz2RST: Error: parameter stepping not implemented for 'pz2RST()'.")
    else:
        if resultObject.dataType == 'poles':
            name = 'Poles of: ' + resultObject.gainType + '. ' + append2caption
        elif resultObject.dataType == 'zeros':
            name = 'Zeros of: ' + resultObject.gainType + '. ' + append2caption
        elif resultObject.dataType == 'pz':
            name = 'Poles and zeros of: ' + resultObject.gainType + '. DC gain = :math:`' + sp.latex(roundN(resultObject.DCvalue)) + '`. ' + append2caption
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

def noiseContribs2RST(resultObject, label='', append2caption='', position=0):
    """
    Creates and returns an RST table snippet that can be included in a ReStructuredText document.

    The table comprises the values of the noise sources and their contributions
    to the detector-referred noise and the source-referred noise. The latter
    only if a signal source has been specified.

    The caption reads 'Noise contributions. '<append2caption>.

    A label can be given as reference.

    :param resultObject: SLiCAP execution result object.
    :type resultObject: SLiCAP.SLiCAPprotos.allResults

    :param label: Reference to this table, defaults to ''
    :type label: str

    :param append2caption: Test string that will be appended to the caption,
                           Defaults to ''
    :type append2caption: str

    :param position: Number of spaces indention from the left margin, defaults to 0
    :type position: int

    :return: RST snippet to be included in a ReStructuredText document
    :rtype: str
    """
    if resultObject.dataType == 'noise' and resultObject.step == False:
        detunits = sp.sympify(resultObject.detUnits + '**2/Hz')
        if resultObject.srcUnits != None:
            srcunits = sp.sympify(resultObject.srcUnits + '**2/Hz')
        # Add a table with noise contributions
        linesList = []
        headerList = ['', 'Value' , 'Units']
        name = "Source contributions. " + append2caption
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
        RST = RSTcreateCSVtable(name, headerList, linesList, unitpos=2, label=label)
    else:
        RST = ''
        print('noise2RST: Error: wrong data type, or stepped analysis.')
    return RST

def dcvarContribs2RST(resultObject, label='', append2caption='', position=0):
    """
    Creates and returns an RST table snippet that can be included in a ReStructuredText document.

    The table comprises the values of the dcvar sources and their contributions
    to the detector-referred DC variance and the source-referred DC variance. The latter
    only if a signal source has been specified.

    The caption reads 'Source contributions. '<append2caption>.

    A label can be given as reference.

    :param resultObject: SLiCAP execution result object.
    :type resultObject: SLiCAP.SLiCAPprotos.allResults

    :param label: Reference to this table, defaults to ''
    :type label: str

    :param append2caption: Test string that will be appended to the caption,
                           Defaults to ''
    :type append2caption: str

    :param position: Number of spaces indention from the left margin, defaults to 0
    :type position: int

    :return: RST snippet to be included in a ReStructuredText document
    :rtype: str
    """
    if resultObject.dataType == 'dcvar' and resultObject.step == False:
        detunits = sp.sympify(resultObject.detUnits + '**2')
        if resultObject.srcUnits != None:
            srcunits = sp.sympify(resultObject.srcUnits + '**2')
        # Add a table with dcvar contributions
        linesList = []
        headerList = ['', 'Value' , 'Units']
        name = "Source contributions. " + append2caption
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
        RST = RSTcreateCSVtable(name, headerList, linesList, unitpos=2, label=label)
    else:
        RST = ''
        print('dcvar2RST: Error: wrong data type, or stepped analysis.')
    return RST

def specs2RST(specs, specType='', label='', caption='', position=0):
    """
    Creates and returns an RST table snippet from a list with specItem objects.
    This table snippet can be included in a ReStructuredText document.

    :param specs: List with spec items.
    :type specs:  list

    :param specType: Type of specification.
    :type types: str

    :param label: Reference to this table, defaults to ''.
    :type label: str

    :param caption: Caption of the table, defaults to ''.
    :type caption: str

    :param position: Number of spaces indention from the left margin, defaults to 0
    :type position: int

    :return: RST snippet to be included in a ReStructuredText document.
    :rtype: str
    """
    linesList  = []
    headerList = ["Name", "Description", "minValue", "typValue", "maxValue", "units"]
    for specItem in specs:
        if specItem.specType.lower()==specType.lower():
            linesList.append(specItem.specLine())
    if len(linesList) > 0:
        RST = RSTcreateCSVtable(caption, headerList, linesList, label=label, position=position) + '\n'
    else:
        RST =  "**Found no specifications of type: " + specType + ".**\n\n"
    return RST

def eqn2RST(LHS, RHS, units='', position=0, label=''):
    """
    Returns an RST snippet of a displayed equation with dimension and reference
    label.

    :param RHS: Right hand side of the equation.
    :type RHS: str, sympy.Expression, or sympy.Symbol

    :param LHS: Left hand side of the equation.
    :type LHS: str, sympy.Expression, or sympy.Symbol

    :param units: Dimension
    :type units: str

    :param label: Reference label
    :type label: str

    :param position: Number of spaces indention from the left margin, defaults to 0
    :type position: int

    :return: RST snippet to be included in a ReStructuredText document.
    :rtype: str
    """
    spaces = makeSpaces(position)
    RST = spaces + '.. math::\n'
    if label != '':
        RST += spaces + '    :label: ' + label + '\n'
    RST += '\n'
    try:
        units = sp.latex(sp.sympify(units))
    except:
        units = ''
    RST += spaces + '    ' + sp.latex(roundN(LHS)) + ' = ' + sp.latex(roundN(RHS))
    if units != '':
        RST += '\,\,\\left[\\mathrm{' + units + '}\\right]\n\n'
    return RST

def matrices2RST(Iv, M, Dv, position=0, label=''):
    """
    Returns an RST snippet of the matrix equation Iv = M.Dv,

    A label can be given for reference.

    :param Iv: (n x 1) matrix with independent variables.
    :type Iv: sympy.Matrix

    :param M: (n x n) matrix.
    :type M: sympy.Matrix

    :param Dv: (n x 1) matrix with dependent variables.
    :type Dv: sympy.Matrix

    :param position: Number of spaces indention from the left margin, defaults to 0
    :type position: int

    :return: RST snippet to be included in a ReStructuredText document.
    :rtype: str
    """
    spaces = makeSpaces(position)
    RST = spaces + '.. math::\n'
    if label != '':
        RST += spaces + '    :label: ' + label + '\n'
    RST += '\n'
    RST += spaces + '    ' + sp.latex(roundN(Iv)) + '=' + sp.latex(roundN(M)) + '\\cdot ' + sp.latex(roundN(Dv)) + '\n\n'
    return RST

def stepArray2rst(stepVars, stepArray, label='', caption='', position=0):
    """
    Creates and returns an RST table snippet that can be included in a ReStructuredText document.

    The table shows the step variables and their values as defined for array-type
    stepping of instructions.

    :param stepVars: List with step variables for array type stepping
                     (SLiCAPinstruction.instruction.stepVars)
    :type stepVars: List

    :param stepArray: List of lists: (SLiCAPinstruction.instruction.stepArray)
    :type stepArray: list

    :param label: Reference lable for this table
    :type label: str

    :param caption: Table caption
    :type caption: str

    :param position: Number of spaces indention from the left margin, defaults to 0
    :type position: int

    :return: RST snippet to be included in a ReStructuredText document.
    :rtype: str
    """
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
    RST = RSTcreateCSVtable(caption, headerList, linesList, position=position, label=label) + '\n\n'
    return RST

def coeffsTransfer2RST(transferCoeffs, label = '', append2caption='', position=0):
    """
    Creates and returns an RST table snippet that can be included in a
    ReStuctrutedText document.

    The table comprises the normalized coefficients of the numerator and
    the denominator as listed in transferCoeffs.

    The normalization factor (Gain) is added to the caption.

    A label can be given as reference.

    :param transferCoeffs: List with:

                           #. gain
                           #. list with numerator coefficients
                           #. list with denominator coefficients

                           Can be obtained with coeffsTransfer()

    :type transferCoeffs: list

    :param label: Reference lable for this table
    :type label: str

    :param append2caption: String that will be appended to the caption.
    :type append2caption: str

    :param position: Number of spaces indention from the left margin, defaults to 0
    :type position: int

    :return: RST snippet to be included in a ReStructuredText document.
    :rtype: str
    """
    (gain, numerCoeffs, denomCoeffs) = transferCoeffs
    caption = ' Gain factor: ' + sp.latex(roundN(gain)) + '. '
    headerList = ['Coeff', 'Value']
    linesList = []
    for i in range(len(numerCoeffs)):
        linesList.append([sp.sympify('n_' + str(i)), numerCoeffs[i]])
    for i in range(len(denomCoeffs)):
        linesList.append([sp.sympify('d_' + str(i)), denomCoeffs[i]])
    caption += ':math:`n_i` = numerator coefficient of i-th order, :math:`d_i` = denominator coefficient of i-th order. '
    caption += append2caption
    RST = RSTcreateCSVtable(caption, headerList, linesList, label=label, position=position)
    return RST

def slicap2RST(scriptFile, firstLine=None, lineRange=None):
    """
    Converts a SLiCAP script file into an RST string that can be included in
    a ReStructuredText document and returns this string.

    :param scriptFile: Name of the script file that resides in the
                       ini.projectPath directory
    :type scriptFile: str

    :param lineRange: Range of lines to be displayed; e.g. '1-7,10,12'. Defaults
                      to None (display all lines)
    :type lineRange: str

    :param firstNumber: Number of the first line to be displayed
    :type firstNumber: int, float, str

    :return: RST snippet to be included in a ReStructuredText document
    :rtype: str
    """
    copyfile(ini.projectPath + scriptFile, ini.sphinxPath + 'SLiCAPdata/' + scriptFile)
    spaces = makeSpaces(position)
    RST = spaces + '.. literalinclude:: ../SLiCAPdata/' + scriptFile + '\n'
    RST += spaces + '    :linenos:\n'
    if lineRange != None:
        RST += spaces + '    :lines: ' + lineRange + '\n'
        if firstNumber != None:
            RST += spaces + '    :lineno-start: ' + str(firstNumber) + '\n'
    return RST

# Functions for generating nippets to be put in a dictionary for inline
# substitutions in an RST file.

def expr2RST(expr, units=''):
    """
    Returns an RST snippet for inline subsitution of an expression in a
    ReStructuredText document.

    :param expr: sympy expression for inline substitution.
    :type expr: sympy.Expression

    :param units: units or dimension, defaults to ''
    :type units: str

    :return: RST snippet for inline substitution in a ReStructuredText document.
    :rtype: str
    """
    try:
        units = sp.latex(sp.sympify(units))
    except:
        units=''
    RST = ':math:`' + sp.latex(roundN(expr))
    if units != '':
        RST += '\\, \\left[ \\mathrm{' + units + '} \\right]` '
    else:
        RST += '` '
    return RST

def eqn2RSTinline(LHS, RHS, units=''):
    """
    Returns an RST snippet for inline subsitution of an equation in a
    ReStructuredText document.

    :param LHS: Left hand side of the equation.
    :type LHS: sympy.Expression, str

    :param RHS: Right hand side of the equation.
    :type RHS: sympy.Expression, str

    :param units: units or dimension, defaults to ''
    :type units: str

    :return: RST snippet for inline substitution in a ReStructuredText document.
    :rtype: str
    """
    try:
        units = sp.latex(sp.sympify(units))
    except:
        units=''
    RST = ':math:`' + sp.latex(roundN(LHS)) + '=' + sp.latex(roundN(RHS))
    if units != '':
        RST += '\\, \\left[ \\mathrm{' + units + '} \\right]` '
    else:
        RST += '` '
    return RST

# Convert the dictionary into an RST data base to be imported for inline substitutions
# Save the output like the above functions and inport it in the document for
# substitutions

def save2RSTinline(vardict):
    """
    Saves the key-value pairs of 'vardict' in the CSV file:

    <ini.sphinxPath>SLiCAPdata/RSTsubstitutions.rst

    :param vardict: Dictionary with inline RST subsitutions
    :type vardict: dict

    :return: None
    :rtype: NoneType
    """
    RST = ''
    for key in vardict.keys():
        RST += '.. |' + key + '| replace:: ' + vardict[key] + '\n'
    saveRST(RST, 'RSTsubstitutions')

# Function saveRST() for including RST files in the report.

def saveRST(RST, fileName):
    """
    Saves an RST snippet for inclusion in a ReStructuredText document in:

    <ini.latexPath>SLiCAdata/<fileName>.rst

    :param RST: RST snippet.
    :type RST: str

    :param fileName: File name
    :type fileName: str

    :return: None
    :rtype: NoneType
    """
    f = open(ini.sphinxPath + 'SLiCAPdata/' + fileName + '.rst', 'w')
    f.write(RST)
    f.close()

# Non-public functions for creating table snippets

def RSTcreateCSVtable(name, headerList, linesList, position=0, unitpos=None, label=''):
    """
    Creates and returns an RST table snippet that can be included in a
    ReStructuredText document.

    A label can be given as reference. The name is displayed as caption.

    :param name: Table caption
    :type name: str

    :param headerList: List with column headers.
    :type headerList: list with strings

    :param linesList: List with lists of table data for each table row
    :type linesList: list

    :param unitpos: Position of column with units (will be typesetted with mathrm)
    :type unitpos: int, str

    :param label: Table reference label
    :type label: str

    :return: RST snippet to be included in a ReStructuredText document
    :rtype: str
    """
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
    """
    Returns a list of lists with row data for the creation of an RST table
    with numeric poles or zeros.

    :param roots: List with numeric roots
    :type roots: List with (complex) numbers

    :param Hz: True if frequencies must be displayed in Hz, False for rad/s.
    :type Hz: Bool

    :param pz: Identifier prefix: 'p' ofr poles 'z' for zeros.
    :type pz: str

    :return: List of lists with data of poles or zeros
    :rtype: List of lists
    """
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
    """
    Returns a list of lists with row data for the creation of an RST table
    with symbolic poles or zeros.

    :param roots: List with symbolic roots
    :type roots: List with sympy expressions

    :param Hz: True if frequencies must be displayed in Hz, False for rad/s.
    :type Hz: Bool

    :param pz: Identifier prefix: 'p' ofr poles 'z' for zeros.
    :type pz: str

    :return: List of lists with data of poles or zeros
    :rtype: List of lists
    """
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

def makeSpaces(n):
    """
    Creates and returns a string with <n> spaces.

    :param n: Number of spaces
    :type n: int

    :return: String with <n> spaces
    :rtype: str
    """
    spaces = ''
    if n > 0:
        for i in range(n):
            spaces += ' '
    return spaces