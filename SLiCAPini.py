#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import re
import sympy as sp
import numpy as np
from time import time
from IPython import display
import ply.lex as lex
import subprocess
import os
from datetime import datetime

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

# Type conversions
LAPLACE         = sp.Symbol(LAPLACE)
FREQUENCY       = sp.Symbol(FREQUENCY)
OMEGA           = sp.Symbol(OMEGA)

# Where is it installed? 
INSTALLPATH     = os.path.abspath('.')