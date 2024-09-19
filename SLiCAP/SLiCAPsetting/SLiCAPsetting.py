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
>>> KICAD       = ''    # Command for kicad-cli
>>> INKSCAPE    = ''    # Command for Inkscape
>>> NETLIST     = 'lepton-netlist -g spice-noqsi'   # Command for netlist generation with gschem or lepton-eda
"""
VERSION     = '1.8.0'
SYSINSTALL  = r' '
USERPATH    = r'C:\Users\anton\SLiCAP'
LIBCOREPATH = r'C:\Users\anton\SLiCAP\lib'
DOCPATH     = r'C:\Users\anton\SLiCAP\docs'
MAXIMA      = r'C:\maxima-5.46.0\bin\maxima.bat' # Windows command for maxima
LTSPICE     = r'C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe' # Command for netlist generation with LTspice
NGSPICE     = r'C:\Users\anton\SLiCAP\ngspice\Spice64\bin\ngspice.exe' # Command for starting NGspice
KICAD       = r'C:\Program Files\KiCad\8.0\bin\kicad-cli.exe' # Command for starting KiCad-cli
INKSCAPE    = r'C:\Program Files\Inkscape\bin\inkscape.exe' # Command for starting Inkscape
NETLIST     = 'lepton-netlist -g spice-noqsi' # Command for netlist generation with gschem or lepton-eda
