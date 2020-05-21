#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 17:36:05 2020

@author: anton
"""

from SLiCAPini import *

HTMLINSERT  = '<!-- INSERT -->' # pattern to be replaced in html files
HTMLINDEX   = 'index.html'      # will be set by initProject()
HTMLPREFIX  = ''                # will be set by checkCircuit()
HTMLPAGE    = ''                # will be set by htmlPage()
HTMLCIRCUIT = False             # will be set by checkCircuit()

def HTMLhead(pageTitle):
    """
    Returns head for an html page with MathJax settings accoring to ini file.
    """
    HTML = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"><head><meta http-equiv="Content-Type" content="text/html;charset=iso-8859-1"/><meta name="Language" content="English"/><title>"' + pageTitle + '"</title><link rel="stylesheet" href="css/slicap.css">'
    if MATHJAXLOCAL == True:
        HTML += '<script type="text/x-mathjax-config">MathJax.Hub.Config({tex2jax: {inlineMath: [[''$'',''$'']]}});</script> <script type="text/x-mathjax-config">MathJax.Hub.Config({TeX: {equationNumbers: {autoNumber: \all"}}});</script><script type="text/javascript" src="' + INSTALLPATH + 'MathJax-latest"/MathJax.js?config=TeX-AMS_HTML"></script>'
        HTML += '</head><body><div id="top"><h1>' + pageTitle + '</h1></div>'
    else:
        HTML += """<script type="text/x-mathjax-config">MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$']]}});</script> <script type="text/x-mathjax-config">MathJax.Hub.Config({TeX: {equationNumbers: {autoNumber: "all"}}});</script><script src='https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML' async></script>"""
        HTML += '</head><body><div id="top"><h1>' + pageTitle + '</h1></div>'
    return(HTML)
    
def HTMLfoot(indexFile):
    """
    Return footer for html pages with link to 'indexFile'.
    """
    idx = indexFile.split('.')[0]
    HTML = '<div id="footnote"><p>Go to <a href="' + indexFile + '">' + idx + '</a></p><p>SLiCAP: Symbolic Linear Circuit Analysis Program, Version 1.0 &copy 2009-2020 SLiCAP development team</p><p>For documentation, examples, support, updates and courses please visit: <a href="http://www.analog-electronics.eu">analog-electronics.eu</a></p></div></body></html>'
    return(HTML)
    
def startHTML(projectName):
    """
    Creates main project index page.
    """
    global HTMLINDEX
    HTMLINDEX = 'index.html'
    toc = '<h2>Table of contents</h2>'
    HTML = HTMLhead(projectName) + toc + '<ol>' + HTMLINSERT + '</ol>' + HTMLfoot(HTMLINDEX)
    f = open(HTMLPATH + HTMLINDEX, 'w')
    f.write(HTML)
    f.close()
    return

def insertHTML(html):
    """
    Inserts html in the current html page.
    """
    global HTMLPAGE
    f = open(HTMLPATH + HTMLPAGE)
    HTML = f.read()
    f.close()
    HTML.replace(HTMLINSERT, html + HTMLINSERT)
    f = open(HTMLPATH + HTMLPAGE, 'w')
    f.write(HTML)
    f.close()
    return

def HTMLprefix(prefix):
    """
    Defines the prefix for HTML file names
    """
    global HTMLPREFIX
    HTMLPREFIX = prefix
    return

def HTMLindex(indexPage):
    """
    Defines active HTML index page
    """
    global HTMLINDEX
    HTMLINDEX = indexPage
    return

def HTMLpage(pageName):
    """
    Defines the active HTML page.
    """
    global HTMLPAGE
    HTMLPAGE = pageName
    return

def HTMLcircuit(circuitObject):
    """
    Defines the circuit for HTML reports.
    """
    global HTMLCIRCUIT
    HTMLCIRCUIT = circuitObject
    return

def readFile(fileName):
    """
    Returns the contents of a file as a string.
    """
    f = open(fileName, 'r')
    txt = f.read()
    f.close()
    return txt

def writeFile(fileName, txt):
    """
    Writes a text string to a file.
    """
    f = open(fileName, 'w')
    f.write(txt)
    f.close()
    return

def insertHTML(fileName, html):
    """
    Inserts html in the file specified by fileName at the location of
    HTMLINSERT.
    """
    HTML = readFile(fileName)
    HTML = HTML.replace(HTMLINSERT, html + HTMLINSERT)
    writeFile(fileName, HTML)
    return

def htmlPage(pageTitle, index = False):
    """
    Creates an HTML page with the title in the title bar. If index==True
    then the page will be used as new index page, else a link to this page will
    be placed on the current index page.
    The global HTMLINDEX holds the name of the current index page.
    """
    global HTMLINDEX, HTMLPAGE
    if index == True:
        # The page is a new index page
        fileName = HTMLPREFIX + 'index.html'
        # Place link on old index page
        href = '<li><a href="' + fileName +'">' + pageTitle + '</a></li>'
        insertHTML (HTMLPATH + HTMLINDEX, href)
        # Create the new HTML file
        toc = '<h2>Table of contents</h2>'
        HTML = HTMLhead(pageTitle) + toc + '<ol>' + HTMLINSERT + '</ol>' + HTMLfoot(HTMLINDEX)
        writeFile(HTMLPATH + fileName, HTML)
        # Make this page the new index page
        HTMLindex(fileName)
        # Make this page the active HTML page
        HTMLpage(fileName)
    else:
        fileName = HTMLPREFIX + '-'.join(pageTitle.split()) + '.html'
        # Place link on the current index page
        href = '<li><a href="' + fileName +'">' + pageTitle + '</a></li>'
        insertHTML(HTMLPATH + HTMLINDEX, href)
        # Create the new HTML page
        HTML = HTMLhead(pageTitle) + HTMLINSERT + HTMLfoot(HTMLINDEX)
        writeFile(HTMLPATH + fileName, HTML)
        # Make this page the active HTML page
        HTMLpage(fileName)
    return(HTML)

def head2html(headText):
    html = '<h2>' + headText + '</h2>'
    insertHTML(HTMLPATH + HTMLPAGE, html)
    return

def head3html(headText):
    html = '<h3>' + headText + '</h3>'
    insertHTML(HTMLPATH + HTMLPAGE, html)
    return

def text2html(txt):
    """
    Places txt on the active HTML page.
    """
    html = '<p>' + txt + '</p>'
    insertHTML(HTMLPATH + HTMLPAGE, html)
    return

def netlist2html():
    """
    Places the netlist of HTMLCIRCUIT on HTMLPAGE
    """
    if HTMLCIRCUIT == False:
        print "Error: no circuit has been defined yet."
    else:
        try:
            netlist = readFile(HTMLCIRCUIT.file)
            html = '<h2>Netlist: ' + HTMLCIRCUIT.file + '</h2><pre>' + netlist + '</pre>'
            insertHTML(HTMLPATH + HTMLPAGE, html)
        except:
            print "Error: could not open netlist file: '%s'."%(HTMLCIRCUIT.file)
    return

def csv2html(fileName, label = ''):
    return

def img2html(fileName, width, label = ''):
    return

def eqn2html(arg1, arg2, units = '', label = ''):
    """
    Displays an equation on the active HTML page'.
    
    ToDo:
        Add HTML label.
    """
    if type(arg1) == str or type(arg1) == float or type(arg1)== int:
        arg1 = sp.sympify(arg1)
    if type(arg2) == str or type(arg2) == float or type(arg2)== int:
        arg2 = sp.sympify(arg2)
    html = '$$' + sp.latex(sp.N(arg1, DISP)) + '=' + sp.latex(sp.N(arg2, DISP)) +'$$'
    insertHTML(HTMLPATH + HTMLPAGE, html)
    return

def matrices2html(MNA, label = ''):
    """
    Displays the MNA equation on the active HTML page.
    
    ToDo:
        Add HTML label.
    """
    try:
        (Iv, M, Vv) = MNA
        Iv = sp.latex(sp.N(Iv, DISP))
        M  = sp.latex(sp.N(M,  DISP))
        Vv = sp.latex(sp.N(Vv, DISP))
        html = '<h3>Matrix equation:</h3>'
        html += '$$' + Iv + '=' + M + '\\cdot' + Vv + '$$'
        insertHTML(HTMLPATH + HTMLPAGE, html)
    except:
        print "Error: unexpected input for 'matrices2html'."
    return

def expr2html(expr, units = ''):
    """
    Inline display of an expression optional with units.
    """
    if units != '':
        units = '\\left[\\mathrm{' + sp.latex(sp.sympify(units)) + '}\\right]'
    html = '$' + sp.latex(sp.N(expr, DISP)) + units + '$'
    insertHTML(HTMLPATH + HTMLPAGE, html)
    return

def elementData2html(label = ''):
    """
    Displays element data on the active html page:
        - refDes
        - nodes
        - referenced elements
        - parameters with symbolic and numeric values
    ToDo:
        Add HTML label.
    """
    if HTMLCIRCUIT == False:
        print "Error: no circuit has been defined yet."
    else:
        html = '<h2>' + HTMLCIRCUIT.title + ' element data of expanded netlist</h2><table><tr><th class="left">RefDes</th><th class="left">Nodes</th><th class="left">Refs</th><th class="left">Model</th><th class="left">Param</th><th class="left">Symbolic</th><th class="left">Numeric</th></tr>'
        elementNames = HTMLCIRCUIT.elements.keys()
        for el in sorted(elementNames):
            elmt = HTMLCIRCUIT.elements[el]
            html += '<tr><td class="left">' + elmt.refDes + '</td><td class = "left">'
            for node in elmt.nodes:
                html += node + ' '
            html += '</td><td class = "left">'
            for ref in elmt.refs:
                html += ref + ' '
            html += '</td><td class = "left">' + elmt.model +'</td>'
            parNames = elmt.params.keys()
            if len(parNames) == 0:
                html += '<td></td><td></td><td></td><tr>'
            else:
                i = 0
                for param in parNames:
                    symValue = '$' + sp.latex(sp.N(elmt.params[param], DISP)) +'$'
                    numValue = '$' + sp.latex(sp.N(fullSubs(elmt.params[param], HTMLCIRCUIT.parDefs), DISP)) + '$'
                    if i == 0:
                        html += '<td class="left">' + param + '</td><td class="left">' + symValue + '</td><td class="left">' + numValue + '</td></tr>'
                    else:
                        html += '<tr><td></td><td></td><td></td><td></td><td class="left">' + param + '</td><td class="left">' + symValue + '</td><td class="left">' + numValue + '</td></tr>'
                    i += 1
        html += '</table>'
        insertHTML(HTMLPATH + HTMLPAGE, html)
    return

def params2html():
    """
    Displays all parameters with definitions and numeric value.
    """
    if HTMLCIRCUIT == False:
        print "Error: no circuit has been defined yet."
    else:
        html = '<h2>' + HTMLCIRCUIT.title + ': parameter definitions</h2><table><tr><th class="left">Name</th><th class="left">Symbolic</th><th class="left">Numeric</th></tr>'
        for par in HTMLCIRCUIT.parDefs.keys():
            parName = '$' + sp.latex(par) + '$'
            symValue = '$' + sp.latex(sp.N(HTMLCIRCUIT.parDefs[par], DISP)) + '$'
            numValue = '$' + sp.latex(sp.N(fullSubs(HTMLCIRCUIT.parDefs[par], HTMLCIRCUIT.parDefs), DISP)) + '$'
            html += '<tr><td class="left">' + parName +'</td><td class="left">' + symValue + '</td><td class="left">' + numValue + '</td></tr>'
        html += '</table>'
        if len(HTMLCIRCUIT.params) > 0:
            html += '<h2>' + HTMLCIRCUIT.title + ': undefined parameters</h2><table><tr><th class="left">Name</th></tr>'
            for par in HTMLCIRCUIT.params:
                parName = '$' + sp.latex(par) + '$'
                html += '<tr><td class="left">' + parName +'</td></tr>'
            html += '</table>'
        insertHTML(HTMLPATH + HTMLPAGE, html)
    return

def pz2html(pzData, label = ''):
    """
    Displays the DC transfer, and tables with poles and zeros on the active 
    HTML page.
    
    ToDo:
        Change this routing with INSTRUCTION object as argument.
        This version is only for debug purposes!
        Add HTML label.
    """
    (poles, zeros, DCgain) = pzData
    html = '<h2>Pole-zero analysis results</h2>'
    if DCgain != False:
        html += '<h3>DC gain</h3>' + '<p>DC gain = ' + sp.latex(sp.N(DCgain, DISP)) + '</p>'
    else:
        html += '<p>DC gain could not be determined.</p>'
    if len(poles) > 0:
        html += '<h3>Poles</h3><table><tr><th>#</th><th>Re</th><th>Im</th><th>f [Hz]</th><th>Q</th></tr>'
        for i in range(len(poles)):
            p  = poles[i]/2/sp.pi
            Re = sp.re(p)
            Im = sp.im(p)
            F  = sp.sqrt(Re**2+Im**2)
            if Im != 0:
                Q = '$' + sp.latex(sp.N(F/2/abs(Re), DISP)) + '$'
            else:
                Q = ''
            F  = '$' + sp.latex(sp.N(F, DISP)) + '$'
            Re = '$' + sp.latex(sp.N(Re, DISP)) + '$'
            Im = '$' + sp.latex(sp.N(Im, DISP)) + '$'
            name = '$p_{' + str(i + 1) + '}$'
            html += '<tr><td>' + name + '</td><td>' + Re + '</td><td>' + Im + '</td><td>' + F + '</td><td>' + Q +'</td></tr>'
        html += '</table>'
    else:
        html += '<p>No poles found.</p>'
    if len(zeros) > 0:
        html += '<h3>Zeros</h3><table><tr><th>#</th><th>Re</th><th>Im</th><th>f [Hz]</th><th>Q</th></tr>'
        for i in range(len(poles)):
            p  = poles[i]/2/sp.pi
            Re = sp.re(p)
            Im = sp.im(p)
            F  = sp.sqrt(Re**2+Im**2)
            if Im != 0:
                Q = '$' + sp.latex(sp.N(F/2/abs(Re), DISP)) + '$'
            else:
                Q = ''
            F  = '$' + sp.latex(sp.N(F, DISP)) + '$'
            Re = '$' + sp.latex(sp.N(Re, DISP)) + '$'
            Im = '$' + sp.latex(sp.N(Im, DISP)) + '$'
            name = '$z_{' + str(i + 1) + '}$'
            html += '<tr><td>' + name + '</td><td>' + Re + '</td><td>' + Im + '</td><td>' + F + '</td><td>' + Q +'</td></tr>'
        html += '</table>'
    else:
        html += '<p>No zeros found.</p>'
    insertHTML(HTMLPATH + HTMLPAGE, html)
    return
    
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
        print "Warning: reached maximum number of substitutions for expression '%s'"%(strValExpr)
    return valExpr

if __name__ == '__main__':
    startHTML('Test project')