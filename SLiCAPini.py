#!/usr/bin/env python2
# -*- coding: utf-8 -*-

LOGFILE         = True
LANGUAGE        = 'english' # Language for error and warnings
DISP            = 4 # Numner of digits for floats in output
BUILT_IN_PARAMS = {'k':             '1.38064852e-23', # Bolzmann constant [J/K]
                   'q':             '1.60217662e-19', # Electron charge [C]
                   'c':             '2.99792458e+08', # Speed of light in vacuum [m/s]
                   'mu_0':          '4*pi*1e-7',      # permeability of vacuum [H/m]
                   'epsilon_0':     '1/c^2/mu_0',     # permittivity of vacuum [F/m]
                   'epsilon_SiO2':  '3.9',            # relative permittivity of SiO2
                   'T':             '300',            # simulation temperature [K]
                   'U_T':           'k*T/q',          # Thermal voltage [V]
                   'e':             'exp(1)',
                   'i':             '1j',
                   'PI':            'pi',
                  }
    
LAPLACE         = 's'     # Laplace veriable
FREQUENCY       = 'f'     # Frequency in Hz
OMEGA           = 'omega' # Frequency in rad/s
MAXRECSUBST     = 10      # Maximum number of recursic=ve substitutions
HZ              = True    # True if frequency output should be in Hz, else: False

# PATHS: relative to the project directory
CIRCUITPATH     = 'cir/'      # path for .asc, .net, .cir, .sch files
LIBRARYPATH     = 'lib/'      # path for include and library files
TXTPATH         = 'txt/'      # path for text files (text2html)
CSVPATH         = 'csv/'      # path for CSV files (csv2html)
LATEXPATH       = 'tex/'      # path for LaTeX output saveTeX()
MATHMLPATH      = 'mathml/'   # path for mathML output saveMathML()

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