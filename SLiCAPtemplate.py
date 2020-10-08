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
VERSION = '$VERSION'
SYSINSTALL = r'$SYSINSTALL'
LIBCOREPATH = r'$LIBCOREPATH'
DOCPATH     = r'$DOCPATH'
# PATHS: relative to the project path
MAXIMA      = r'$MAXIMAPATH' # Windows command for maxima
LTSPICE     = 'wine ~/.wine/drive_c/Program\ Files/LTC/LTspiceXVII/XVIIx64.exe -wine -netlist' # Command for netlist generation with LTspice
NETLIST     = 'lepton-netlist -g spice-noqsi' # Command for netlist generation with gschem or lepton-eda


def _selftest_maxima():
    if platform.system() == 'Windows':
        try:
            result = subprocess.run([self._maxima_cmd, '--very-quiet', '-batch-string', maxInput], capture_output=True, timeout=3, text=True).stdout.split('\n')
        except:
            print("Not able to succesfully execute the maxima command, please re-run the SLiCAP setup.py script and set the path again")
    else:
        try:
            result = subprocess.run(['maxima', '--very-quiet', '-batch-string', maxInput], capture_output=True, timeout=3, text=True).stdout.split('\n')

        except:
            print("Not able to run the maxima command, verify maxima is installed by typing 'maxima' in the command line")
            print("In case maxima is not installed, use your package manager to install it (f.e. 'sudo apt install maxima')")
    
    result = [i for i in result if i] # Added due to variability of trailing '\n'
    result = result[-1]
    if int(result) == 2:
        succes = True
        print("Succesfully self-tested the Maxima command")
    
def _check_version():
    