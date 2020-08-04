#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 14:59:59 2020

@author: anton
"""
from SLiCAP import *
t1 = time()

prj = initProject('Vamp bias project') # Creates the SLiCAP libraries and the
                             # project HTML index page

fileName = 'VampBiasNullor.cir'
i1 = instruction()           # Creates an instance of an instruction object
i1.setCircuit(fileName)    # Checks and defines the local circuit object and
                             # resets the index page to the project index page
i1.setDetector('V_6')
i1.setSimType('symbolic')
i1.setGainType('vi')
i1.setDataType('dc')
result = i1.execute();
DCvalue = result.dc;
i1.setDataType('dcsolve')
result = i1.execute()
DCsolution = result.dcSolve

htmlPage('Netlist and circuit data');
netlist2html(fileName);
elementData2html(i1.circuit);
htmlPage('DC analysis');
text2html('The DC voltage $V_6$ is obtained as:')
eqn2html('V_6', DCvalue, units = 'V');
text2html('The DC solution of the network is:')
eqn2html(result.Dv, DCsolution)

i1.setDataType('dcvar')
result = i1.execute()
htmlPage('DC variance analysis')
dcVar2html(result)
t2 = time()
print '\n', t2-t1, 's'