#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Main module for running SLiCAP from a console or from within a Python IDE.

When working with Jupyter notebooks the main imort module is SLiCAPnotebook.py. 
It will import SLiCAP.py and some extra modules for displaying LaTeX, SVG and 
RST in the Jupyter notebooks.
"""
from SLiCAPinstruction import *

class SLiCAPproject(object):
    """
    Prototype of a SLiCAPproject. 
    """
    def __init__(self, name):
        
        self.name = name
        """
        SLiCAPproject.name (str) is the name of the project. It will appear 
        on the main html index page
        """       
        
        self.lastUpdate = datetime.now()
        """
        SLiCAPproject.lastUpdate (datetime.datetime) will be updated by
        running: SLiCAPproject.initProject(<name>)  
        """
        
        self.author = getpass.getuser()
        """
        SLiCAPproject.author (str) Will be updated by running: 
        SLiCAPproject.initProject(<name>)    
        """
        
        ini.lastUpdate = self.lastUpdate
    
def initProject(name):
    """
    Initializes a SLiCAP project.
    
    - Copies the directory structure from the templates subdirectory to the
      project directory in the case it has not yet been created.
    - Creates index.html in the html directory with the project name in the
      title bar
    - Compiles the system libraries
    - Creates or updates 'SLiCAPconfig.py' in the project directory
    - Creates instance of SLiCAPproject object
    
    :param name: Name of the project will be passed to an instance of the 
                 SLiCAPproject object.
    :type name: str
    :return:     SLiCAPproject
    :rtype:      SLiCAP.SLiCAPproject
    
    
    :Example:
    
    >>> prj = initProject('my first SLiCAP project')
    >>> print prj.author
    anton

    """
    ini.updatePaths(os.path.abspath('.') + '/')
    prj = SLiCAPproject(name)
    if not os.path.exists(ini.projectPath + 'SLiCAPconfig.py'):
        f = open(ini.installPath + 'SLiCAPconfig.py', 'r')
        txt = f.read()
        f.close()
        txt += '\n\n# Project information'
        txt += '\nPROJECT    = ' + '\'' + prj.name + '\'' 
        txt += '\nAUTHOR     = ' + '\'' + prj.author + '\'' 
        txt += '\nCREATED    = ' + '\'' + str(prj.lastUpdate) + '\'' 
        txt += '\nLASTUPDATE = ' + '\'' + str(prj.lastUpdate) + '\'' 
        f = open(ini.projectPath + 'SLiCAPconfig.py', 'w')
        f.write(txt)
        f.close()
    else:
        f = open(ini.projectPath + 'SLiCAPconfig.py', 'r')
        lines = f.readlines()[0:-1]
        f.close()
        lines.append('LASTUPDATE = ' + '\'' + str(prj.lastUpdate) + '\'')
        f = open(ini.projectPath + 'SLiCAPconfig.py', 'w')
        f.writelines(lines)
        f.close()
    makeDir(ini.circuitPath)
    makeDir(ini.imgPath)
    makeDir(ini.libraryPath)
    makeDir(ini.csvPath)
    makeDir(ini.txtPath)
    makeDir(ini.htmlPath)
    makeDir(ini.htmlPath + 'img/')
    makeDir(ini.htmlPath + 'css/')
    copyNotOverwrite(ini.installPath + 'slicap.css', ini.htmlPath + 'css/slicap.css')
    copyNotOverwrite(ini.installPath + 'Grid.png', ini.htmlPath + 'css/Grid.png')
    makeDir(ini.mathmlPath)
    makeDir(ini.latexPath)
    # Create the HTML project index file
    startHTML(name)
    # Create the libraries
    makeLibraries()
    return prj

if __name__ == '__main__':
    """
    Here is how to redefine symbols with assumption 'real'. 
    
    This cannot be added to the tokenizer, because parameter names ar modified 
    during circuit expansion. 
    
    The best place is to add it in SLiCAPyacc.updateCirData() and
    in SLiCAPprotos.circuit.defPar() and in SLiCAPprotos.circuit.defPars().
    See ToDos in these files.
    """
    a = sp.Symbol('a')
    b = sp.Symbol('b')
    c = a+sp.I*b
    print sp.re(c), sp.im(c)
    c = c.xreplace({symbol: sp.Symbol(str(symbol), real = True) for symbol in c.atoms(sp.Symbol)})
    print sp.re(c), sp.im(c)
    print c.as_real_imag()