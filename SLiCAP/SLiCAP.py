#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main module for running SLiCAP from a console or from within a Python IDE.

When working with Jupyter notebooks the main imort module is SLiCAPnotebook.py.
It will import SLiCAP.py and some extra modules for displaying LaTeX, SVG and
RST in the Jupyter notebooks.
"""
from SLiCAP.SLiCAPinstruction import *

try:
    __IPYTHON__
    print("Running from an Ipython enviroment, importing SLiCAPnotebook.")
    from SLiCAP.SLiCAPnotebook import *
    ini.notebook = True
except NameError:
    ini.notebook = False


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

def initProject(name, firstRun=True):
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
    ini.lastUpdate = prj.lastUpdate
    if not os.path.exists(ini.projectPath + 'SLiCAPconfig.py'):
        f = open(ini.installPath + '/SLiCAPconfig/SLiCAPconfig.py', 'r')
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
    if firstRun:
        makeDir(ini.circuitPath)
        makeDir(ini.imgPath)
        makeDir(ini.libraryPath)
        makeDir(ini.csvPath)
        makeDir(ini.txtPath)
        makeDir(ini.htmlPath)
        makeDir(ini.htmlPath + 'img/')
        makeDir(ini.htmlPath + 'css/')
        copyNotOverwrite(ini.defaultLib + '/slicap.css', ini.htmlPath + 'css/slicap.css')
        copyNotOverwrite(ini.defaultLib + '/Grid.png', ini.htmlPath + 'css/Grid.png')
        makeDir(ini.mathmlPath)
        makeDir(ini.latexPath)
        # Create the HTML project index file
    startHTML(name)
        # Create the libraries
    if len(list(SLiCAPCIRCUITS.keys())) == 0 or len(list(SLiCAPPARAMS.keys())) == 0:
        makeLibraries()
    return prj    

def makeNetlist(fileName, cirTitle):
    """
    Creates a netlist from a schematic file generated with LTspice or gschem.
    
    - LTspice: '.asc' file
    - gschem: '.sch' file
    
    :param fileName: Name of the file, relative to **ini.circuitPath**
    :type fileName: str
    
    :param cirTitle: Title of the schematic.
    :type cirTitle: str
    """
    if not os.path.isfile(ini.circuitPath + fileName):
        print("Error: could not open: '%s'."%(ini.circuitPath + fileName))
        return
    else:
        fileNameParts = fileName.split('.')
        fileType = fileNameParts[-1].lower()
        baseFileName = ini.circuitPath + '.'.join(fileNameParts[0:-1])
        if fileType == 'asc':
            file = os.path.abspath(baseFileName + '.asc')
            print(file)
            if platform.system() == 'Windows':    
                file = file.replace('\\','\\\\')
                subprocess.run([ini.ltspice, '-netlist', file])
            else:
                subprocess.run(['wine', ini.ltspice, '-wine', '-netlist', file])
            try:
                f = open(baseFileName + '.net', 'r')
                netlistLines = ['"' + cirTitle + '"\n'] + f.readlines()
                f.close()
                f = open(baseFileName + '.cir', 'w')
                f.writelines(netlistLines)
                f.close()
            except:
                print("Error: could not open: '%s'."%(baseFileName + '.net'))
        elif fileType == 'sch':
            outputfile = os.path.abspath(baseFileName + '.net')
            inputfile = os.path.abspath(baseFileName + '.sch')
            print('input: ',inputfile, ' output: ', outputfile)
            if platform.system() != 'Windows':    
                try:
                    subprocess.run(['lepton-netlist', '-g', 'spice-noqsi', '-o', outputfile, inputfile])
                except:
                    print("Could not generate netlist using Lepton-eda")
            try:
                if platform.system() == 'Windows':    
                    outputfile = outputfile.replace('\\','\\\\')
                    inputfile = inputfile.replace('\\','\\\\')
                subprocess.run(['gnetlist', '-q', '-g', 'spice-noqsi', '-o', outputfile, inputfile])
            except:
                print("Could not generate netlist using gschem")
            try:
                f = open(baseFileName + '.net', 'r')
                netlistLines = ['"' + cirTitle + '"\n'] + f.readlines()[1:] + ['.end\n']
                f.close()
                f = open(baseFileName + '.cir', 'w')
                f.writelines(netlistLines)
                f.close()
            except:
                print("Error: could not open: '{0}'.".format(baseFileName + '.net'))
    return

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
    print(sp.re(c), sp.im(c))
    c = c.xreplace({symbol: sp.Symbol(str(symbol), real = True) for symbol in c.atoms(sp.Symbol)})
    print(sp.re(c), sp.im(c))
    print(c.as_real_imag())
