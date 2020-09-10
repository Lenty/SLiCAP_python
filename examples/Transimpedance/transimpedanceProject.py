#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 21:21:35 2020

@author: anton
"""

from SLiCAP import *
prj = initProject('Transimpedance')
instr = instruction()
instr.setCircuit('transimpedanceSpec.cir')
htmlPage('Application and specifications')
file2html('applicationDescription.txt')