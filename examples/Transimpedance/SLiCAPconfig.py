#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
SLiCAP module with user-defined path settings.
"""
PROJECTPATH     = None      # Leave it for automatic detection
# PATHS: relative to the project path
HTMLPATH        = 'html/'   # path for html output
CIRCUITPATH     = 'cir/'    # path for .asc, .net, .cir, .sch files
LIBRARYPATH     = 'lib/'    # path for include and library files
TXTPATH         = 'txt/'    # path for text files (text2html)
CSVPATH         = 'csv/'    # path for CSV files (csv2html)
LATEXPATH       = 'tex/'    # path for LaTeX output saveTeX()
MATHMLPATH      = 'mathml/' # path for mathML output saveMathML()
IMGPATH         = 'img/'    # path for image files

# Project information
PROJECT    = 'Transimpedance'
AUTHOR     = 'anton'
CREATED    = '2020-08-31 21:24:34.205164'
LASTUPDATE = '2020-08-31 23:45:06.796367'