#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLiCAP initialization module, imports external modules and defines settings.

Imported by the module **SLiCAini.py**
"""
from SLiCAPconfig import *
import docutils.core
import docutils.writers.html5_polyglot
import numpy as np
import sympy as sp
from scipy.signal import residue
from scipy.optimize import newton
import ply.lex as lex
from shutil import copy2 as cp
from time import time
from datetime import datetime
import re
import subprocess
import platform
import os
import getpass
import inspect
import matplotlib._pylab_helpers as plotHelp
from matplotlib import pyplot as plt
#plt.ioff() # Turn off the interactive mode for plotting

class settings(object):
    """
    A class for global variables.
    
    The following globals are defined:
        
    #. path settings
    
       - installPath       : Directory with SLiCAP modules files
       - projectPath       : Directory with SLiCAP project files
       - htmlPath          : Directory with SLiCAP HTML output
       - circuitPath       : Directory with SLiCAP project circuit files
       - libraryPath       : Directory with SLiCAP user libraries
       - txtPath           : Directory with text files for HTML output
       - csvPath           : Directory with csv files for HTML tables
       - latexPath         : Directory with csv files for HTML tables
       - mathmlPath        : Directory fro mathML output
       - imgPath           : Directory with images for HTML output
    
    #. active HTML pages and active HTMLfile prefix
    
       - htmlIndex         : Active HTML index page
       - htmlPage          : Active HTML page
       - htmlPrefix        : Active HTML prefix
    
    #. HTML labels and page names
    
       - htmlLabels        : Dict with HTML labels:
           
         - key   = labelName  : name of the label
         - value = pageName   : page of the label
         
       - htmlEqLabels      : Dict with HTML equation labels:
         
         - key   = labelName  : name of the label
         - value = pageName   : page of the label
         
       - htmlPages         : List with names of HTML pages
    
    #. Math settings
    
       - maxSolve:
        
         - True  : use Maxima for solving equations
         -  False : use Sympy for solving equations
      
       - stepFunction: 
      
         - True: use Sympy.lambify for parameter stepping
         - False : substitute step parameters in matrix
      
       - Hz:
        
         - True: frequency in Hz and phase in degrees
         - False : frequency in radians/s and phase in radians
      
       - Laplace           : Parameter used for Laplace variable
       - frequency         : Parameter used for frequency variable
       - maxRecSubst       : Maximum number of recursive substitutions
       - simplify          : True: simplify transfer functions
       - normalize: True: normalize transfer functions: lowest order  coefficient 
         of the Laplace variable will be normalized to unity.
       - factor: : Try to write the numerator and denominator of expressions as 
         a product of factors.
    
    #. Display settings
    
       - disp              : Number of digits for displaying floats on html pages
       - mathml:
      
         - True  : math in mathml in html pages 
         - False : math in latex in html pages and MathJaX cloud
      
       - language: language for error messages
    
    #. Plot settings
    
       - figureAxisHeight  : Height of the axis in inches (72dpi), pole-zero 
         and polar plots are square and have their height set to their width.
       - figureAxisWidth   : Width of an axis in inches (72dpi)
       - defaultColors     : List with matplotlib color names for param. stepping
       - gainColors        : dict with color names for gain types:
           
         - key   = gainType
         - value = matplotlib color name
         
       - defaultMarkers    : list with matplotlib markers
       - tableFileType     : file type for saving traces as tables
       - figureFileType    : graphic file type for saving plots
       - axisXscale        : default x-axis scale type
       - axisYscale        : default y-axis scale type
       - legendLoc         : default plot legend location
       - plotFontSize      : default plot font size
    
    #. Jupyter notebook settings
    
       - notebook: True adapts HTML math return variables to markdown format 
         required by Jupyter notebook
         
    #. Netlister settings:
   
       - ltspice : os command for batch netlist creation with LTspice
       
    #. Maxima command setting (only required for MSWindows)
    
       - maxima: command to start maxima under MSWindows
    """
    def __init__(self):
        """
        Initializes the start-up values of the global parameters.
        """
        self.installPath        = None 
        """
        Installation path of SLiCAP (*str*), defaults to None.
        """
        
        self.projectPath        = None
        """
        Project path (*str*), will be set by **SLiCAP.initProject()**;  defaults to None.
        """
        
        self.htmlPath           = None
        """
        HTML path (*str*), will be set by **SLiCAP.initProject()**;  defaults to None.
        """
        
        self.circuitPath        = None
        """
        Path (*str*) to circuit files, will be set by **SLiCAP.initProject()**;  defaults to None.
        """
        
        self.libraryPath        = None
        """
        Path (*str*) to library files, will be set by **SLiCAP.initProject()**;  defaults to None.
        """
        
        self.txtPath            = None
        """
        Path (*str*) to text files, will be set by **SLiCAP.initProject()**;  defaults to None.
        """
        
        self.csvPath            = None
        """
        Path (*str*) to .csv files, will be set by **SLiCAP.initProject()**;  defaults to None.
        """
        
        self.latexPath          = None
        """
        Path (*str*) for saving latex files, will be set by **SLiCAP.initProject()**;  defaults to None.
        """
        
        self.mathmlPath         = None
        """
        Path (*str*) for saving mathml files, will be set by **SLiCAP.initProject()**;  defaults to None.
        """
        
        self.imgPath            = None
        """
        Path (*str*), to image files will be set by **SLiCAP.initProject()**;  defaults to None.
        """
        
        self.mathml             = False
        """
        (*Bool*) setting for rendering math in html pages.
        
        - True  : math in mathml in html pages 
        - False : math in latex in html pages and MathJaX cloud
        """
        
        self.simplify           = False
        """
        (*Bool*) setting for simplification of expressions.
        
        - True  : simplification 
        - False : no simplification
        """
        
        self.normalize          = True
        """
        (*Bool*) setting for normalization of rational functions.
        
        - True  : normalization 
        - False : no normalization 
        """
        
        self.factor             = False
        """
        (*Bool*) setting for factorization of rational functions.
        
        - True  : factorization 
        - False : no factorization 
        """
        
        self.htmlIndex          = None
        """
        Name (*str*) of the active html index file. 
        Wiil be set by **SLiCAP.initProject()**. Defaults to: None.
        """
        
        self.htmlPage           = None
        """
        Name (*str*) of the active html file. 
        Wiil be set by **SLiCAP.initProject()**. Defaults to: None.
        """
        
        self.htmlPrefix         = None
        """
        Name (*str*) of athe ctive html prefix (first part of the file name). 
        Wiil be set by **SLiCAP.initProject()**. Defaults to: None.
        """
        
        self.htmlLabels         = None
        """
        (*dict*) with key-value pairs:
            
        - key: label name (*str*)
        - value" label object (*SLiCAPhtml.label*)
        
        Defaults to: None.
        """
        
        self.htmlPages          = None
        """
        (*list*) with names of html pages generated in the project.
        Defaults to: None.
        """
        
        self.stepFunction       = True
        """
        (*Bool*)
        
         - True: use Sympy.lambify for parameter stepping
         - False : substitute step parameters in matrix
         """
         
        self.maxSolve           = True
        """
        (*Bool*)
        
        - True: use Maxima CAS for solving matrix equations
        - False : use Sympy for solving matrix equations
        """
        
        self.maxRecSubst        = 10
        """
        Maximum number (*int*) of recursive substitutions in equations.
        Defaults to 10.
        """
        
        self.disp               = 4
        """
        Number of digits ()*int* for displaying floats on html pages.
        Defaults to 4.
        """
        
        self.Hz                 = True
        """
        (*Bool*)
        
        - True: frequency in Hz and phase in degrees
        - False : frequency in radians/s and phase in radians
        
        Defaults to True
        """
        
        self.Laplace            = sp.Symbol('s')
        """
        Symbol (*sympy.Symbol*) used for the Laplace variable.
        Defaults to sp.Symbol('s').
        """
        
        self.frequency          = sp.Symbol('f')
        """
        Symbol (*sympy.Symbol*) used for frequency.
        Defaults to sp.Symbol('f').
        """
        
        self.figureAxisHeight   = 5
        """
        Height in inches (*int, float*) of an axis system in a figure.
        Defaults to 5.
        """
        
        self.figureAxisWidth    = 7
        """
        Width in inches (*int, float*) of an axis system in a figure.
        Defaults to 7.
        """
        
        self.defaultColors      = ('r','b','g','c','m','y','k')
        """
        (*tuple*) with matplotlib color names (*str*) for traces in plots.
        Defaults to ('r','b','g','c','m','y','k')
        """
        
        self.gainColors         = {'gain': 'b', 'asymptotic': 'r', 
                                   'loopgain': 'k', 'direct': 'g', 
                                   'servo': 'm', 'vi': 'c'}
        """
        (*dict*) with key-value pairs for the color of traces for different
        gain types:
        
        - key: gain type: (*str*)
        - value: matplotlib color name (*str*) for traces in plots.
        
        Defaults to: {'gain': 'b', 'asymptotic': 'r', 'loopgain': 'k', 
        'direct': 'g', 'servo': 'm', 'vi': 'c'}
        """
        
        self.defaultMarkers     = ['']
        """
        (*list*) with matplotlib names of markers used for traces in plots.
        Defaults to: [''].
        """
        
        self.tableFileType      = 'csv'
        """
        File type (*str*) for csv files. Defaults to 'csv'.
        """
        
        self.figureFileType     = 'svg'
        """
        File type (*str*) for saving plots. Defaults to 'svg'.
        """
        
        self.axisXscale         = 'lin'
        """
        Default x axis type (*str*) for plots. Can be 'lin' or 'log'. 
        Defaults to 'lin'.
        """
        
        self.axisYscale         = 'lin'
        """
        Default y axis type (*str*) for plots.  Can be 'lin' or 'log'. 
        Defaults to 'lin'.
        """
        
        self.legendLoc          = 'best'
        """
        Default legend position (*str*) in plots. Cab be: 'upper left', 
        'upper right', 'lower left', 'lower right', 'upper center', 'lower center', 
        'center left', 'center right', 'center' or 'best'.

        Defaults to 'best'.
        """
        self.notebook           = False 
        """
        (*Bool*)
        
        - True: Places html math output between double dollar signs for correct 
          rendering of latex in Jupyter notebooks.
        
        Defaults to False.
        """
        
        self.plotFontSize       = 12
        """
        Value (*int*) for the font size in plots in points. Defaults to 12.
        """
        
        self.lastUpdate         = None
        """
        Value (*datetime.datetime*) of the date and time of the last project 
        update. This is set by **SLiCAP.initProject()**.
        """
        
        self.MaximaTimeOut      = 5     
        """
        Maximum time in seconds (*int*) for subprocess to run Maxima. Defaults
        to 5.
        """
        
        self.ltspice = 'wine ~/.wine/drive_c/Program\ Files/LTC/LTspiceXVII/XVIIx64.exe -netlist'
        """
        Operating system command prefix for batch generation of a netlist from an 
        LTspice circuit.
        
        - Windows: 'C:/Program Files/LTC/LTspiceXVII/XVIIx64.exe -netlist '
        - Linux (Wine): 'wine ~/.wine/drive_c/Program\ Files/LTC/LTspiceXVII/XVIIx64.exe -netlist '
        
        Defaults to *SLiCAPconfig.LTSPICE*
        
        This prefix will be followed by the name of the schematic file.
        """
        
        self.maxima             = None
        """
        MSWindows command for starting Maxima.
        
        Defaults to *SLiCAPconfig.MAXIMA*
        """
        
    def dump(self):
        """
        Prints the global variables and their values.
        """
        disallowed = ['asymptotic', 'servo', 'vi', 'direct', 'loopgain', 'gain']
        printTypes = [dict, list, int, float, str, bool]
        tabWidth   = 18
        for attr in dir(self):
            dct = getattr(self, attr)
            if type(dct) == dict:
                keys = list(dct.keys())
                keys.sort()
                for key in keys:
                    if key not in disallowed and type(dct[key]) in printTypes:
                        if key != 'htmlLabels':
                            ndots = tabWidth - len(key)
                            print(key, end = '')
                            dots = ''
                            for i in range(ndots):
                                dots += '.'
                            print(dots,':', dct[key])
                        elif key == 'htmlLabels':
                            dispkey = key + '.keys()'
                            ndots = tabWidth - len(dispkey)
                            print(dispkey, end = '')
                            dots = ''
                            for i in range(ndots):
                                dots += '.'
                            if type(dct[key]) == dict:
                                print(dots,':', list(dct[key].keys()))
                            else:
                                print(dots,':', dct[key])
                            
    def updatePaths(self, projectPath):
        """
        Updates the file locations according to the project path.
        
        :param projectPath: Path to the active SLiCAP project.
        :type projectPath: str
        """
        self.projectPath      = projectPath
        self.htmlPath         = projectPath + HTMLPATH
        self.circuitPath      = projectPath + CIRCUITPATH
        self.libraryPath      = projectPath + LIBRARYPATH
        self.txtPath          = projectPath + TXTPATH
        self.csvPath          = projectPath + CSVPATH
        self.latexPath        = projectPath + LATEXPATH
        self.mathmlPath       = projectPath + MATHMLPATH
        self.imgPath          = projectPath + IMGPATH
        self.maxima           = MAXIMA
        self.ltspice          = LTSPICE
                                    
ini = settings()
    
# Create an instance of globals
# Automatic detection of install and project paths
# Get the installation path
# ini.installPath  = '/'.join(os.path.realpath(__file__).split('/')[0:-1]) + '/'
ini.installPath = inspect.getfile(settings).replace('\\', '/').split('/')
ini.installPath = '/'.join(ini.installPath[0:-1]) + '/'
# Copy path settings from user configuration.
if PROJECTPATH == None:
    # Get the project path (the path of the script that imported SLiCAP.ini)
    PROJECTPATH  = os.path.abspath('.') + '/'
    
ini.updatePaths(PROJECTPATH)

if __name__ == '__main__':
    ini.dump()