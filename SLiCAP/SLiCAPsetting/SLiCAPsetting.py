#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SLiCAP module with settings defined on install, contains fixed parameters

Default parameters:

>>> VERSION     = None  # Version number
>>> SYSINSTALL  = ''    # System install path
>>> USERPATH    = ''    # User install path
>>> LIBCOREPATH = ''    # Library install path
>>> DOCPATH     = ''    # Documentation install path
>>> MAXIMA      = ''    # Windows command for maxima
>>> LTSPICE     = 'wine ~/.wine/drive_c/Program\ Files/LTC/LTspiceXVII/XVIIx64.exe -wine -netlist'      # Command for netlist generation with LTspice
>>> NETLIST     = 'lepton-netlist -g spice-noqsi'   # Command for netlist generation with gschem or lepton-eda
"""
VERSION     = '1.7.0'
SYSINSTALL  = r' '
USERPATH    = r'/home/anton/SLiCAP'
LIBCOREPATH = r'/home/anton/SLiCAP/lib'
DOCPATH     = r'/home/anton/SLiCAP/docs'
MAXIMA      = r'maxima' # Windows command for maxima
LTSPICE     = r'/home/anton/.wine/drive_c/Program Files/LTC/LTspiceXVII/XVIIx64.exe' # Command for netlist generation with LTspice
NETLIST     = 'lepton-netlist -g spice-noqsi' # Command for netlist generation with gschem or lepton-eda
