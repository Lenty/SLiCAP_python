#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon July 06 18:32:40 2020

@author: anton
"""

from SLiCAP import *
t1 = time()

prj = initProject('Test Cramer') 
                             # Creates the SLiCAP libraries and the
                             # project HTML index page
#ini.projectPath = '/mnt/DATA/SLiCAP/SLiCAP_github/SLiCAP_python/testProjects/testCramer/'
fileName = 'LowPassLR.cir'

i1 = instruction()           # Creates an instance of an instruction object
i1.setCircuit(fileName)    # Checks and defines the local circuit object and
                             # resets the index page to the project index page
                             
i1.setSource('V1')
i1.setDetector('V_out')
i1.setSimType('numeric')
i1.setGainType('vi')
i1.setDataType('matrix')
result = i1.execute()

i1.setDataType('time')
responseTime= i1.execute()
response    = responseTime.time
ini.gainColors['vi'] = 'r'
figTime = plotSweep('time', 'response', responseTime, 0, 1.5, 200, sweepScale='m', yScale = 'm', yUnits = 'V', show=True)

t2 = time()
print t2-t1, 's'