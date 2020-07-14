#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon July 06 18:32:40 2020

@author: anton
"""

from SLiCAP import *
t1 = time()

prj = initProject('Response 4-th order Linkwitz-Riley Filter') 
                             # Creates the SLiCAP libraries and the
                             # project HTML index page
#ini.projectPath = '/mnt/DATA/SLiCAP/SLiCAP_github/SLiCAP_python/testProjects/testCramer/'
fileName = 'LowPassLR.cir'

i1 = instruction()           # Creates an instance of an instruction object
i1.checkCircuit(fileName)    # Checks and defines the local circuit object and
                             # resets the index page to the project index page
                             
i1.source   = 'V1'
i1.detector = 'V_out'
i1.simType  = 'numeric'
i1.gainType = 'vi'
i1.dataType = 'matrix'
result = i1.execute()

i1.dataType = 'time'
responseTime= i1.execute()
response    = responseTime.time
ini.gainColors['vi'] = 'r'
figTime = plotTime('time', 'response', responseTime, 0, 1.5, 200, xscale='m', yscale = 'm', yunits = 'V', show=True)

t2 = time()
print t2-t1, 's'