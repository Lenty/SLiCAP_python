#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:36:05 2020

@author: anton
"""

from SLiCAPpythonMaxima import *

HTMLINSERT   = '<!-- INSERT -->' # pattern to be replaced in html files
HTMLINDEX    = 'index.html'      # will be set by initProject()
HTMLPREFIX   = ''                # will be set by checkCircuit()
HTMLPAGE     = ''                # will be set by htmlPage()
HTMLLABELS   = {}                # label dictionary:
                                 #      key = label
                                 #      value = page
HTMLEQLABELS = {}                # equation label dictionary:
                                 #      key   = label
                                 #      value = page
HTMLPAGES    = []                # list with file names of html pages# Get the project path 

# Initialize HTML globals
ini.htmlIndex    = ''
ini.htmlPrefix   = ''
ini.htmlPage     = ''
ini.htmlLabels   = {}
ini.htmlEqLabels = {}
ini.htmlPages    = []

def startHTML(projectName):
    """
    Creates main project index page.
    """
    global HTMLINDEX, HTMLPAGES
    ini.htmlIndex = 'index.html'
    toc = '<h2>Table of contents</h2>'
    HTML = HTMLhead(projectName) + toc + '<ol>' + HTMLINSERT + '</ol>' + HTMLfoot(HTMLINDEX)
    f = open(ini.htmlPath + ini.htmlIndex, 'w')
    f.write(HTML)
    f.close()
    ini.htmlPages.append(ini.htmlIndex)
    return

def HTMLhead(pageTitle):
    """
    Returns the html page head, ignores MathJax settings in SLiCAPini.py
    """
    HTML = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\n'
    HTML += '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'
    HTML += '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n'
    HTML += '<head><meta http-equiv="Content-Type" content="text/html;charset=iso-8859-1"/>\n'
    HTML += '<meta name="Language" content="English"/>\n'
    HTML += '<title>"' + pageTitle + '"</title><link rel="stylesheet" href="css/slicap.css">\n'
    HTML += '<script>MathJax = {tex:{tags: \'ams\', inlineMath:[[\'$\',\'$\'],]}, svg:{fontCache:\'global\'}};</script>\n'
    HTML += '<script type="text/javascript" id="MathJax-script" async  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>\n'
    HTML += '</head><body><div id="top"><h1>' + pageTitle + '</h1></div>\n'
    if MATHJAXLOCAL == True:
        print 'MathJax version 3 is not installed. Only web access is supported!'
        # see http://docs.mathjax.org/en/latest/web/hosting.html
    return(HTML)
    
def HTMLfoot(indexFile):
    """
    Returns html page footer with link to 'indexFile'.
    """
    idx = indexFile.split('.')[0]
    HTML = '\n<div id="footnote">\n'
    HTML += '<p>Go to <a href="' + indexFile + '">' + idx + '</a></p>\n'
    HTML += '<p>SLiCAP: Symbolic Linear Circuit Analysis Program, Version 1.0 &copy 2009-2020 SLiCAP development team</p>\n'
    HTML += '<p>For documentation, examples, support, updates and courses please visit: <a href="http://www.analog-electronics.eu">analog-electronics.eu</a></p>\n'
    HTML += '</div></body></html>'
    return(HTML)

def insertHTML(fileName, html):
    """
    Inserts html in the file specified by 'fileName' at the location of
    HTMLINSERT.
    
    ToDo: check if this file exists.
    """
    HTML = readFile(fileName)
    HTML = HTML.replace(HTMLINSERT, html + HTMLINSERT)
    writeFile(fileName, HTML)
    return

def readFile(fileName):
    """
    Returns the contents of a file as a string.
    
    ToDo: check if this file exists.
    """
    f = open(fileName, 'r')
    txt = f.read()
    f.close()
    return txt

def writeFile(fileName, txt):
    """
    Writes a text string to a file.
    
    ToDo: check if this file exists.
    """
    f = open(fileName, 'w')
    f.write(txt)
    f.close()
    return

### User Functions ###########################################################

def htmlPage(pageTitle, index = False):
    """
    Creates an HTML page with the title in the title bar. If index==True
    then the page will be used as new index page, else a link to this page will
    be placed on the current index page.
    The global HTMLINDEX holds the name of the current index page.
    """
    if index == True:
        # The page is a new index page
        fileName = ini.htmlPrefix + 'index.html'
        # Place link on old index page
        href = '<li><a href="' + fileName +'">' + pageTitle + '</a></li>'
        insertHTML(ini.htmlPath + ini.htmlIndex, href)
        # Create the new HTML file
        toc = '<h2>Table of contents</h2>'
        HTML = HTMLhead(pageTitle) + toc + '<ol>' + HTMLINSERT + '</ol>' + HTMLfoot(HTMLINDEX)
        writeFile(ini.htmlPath + fileName, HTML)
        # Make this page the new index page
        ini.htmlIndex = fileName
    else:
        fileName = ini.htmlPrefix + '-'.join(pageTitle.split()) + '.html'
        # Place link on the current index page
        href = '<li><a href="' + fileName +'">' + pageTitle + '</a></li>'
        insertHTML(ini.htmlPath + ini.htmlIndex, href)
        # Create the new HTML page
        HTML = HTMLhead(pageTitle) + HTMLINSERT + HTMLfoot(HTMLINDEX)
        writeFile(ini.htmlPath + fileName, HTML)
    # Make this page the active HTML page
    ini.htmlPage = fileName
    ini.htmlPages.append(fileName)
    # Remove double entries in ini.htmlPages
    ini.htmlPages = list(set(ini.htmlPages))
    return(HTML)
    
def head2html(headText, label=''):
    """
    Placed a level-2 heading on the active HTML page.
    """
    if label != '':
        ini.htmlLabels[label] = ini.htmlPage
        label = '<a id="' + label + '"></a>'
    html = '<h2>' + label + headText + '</h2>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    return

def head3html(headText, label=''):
    """
    Placed a level-3 heading on the active HTML page.
    """
    if label != '':
        ini.htmlLabels[label] = ini.htmlPage
        label = '<a id="' + label + '"></a>'
    html = '<h3>' + label + headText + '</h3>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    return

def text2html(txt):
    """
    Places txt on the active HTML page.
    """
    html = '<p>' + txt + '</p>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    return

def netlist2html(fileName, label=''):
    """
    Places the netlist of HTMLCIRCUIT on HTMLPAGE
    """
    try:
        if label != '':
            ini.htmlLabels[label] = ini.htmlPage
            label = '<a id="' + label + '"></a>'
        netlist = readFile(ini.circuitPath + fileName)
        html = '<h2>' + label + 'Netlist: ' + fileName + '</h2>\n<pre>' + netlist + '</pre>\n'
        insertHTML(ini.htmlPath + ini.htmlPage, html)
    except:
        print "Error: could not open netlist file: '%s'."%(fileName)
    return

def elementData2html(circuitObject, label = '', caption = ''):
    """
    Displays element data on the active html page:
        - refDes
        - nodes
        - referenced elements
        - parameters with symbolic and numeric values
    ToDo:
        Add HTML label.
    """
    if label != '':
        ini.htmlLabels[label] = ini.htmlPage
        label = '<a id="' + label + '"></a>'
    caption = "<caption>Table: Element data of expanded netlist '%s'<br>%s</caption>\n"%(circuitObject.title, caption)
    html = '%s<table>%s\n'%(label, caption)
    html += '<tr><th class="left">RefDes</th><th class="left">Nodes</th><th class="left">Refs</th><th class="left">Model</th><th class="left">Param</th><th class="left">Symbolic</th><th class="left">Numeric</th></tr>\n'
    elementNames = circuitObject.elements.keys()
    for el in sorted(elementNames):
        elmt = circuitObject.elements[el]
        html += '<tr><td class="left">' + elmt.refDes + '</td><td class = "left">'
        for node in elmt.nodes:
            html += node + ' '
        html += '</td><td class = "left">'
        for ref in elmt.refs:
            html += ref + ' '
        html += '</td><td class = "left">' + elmt.model +'</td>\n'
        parNames = elmt.params.keys()
        if len(parNames) == 0:
            html += '<td></td><td></td><td></td><tr>'
        else:
            i = 0
            for param in parNames:
                symValue = '$' + sp.latex(sp.N(elmt.params[param], DISP)) +'$'
                numValue = '$' + sp.latex(sp.N(fullSubs(elmt.params[param], circuitObject.parDefs), DISP)) + '$'
                if i == 0:
                    html += '<td class="left">' + param + '</td><td class="left">' + symValue + '</td><td class="left">' + numValue + '</td></tr>\n'
                else:
                    html += '<tr><td></td><td></td><td></td><td></td><td class="left">' + param + '</td><td class="left">' + symValue + '</td><td class="left">' + numValue + '</td></tr>\n'
                i += 1
    html += '</table>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    return

def params2html(circuitObject, label = '', caption = ''):
    """
    Displays all parameters with definitions and numeric value.
    """
    if label != '':
        ini.htmlLabels[label] = ini.htmlPage
        label = '<a id="' + label + '"></a>'
    caption = "<caption>Table: Parameter definitions in '%s'.<br>%s</caption>\n"%(circuitObject.title, caption)
    html = '%s<table>%s\n'%(label, caption)
    html += '<tr><th class="left">Name</th><th class="left">Symbolic</th><th class="left">Numeric</th></tr>\n'
    for par in circuitObject.parDefs.keys():
        parName = '$' + sp.latex(par) + '$'
        symValue = '$' + sp.latex(sp.N(circuitObject.parDefs[par], DISP)) + '$'
        numValue = '$' + sp.latex(sp.N(fullSubs(circuitObject.parDefs[par], circuitObject.parDefs), DISP)) + '$'
        html += '<tr><td class="left">' + parName +'</td><td class="left">' + symValue + '</td><td class="left">' + numValue + '</td></tr>\n'
    html += '</table>\n'
    if len(circuitObject.params) > 0:
        caption = "<caption>Table: Parameters without definition in '%s.<br>%s</caption>\n"%(HTMLCIRCUIT.title, caption)
        html += '<table>%s\n'%(caption)
        html += '<table><tr><th class="left">Name</th></tr>\n'
        for par in circuitObject.params:
            parName = '$' + sp.latex(par) + '$'
            html += '<tr><td class="left">' + parName +'</td></tr>\n'
        html += '</table>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    return

def img2html(fileName, width, label = '', caption = ''):
    """
    Copies the image file to the 'img.' subdirectory of the 'html/' directory
    set by HTMLPATH in SLiCAPini.py and creates a link to this file on the 
    active html page.
    """
    if label != '':
        ini.htmlLabels[label] = ini.htmlPage
        label = '<a id="' + label + '"></a>'
    try:
        cp(ini.imgPath + fileName, ini.htmlPath + 'img/' + fileName)
    except:
        print("Error: could not copy: '%s'."%(fileName))
    html = '<figure>%s<img src="img/%s" alt="%s" style="width:%spx">\n'%(label, fileName, caption, width)
    if caption != '':
        html+='<figcaption>Figure: %s<br>%s</figcaption>\n'%(fileName, caption)
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    return

def csv2html(fileName, label = '', separator = ',', caption = ''):
    """
    Displays the contents of a csv file as a table on the active HTML page.
    """
    if label != '':
        ini.htmlLabels[label] = ini.htmlPage
        label = '<a id="' + label + '"></a>'
    caption = '<caption>Table: %s<br>%s.</caption>'%(fileName, caption)
    html = '%s<table>%s'%(label, caption)
    csvLines = readFile(ini.csvPath + fileName).splitlines()
    for i in range(len(csvLines)):
        cells = csvLines[i].split(separator)
        html += '<tr>'
        if i == 0:
            for cell in cells:
                html += '<th>%s</th>'%(cell)
        else:
            for cell in cells:
                html += '<td>%s</td>'%(cell)
        html += '</tr>\n'
    html += '</table>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    return

def expr2html(expr, units = ''):
    """
    Inline display of an expression optional with units.
    """
    if isinstance(expr, tuple(sp.core.all_classes)):
        if units != '':
            units = '\\left[\\mathrm{' + sp.latex(sp.sympify(units)) + '}\\right]'
        html = '$' + sp.latex(sp.N(expr, DISP)) + units + '$'
        insertHTML(ini.htmlPath + ini.htmlPage, html)
        return
    else:
        print "Error: expr2html, expected a Sympy expression."

def eqn2html(arg1, arg2, units = '', label = ''):
    """
    Displays an equation on the active HTML page'.
    
    ToDo:
        Add HTML label.
    """
    if arg1 == None or arg2 == None:
        return
    eqlabel = label
    if not isinstance(arg1, tuple(sp.core.all_classes)):
        arg1 = sp.sympify(arg1)
    if not isinstance(arg2, tuple(sp.core.all_classes)):
        arg2 = sp.sympify(arg2)
    if units != '':
        units = '\\,\\left[ \\mathrm{' + sp.latex(sp.sympify(units)) + '}\\right]'
    if label != '':
        ini.htmlLabels[label] = ini.htmlPage
        ini.htmlEqLabels[label]= ini.htmlPage
        eqlabel = '\\label{' + label + '}\n'
        label   = '<a id="'+ label +'"></a>\n'
    html = label + '\\begin{equation}\n' + sp.latex(sp.N(arg1, DISP)) + '=' + sp.latex(sp.N(arg2, DISP)) + units + '\n'
    html += eqlabel
    html += '\\end{equation}\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    return

def matrices2html(instrObj, label = ''):
    """
    Displays the MNA equation on the active HTML page.
    
    ToDo:
        Add HTML label.
    """
    eqlabel = ''
    if instrObj.errors != 0:
        print "Errors found during executeion."
        return
    elif instrObj.dataType != 'matrix':
        print "Error: expected dataType 'matrix' for 'matrices2html()', got: '%s'."%(instrObj.dataType)
        return
    try:
        (Iv, M, Dv) = (instrObj.results.Iv, instrObj.results.M, instrObj.results.Dv)
        Iv = sp.latex(sp.N(Iv, DISP))
        M  = sp.latex(sp.N(M,  DISP))
        Dv = sp.latex(sp.N(Dv, DISP))
        if label != '':
            ini.htmlLabels[label] = ini.htmlPage
            ini.htmlEqLabels[label]= ini.htmlPage
            eqlabel = '\\label{' + label + '}\n'
            label = '<a id="' + label + '"></a>'
        html = '<h3>' + label + 'Matrix equation:</h3>\n'
        html += '\\begin{equation}\n' + Iv + '=' + M + '\\cdot' + Dv + '\n'
        html += eqlabel
        html += '\\end{equation}\n'
        insertHTML(ini.htmlPath + ini.htmlPage, html)
    except:
        print "Error: unexpected input for 'matrices2html()'."
    return

def pz2html(instObj, label = ''):
    """
    Displays the DC transfer, and tables with poles and zeros on the active 
    HTML page.
    """
    if instObj.errors != 0:
        print "Errors found in instruction."
        return
    elif instObj.dataType != 'poles' and instObj.dataType != 'zeros' and instObj.dataType != 'pz':
        print "Error: 'pz2html()' expected dataType: 'poles', 'zeros', or 'pz', got: '%s'."%(instObj.dataType)
        return
    elif instObj.step == True :
        print "Error: parameter stepping not yet implemented for 'pz2html()'."
        return  
    if label != '':
        ini.htmlLabels[label] = ini.htmlPage
        label = '<a id="' + label + '"></a>'
    (poles, zeros, DCgain) = (instObj.results.poles, instObj.results.zeros, instObj.results.DCvalue)
    if instObj.dataType == 'poles':
        headTxt = 'Poles '
    elif instObj.dataType == 'zeros':
        headTxt = 'Zeros '
    elif instObj.dataType == 'pz':
        headTxt = 'PZ '
    html = '<h2>' + label + headTxt + ' analysis results</h2>\n'
    html += '<h3>Gain type: %s</h3>'%(instObj.gainType)
    if DCgain != None and instObj.dataType =='pz':
        html += '\n' + '<p>DC gain = ' + str(sp.N(DCgain, DISP)) + '</p>\n'
    elif instObj.dataType =='pz':
        html += '<p>DC gain could not be determined.</p>\n'
    if HZ == True:
        unitsM = 'Mag [Hz]'
        unitsR = 'Re [Hz]'
        unitsI = 'Im [Hz]'
    else:
        unitsM = 'Mag [rad/s]'
        unitsR = 'Re [rad/s]'
        unitsI = 'Im [rad/s]'
    if len(poles) > 0 and instObj.dataType == 'poles' or instObj.dataType == 'pz':
        html += '<table><tr><th>pole</th><th>' + unitsR + '</th><th>' + unitsI + '</th><th>' + unitsM + '</th><th>Q</th></tr>\n'
        for i in range(len(poles)):
            p = poles[i]
            if HZ == True:
                p  = p/2/sp.pi
            Re = sp.re(p)
            Im = sp.im(p)
            F  = sp.sqrt(Re**2+Im**2)
            if Im != 0:
                Q = str(sp.N(F/2/abs(Re), DISP))
            else:
                Q = ''
            F  = str(sp.N(F, DISP))
            Re = str(sp.N(Re, DISP))
            if Im != 0.:
                Im = str(sp.N(Im, DISP))
            else:
                Im = ''
            name = 'p<sub>' + str(i + 1) + '</sub>'
            html += '<tr><td>' + name + '</td><td>' + Re + '</td><td>' + Im + '</td><td>' + F + '</td><td>' + Q +'</td></tr>\n'
        html += '</table>\n'
    elif instObj.dataType == 'poles' or instObj.dataType == 'pz':
        html += '<p>No poles found.</p>\n'
    if len(zeros) > 0 and instObj.dataType == 'zeros' or instObj.dataType == 'pz':
        html += '<table><tr><th>zero</th><th>' + unitsR + '</th><th>' + unitsI + '</th><th>' + unitsM + '</th><th>Q</th></tr>\n'
        for i in range(len(zeros)):
            z = zeros[i]
            if HZ == True:
                z = z/2/sp.pi
            Re = sp.re(z)
            Im = sp.im(z)
            F  = sp.sqrt(Re**2+Im**2)
            if Im != 0:
                Q = str(sp.N(F/2/abs(Re), DISP))
            else:
                Q = ''
            F  = str(sp.N(F, DISP))
            Re = str(sp.N(Re, DISP))
            if Im != 0.:
                Im = str(sp.N(Im, DISP))
            else:
                Im = ''
            name = 'z<sub>' + str(i + 1) + '</sub>'
            html += '<tr><td>' + name + '</td><td>' + Re + '</td><td>' + Im + '</td><td>' + F + '</td><td>' + Q +'</td></tr>\n'
        html += '</table>\n'
    elif instObj.dataType == 'zeros' or instObj.dataType == 'pz':
        html += '<p>No zeros found.</p>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, html)
    return

### HTML links and labels

def eqref(label):
    """
    Returns the html code for a jump to an equation with label 'labelName'.
    This works for references to MathJax equations on the same page.
    """
    return '\\eqref{' + label + '}'
    
def href(label, linkText, fileName = ''):
    """
    Returns the html code for a jump to a label 'labelName'.
    This label can be on any page. If referring backwards 'fileName' can be
    detected automatically. When referring forward 'fileName' must be the 
    name of the file that will be created later. Run a project 2 times without
    closing it after the first run, automaitcally detects all labels.
    """
    if fileName == '':
        fileName = ini.htmlLabels[label]
    if fileName == ini.htmlPage:
        html = '<a href="#' +label+'">'+linkText+'</a>'
    else:
        html = '<a href="' + fileName + '#' +label+'">'+linkText+'</a>'
    return html

if __name__ == '__main__':
    ini.projectPath = ini.installPath + 'testProjects/MOSamp/'
    ini.htmlPath    = ini.projectPath + 'html/'
    startHTML('Test project') 