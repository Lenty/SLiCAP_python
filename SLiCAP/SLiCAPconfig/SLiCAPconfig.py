#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLiCAP module with user-defined path settings.

Default values:

>>> PROJECTPATH = None      # Leave it for automatic detection
>>> # PATHS: relative to the project path
>>> HTMLPATH    = 'html/'   # path for html output
>>> CIRCUITPATH = 'cir/'    # path for .asc, .net, .cir, .sch files
>>> LIBRARYPATH = 'lib/'    # path for include and library files
>>> TXTPATH     = 'txt/'    # path for text files (text2html)
>>> CSVPATH     = 'csv/'    # path for CSV files (csv2html)
>>> LATEXPATH   = 'tex/'    # path for LaTeX output saveTeX()
>>> MATHMLPATH  = 'mathml/' # path for mathML output saveMathML()
>>> IMGPATH     = 'img/'    # path for image files
>>> MAXIMA      = 'C:\\maxima-5.44.0\\bin\\maxima.bat' # Windows command for maxima
>>> LTSPICE     = 'wine ~/.wine/drive_c/Program\ Files/LTC/LTspiceXVII/XVIIx64.exe -wine -netlist' # Command for netlist generation with LTspice
>>> NETLIST     = 'lepton-netlist -g spice-noqsi' # Command for netlist generation with gschem or lepton-eda
"""
VERSION = '0.9.0'
PROJECTPATH = None      # Leave it for automatic detection
LIBCOREPATH = r'C:\Users\luc_e\SLiCAP\lib'
# PATHS: relative to the project path
HTMLPATH    = 'html/'   # path for html output
CIRCUITPATH = 'cir/'    # path for .asc, .net, .cir, .sch files
LIBRARYPATH = 'lib/'    # path for include and library files
TXTPATH     = 'txt/'    # path for text files (text2html)
CSVPATH     = 'csv/'    # path for CSV files (csv2html)
LATEXPATH   = 'tex/'    # path for LaTeX output saveTeX()
MATHMLPATH  = 'mathml/' # path for mathML output saveMathML()
IMGPATH     = 'img/'    # path for image files
MAXIMA      = r'C:\maxima-5.42.2\bin\maxima.bat' # Windows command for maxima
LTSPICE     = 'wine ~/.wine/drive_c/Program\ Files/LTC/LTspiceXVII/XVIIx64.exe -wine -netlist' # Command for netlist generation with LTspice
NETLIST     = 'lepton-netlist -g spice-noqsi' # Command for netlist generation with gschem or lepton-eda