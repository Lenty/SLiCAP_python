#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLiCAP module with user-defined path settings.
"""
PROJECTPATH = 'C:\\Users\\luc_e\\Documents\\git\\SLiCAP_python\\examples\\MOSparams'      # Leave it for automatic detection
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
NETLIST     = 'lepton-netlist -g spice-noqsi' # Command for netlist generation with gschem or lepton-eda

# Project information
PROJECT    = 'NMOS EKV polts'
AUTHOR     = 'Anton'
CREATED    = '2020-09-10 10:46:09.433889'
LASTUPDATE = '2020-09-29 18:04:38.328140'