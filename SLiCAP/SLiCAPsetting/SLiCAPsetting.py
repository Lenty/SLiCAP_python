#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLiCAP module with settings defined on install

Default parameters:

>>> VERSION     = None  #Version number
>>> SYSINSTALL  = ''    #System install path
>>> LIBCOREPATH = ''    #Library install path     
>>> DOCPATH     = ''    #Documentation install path
>>> MAXIMA      = ''    # Windows command for maxima
>>> LTSPICE     = 'wine ~/.wine/drive_c/Program\ Files/LTC/LTspiceXVII/XVIIx64.exe -wine -netlist'      # Command for netlist generation with LTspice
>>> NETLIST     = 'lepton-netlist -g spice-noqsi'   # Command for netlist generation with gschem or lepton-eda
"""
VERSION = '0.9.0'
SYSINSTALL = r' '
LIBCOREPATH = r'C:\Users\luc_e\SLiCAP\lib'
DOCPATH     = r'C:\Users\luc_e\SLiCAP\docs'
# PATHS: relative to the project path
MAXIMA      = r'C:\maxima-5.42.2\bin\maxima.bat' # Windows command for maxima
LTSPICE     = 'wine ~/.wine/drive_c/Program\ Files/LTC/LTspiceXVII/XVIIx64.exe -wine -netlist' # Command for netlist generation with LTspice
NETLIST     = 'lepton-netlist -g spice-noqsi' # Command for netlist generation with gschem or lepton-eda
