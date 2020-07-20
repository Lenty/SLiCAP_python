#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 20:29:52 2020

@author: anton
"""
from SLiCAPinstruction import *

class SLiCAPproject(object):
    """
    Prototype of a SLiCAPproject.
    """
    def __init__(self, name):
        self.name = name
        self.lastUpdate = datetime.now()
        self.author = getpass.getuser()
        ini.lastUpdate = self.lastUpdate

def makeDir(dirName):
    """
    Creates the directory 'dirName' if it does not yet exist.
    """
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    return

def copyNotOverwrite(src, dest):
    """
    Copies the file 'src' to 'dest' if the latter one does not exist.
    """
    if not os.path.exists(dest):
        cp(src, dest)
    return
    
def initProject(name):
    """
    Initializes a SLiCAP project.
    
    - Copies the directory structure from the templates subdirectory to the
      project directory in the case it has not yet been created.
    - Creates index.html in the html directory
    - Compiles the system libraries
    - Creates or updates 'SLiCAPconfig.py' in the project directory
    
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
    startHTML(name)
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