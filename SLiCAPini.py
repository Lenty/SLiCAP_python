#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sympy as sp
import numpy as np
import ply.lex as lex
from shutil import copy2 as cp
from time import time
from IPython import display
from datetime import datetime
import re
import subprocess
import os
import getpass

LOGFILE         = True
LANGUAGE        = 'english' # Language for error and warnings
DISP            = 4         # Numner of digits for floats in output
MATHJAXLOCAL    = False     # Local version of MathJax will be used if True

LAPLACE         = 's'       # Laplace veriable
FREQUENCY       = 'f'       # Frequency in Hz
OMEGA           = 'omega'   # Frequency in rad/s
MAXRECSUBST     = 10        # Maximum number of recursic=ve substitutions
HZ              = True      # True if frequency output in Hz, else: False

# PATHS: relative to the SLiCAP directory
HTMLPATH        = 'Project/html/'   # path for html output
CIRCUITPATH     = 'Project/cir/'    # path for .asc, .net, .cir, .sch files
LIBRARYPATH     = 'lib/'            # path for include and library files
TXTPATH         = 'Project/txt/'    # path for text files (text2html)
CSVPATH         = 'Project/csv/'    # path for CSV files (csv2html)
LATEXPATH       = 'Project/tex/'    # path for LaTeX output saveTeX()
MATHMLPATH      = 'Project/mathml/' # path for mathML output saveMathML()
IMGPATH         = 'Project/img/'    # path for image files

# Default plot settings
figureAxisHeight= 4
figureAxisWidth = 6
defaultColors   = ('r','b','g','c','m','y','k')
defaultMarkers  = ['']
tableFileType   = 'csv'
figureFileType  = 'svg'
axisXscale      = 'linear'    # Scale for the x-axis can be 'linear' or 'log'
axisYscale      = 'linear'    # Scale for the y-axis can be 'linear' or 'log'
legendLoc       = 'best'
SCALEFACTORS    =  {'y':'-24','z':'-21','a':'-18','f':'-15','p':'-12','n':'-9',
                    'u':'-6','m':'-3','k':'3','M':'6','G':'9','T':'12','P':'15',
                    'E':'18','Z':'21','Y':'24'} 
# Type conversions
LAPLACE         = sp.Symbol(LAPLACE)
FREQUENCY       = sp.Symbol(FREQUENCY)
OMEGA           = sp.Symbol(OMEGA)

# Where is it installed? 
INSTALLPATH     = os.path.abspath('.')