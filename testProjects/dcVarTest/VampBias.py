#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 08:59:59 2020

@author: anton
"""
from SLiCAP import *
t1 = time()

prj = initProject('Vamp bias project') # Creates the SLiCAP libraries and the
                             # project HTML index page

fileName = 'VampBias.cir'
i1 = instruction()           # Creates an instance of an instruction object
i1.setCircuit(fileName)      # Checks and defines the local circuit object and
                             # sets the index page to the circuit index page
i1.setDetector('V_out')
i1.setSimType('symbolic')
i1.setGainType('vi')
i1.setDataType('dcvar')
result = i1.execute()

htmlPage('Netlist and circuit data');
netlist2html(fileName);
elementData2html(i1.circuit);
htmlPage('DC variance analysis');
dcVar2html(result)
t2 = time()
print '\n', t2-t1, 's'