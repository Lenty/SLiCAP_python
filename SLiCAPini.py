#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from SLiCAPconfig import *
import sympy as sp
import numpy as np
from scipy.signal import residue
import ply.lex as lex
from shutil import copy2 as cp
from time import time
from datetime import datetime
import re
import subprocess
import os
import getpass
import matplotlib._pylab_helpers as plotHelp
from matplotlib import pyplot as plt
plt.ioff() # Turn off the interactive mode for plotting

class settings(object):
    """
    Class with global variables that can be modified from within other modules
    and by the user. These variables can be adressed as attributes of 'ini', 
    e.g. ini.circuitPath = 'cir/'.
    
    The following globals are defined:
        
    path settings
    -------------
    
    - installPath       : Directory with SLiCAP python script files
    - projectPath       : Directory with SLiCAP project script files
    - htmlPath          : Directory with SLiCAP HTML output
    - circuitPath       : Directory with SLiCAP project circuit files
    - libraryPath       : Directory with SLiCAP user libraries
    - txtPath           : Directory with text files for HTML output
    - csvPath           : Directory with csv files for HTML tables
    - latexPath         : Directory with csv files for HTML tables
    - mathmlPath        : Directory fro mathML output
    - imgPath           : Directory with images for HTML output
    
    active HTML pages and active HTMLfile prefix
    --------------------------------------------
    
    - htmlIndex         : Active HTML index page
    - htmlPage          : Active HTML page
    - htmlPrefix        : Active HTML prefix
    
    HTML labels and page names
    --------------------------
    
    - htmlLabels        : Dict with HTML labels:
                            key   = labelName  : name of the label
                            value = pageName   : page of the label
    - htmlEqLabels      : Dict with HTML equation labels:
                            key   = labelName  : name of the label
                            value = pageName   : page of the label
    - htmlPages         : List with names of HTML pages
    
    Math settings
    -------------
    
    - maxSolve          : True  : use Maxima for solving equations
                          False : use Sympy for solving equations
    - stepFunction      : True  : use Sympy.lambify for parameter stepping
                          False : substitute step parameters in matrix
    - Hz                : True  : frequency in Hz and phase in degrees
                          False : frequency in radians/s and phase in radians
    - Laplace           : Parameter used for Laplace variable
    - frequency         : Parameter used for frequency variable
    - maxRecSubst       : Maximum number of recursive substitutions
    - simplify          : True: simplify transfer functions
    - normalize         : True: normalize transfer functions: lowest order
                          coefficient of the Laplace variable will be
                          normalized to unity.
    - factor            : Try to write the numerator and denominator of
                          expressions as product of factors.
    
    Display settings
    ----------------
    
    - disp              : Number of digits for displaying floats on html pages
    - mathml            : True  : math in mathml in html pages 
                        : False : math in latex in html pages and MathJaX cloud
    - language          : language for error messages
    
    Plot settings
    -------------
    
    - figureAxisHeight  : Height of the axis in inches (72dpi)
                          Pole-zero and polar plots are square and have their 
                          height set to their width.
    - figureAxisWidth   : Width of an axis in inches (72dpi)
    - defaultColors     : List with matplotlib color names for param. stepping
    - gainColors        : dict with color names for gain types:
                            key   = gainType
                            value = matplotlib color name
    - defaultMarkers    : list with matplotlib markers
    - tableFileType     : file type for saving traces as tables
    - figureFileType    : graphic file type for saving plots
    - axisXscale        : default x-axis scale type
    - axisYscale        : default y-axis scale type
    - legendLoc         : default plot legend location
    - plotFontSize      : default plot font size
    
        
    """
    def __init__(self):
        """
        Initializes the start-up values of the global parameters.
        """
        self.installPath        = None 
        self.projectPath        = None
        self.htmlPath           = None
        self.circuitPath        = None
        self.libraryPath        = None
        self.txtPath            = None
        self.csvPath            = None
        self.latexPath          = None
        self.mathmlPath         = None
        self.imgPath            = None
        self.mathml             = False
        self.simplify           = False
        self.normalize          = True
        self.factor             = False
        self.htmlIndex          = None
        self.htmlPage           = None
        self.htmlPrefix         = None
        self.htmlLabels         = None
        self.htmlEqLabels       = None
        self.htmlPages          = None
        self.stepFunction       = True
        self.maxSolve           = True
        self.maxRecSubst        = 10
        self.disp               = 4
        self.Hz                 = True
        self.Laplace            = sp.Symbol('s')
        self.frequency          = sp.Symbol('f')
        self.figureAxisHeight   = 5
        self.figureAxisWidth    = 7
        self.defaultColors      = ('r','b','g','c','m','y','k')
        self.gainColors         = {'gain': 'b', 'asymptotic': 'r', 
                                   'loopgain': 'k', 'direct': 'g', 
                                   'servo': 'm', 'vi': 'c'}
        self.defaultMarkers     = ['']
        self.tableFileType      = 'csv'
        self.figureFileType     = 'svg'
        self.axisXscale         = 'linear'
        self.axisYscale         = 'linear'
        self.legendLoc          = 'best'
        self.plotFontSize       = 12
        self.lastUpdate         = None

# Create an instance of globals
ini = settings()
# Automatic detection of install and project paths
# Get the installation path
ini.installPath  = '/'.join(os.path.realpath(__file__).split('/')[0:-1]) + '/'
# Get the project path (the path of the script that imported SLiCAP.ini)
ini.projectPath  = os.path.abspath('.') + '/'
# Copy path settings from user configuration.
ini.htmlPath         = ini.projectPath + HTMLPATH
ini.circuitPath      = ini.projectPath + CIRCUITPATH
ini.libraryPath      = ini.projectPath + LIBRARYPATH
ini.txtPath          = ini.projectPath + TXTPATH
ini.csvPath          = ini.projectPath + CSVPATH
ini.latexPath        = ini.projectPath + LATEXPATH
ini.mathmlPath       = ini.projectPath + MATHMLPATH
ini.imgPath          = ini.projectPath + IMGPATH