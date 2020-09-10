#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
SLiCAP module with user-defined path settings.
"""
PROJECTPATH = None      # Leave it for automatic detection
# PATHS: relative to the project path
HTMLPATH    = 'html/'   # path for html output
CIRCUITPATH = 'cir/'    # path for .asc, .net, .cir, .sch files
LIBRARYPATH = 'lib/'    # path for include and library files
TXTPATH     = 'txt/'    # path for text files (text2html)
CSVPATH     = 'csv/'    # path for CSV files (csv2html)
LATEXPATH   = 'tex/'    # path for LaTeX output saveTeX()
MATHMLPATH  = 'mathml/' # path for mathML output saveMathML()
IMGPATH     = 'img/'    # path for image files
MAXIMA      = 'C:\\maxima-5.44.0\\bin\\maxima.bat' # Windows command for maxima
LTSPICE     = 'wine ~/.wine/drive_c/Program\ Files/LTC/LTspiceXVII/XVIIx64.exe -netlist '  

# Project information
PROJECT    = 'My first RC network'
AUTHOR     = 'anton'
CREATED    = '2020-09-10 10:22:47.760338'
LASTUPDATE = '2020-09-10 12:25:09.024005'