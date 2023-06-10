#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 18:03:04 2021

@author: anton
"""
from SLiCAP import *
from SLiCAP.SLiCAPdocTools import *

fileName = 'myFirstVampOPA211bias'

prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName + '.cir');
#
i1.setSource('V1');
i1.setDetector('V_out');
i1.setGainType('vi');
i1.setDataType('dcvar');
#
dcVarResults = i1.execute()

saveRST(dcvarContribs2RST(dcVarResults), fileName + '_dcvar')