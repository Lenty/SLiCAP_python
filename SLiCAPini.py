#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from SLiCAPconfig import *
import sympy as sp
import numpy as np
import ply.lex as lex
from shutil import copy2 as cp
from shutil import copytree as ct
from time import time
from datetime import datetime
import re
import subprocess
import os
import getpass

# Type conversions
LAPLACE         = sp.Symbol(LAPLACE)
FREQUENCY       = sp.Symbol(FREQUENCY)
OMEGA           = sp.Symbol(OMEGA)

# Automatic detection of install and project paths
# Get the installation path
INSTALLPATH     = '/'.join(os.path.realpath(__file__).split('/')[0:-1]) + '/'
# Get the project path (the path of the script that imported SLiCAP.ini)
PROJECTPATH     = os.path.abspath('.') + '/'
# For test purposes there is a testproject directory:
if  PROJECTPATH == INSTALLPATH:
    # This is the case when running:
    # if __name__ == '__main__' sections in SLICAP script files.
    PROJECTPATH += 'testProjects/PIVA/'