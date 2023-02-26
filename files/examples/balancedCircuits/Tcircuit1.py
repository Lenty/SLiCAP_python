#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 17:14:45 2023

@author: anton
"""
from SLiCAP import *

fileName = "Tcircuit1"

#makeNetlist(fileName + ".asc", "T circuit -1-")

i1 = instruction()
i1.setCircuit(fileName + ".cir")

htmlPage("Circuit Data")
head2html("Circuit diagram")
img2html(fileName + ".svg", 600)
netlist2html(fileName + ".cir")
elementData2html(i1.circuit)
params2html(i1.circuit)

i1.setSource(['I1', 'I2'])

htmlPage("DM-CM decomposition")
# Define the decomposition
head2html("MNA matrix equation")
i1.setGainType("vi")
i1.setDataType("matrix")
matrices2html(i1.execute())
i1.setDetector('V_C')
i1.setGainType('gain')
i1.setDataType('laplace')
result = i1.execute()
print(result.laplace)

head2html("DM-CM matrix equation")
i1.defPar("R_b", "R_a")
i1.setPairExt(['P', 'N'])
i1.setConvType('all') 
i1.setGainType("vi")
i1.setDataType("matrix")
matrices2html(i1.execute())
i1.setDetector('V_C')
i1.setGainType('gain')
i1.setDataType('laplace')
result = i1.execute()
print(result.laplace)

head2html("DM matrix equation")
i1.setConvType('dd') 
i1.setGainType("vi")
i1.setDataType("matrix")
matrices2html(i1.execute())
i1.setDetector('V_in_D')
i1.setGainType('gain')
i1.setDataType('laplace')
result = i1.execute()
print(result.laplace)
print(result.Iv, result.M, result.Dv)

head2html("CM matrix equation")
i1.setConvType('cc') 
i1.setGainType("vi")
i1.setDataType("matrix")
matrices2html(i1.execute())
i1.setDetector('V_in_C')
i1.setGainType('gain')
i1.setDataType('laplace')
result = i1.execute()
print(result.laplace)