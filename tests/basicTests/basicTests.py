#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 13:24:50 2020

@author: anton
"""
from SLiCAP import *
prj = initProject('basicTests')
t1 = time()
i1 = instruction()

circuits = ['E', 'EZ', 'F', 'G', 'H', 'HZ'];
results = {'E': sp.sympify('-(A_v*R_2*(s*tau_z + 1))/((2*R_1 + R_2)*(s*tau_p + 1))'),
           'EZ': sp.sympify('-(A_v*R_2*(s*tau_z + 1)*(s*tau_zp + 1))/((s*tau_p + 1)*(R + 2*R_1 + R_2 + R*s*tau_zz + 2*R_1*s*tau_zp + R_2*s*tau_zp))'),
           'F': sp.sympify('-(A_i*R_2*(s*tau_z + 1))/((2*R_1 + R_2)*(s*tau_p + 1))'),
           'G': sp.sympify('-(A_y*R_2*R_3*(s*tau_z + 1))/((s*tau_p + 1)*(2*R_1 + R_2 + R_3))'),
           'H': sp.sympify('-(A_z*(s*tau_z + 1))/(2*R_1*(s*tau_p + 1))'),
           'HZ': sp.sympify('-(A_z*(s*tau_z + 1)*(s*tau_zp + 1))/((s*tau_p + 1)*(R + 2*R_1 + R*s*tau_zz + 2*R_1*s*tau_zp))')}

for i in range(len(circuits)):
    i1.setCircuit(circuits[i] + '.cir')
    htmlPage("Circuit data " + circuits[i])
    netlist2html(circuits[i] + '.cir')
    elementData2html(i1.circuit)
    i1.setSimType('symbolic')
    i1.setDataType('laplace')
    i1.setGainType('loopgain')
    i1.setLGref(circuits[i] + '1')
    result      = i1.execute()
    lgLaplace   = result.laplace
    print('Loop gain test:', circuits[i])
    if sp.simplify(results[circuits[i]] - lgLaplace) == 0:
        print('OK!\n')
    else:
        print(lgLaplace)
        print('Wrong answer.\n')

# Check balanced resonator
i1.setCircuit("balancedResonator.cir")
netlist2html('balancedResonator.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)
i1.setSource(['I1','I2'])
i1.setDetector(['V_inP', 'V_inN'])
i1.setGainType('gain')
i1.setDataType('laplace')
i1.setSimType("numeric")
i1.defPar("K",1)
DMresult = i1.execute()
error = sp.simplify(DMresult.laplace - sp.sympify("2.0*L_d*R_d*s/(2.0*C_d*L_d*R_d*s**2 + 2.0*L_d*s + R_d)"))
if error == 0:
    print("OK!\n")
else:
    print(error)
    print("Wrong answer.\n")
i1.defPar("K",0)
DMresult = i1.execute()
error = sp.simplify(DMresult.laplace - sp.sympify("1.0*L_d*R_d*s/(C_d*L_d*R_d*s**2 + L_d*s + R_d)"))
if error == 0:
    print("OK!\n")
else:
    print(error)
    print("Wrong answer.\n")
i1.defPar("K",-1)
DMresult = i1.execute()
error = DMresult.laplace
if error == 0:
    print("OK!\n")
else:
    print(error)
    print("Wrong answer.\n")
#print("ERROR",error)

# Check balanced amplifier
i1.setCircuit("DMCM.cir")
netlist2html('DMCM.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)

i1.setSimType('symbolic')
i1.setGainType('gain')
i1.setDataType('laplace')
i1.setSource(['ViN', 'ViP'])
i1.setDetector('V_n3P')
i1.setLGref(['G1P', 'G1N'])
seResult = i1.execute()
seGain = seResult.laplace

i1.setConvType('dd')
i1.setPairExt(['P', 'N'])
i1.setDetector('V_n3_D')
ddResult = i1.execute()
ddGain = ddResult.laplace

i1.setConvType('cc')
i1.setDetector('V_n3_C')
ccResult = i1.execute()
ccGain = ccResult.laplace

i1.setConvType(None)

# Check model QD
i1.setCircuit('QDmodel.cir')
netlist2html('QDmodel.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)

# Check hierarchy
i1.setCircuit('hierarchy.cir')
netlist2html('hierarchy.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)

# Check if default model parameters are passed to an element of which the
# model needs to be expanded. This is done for a bipolar transistor model 'QV'.
i1.setCircuit('defaultParams.cir')
htmlPage('Circuit data')
netlist2html('defaultParams.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)

# Check if parameters are passed correctly to models
i1.setCircuit('params2model.cir')
htmlPage('Circuit data')
netlist2html('params2model.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)

# Check if parameters are passed correctly to subcircuits
i1.setCircuit('params2subckt.cir')
htmlPage('Circuit data')
netlist2html('params2subckt.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)

i1.setCircuit('noiseTest.cir')
htmlPage('Circuit data')
netlist2html('params2subckt.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)
i1.setGainType('vi')
i1.setDataType('noise')
i1.setSimType('symbolic')
i1.setSource('V1')
i1.setDetector('V_3')
result = i1.execute()
htmlPage('Symbolic noise anaysis')
noise2html(result)

i1.setSimType('numeric')
result = i1.execute()
htmlPage('Numeric noise anaysis')
noise2html(result)
print(time()-t1)

i1.setCircuit('smallestMatrix.cir')
i1.setSimType('numeric')
i1.setGainType('vi')
i1.setDataType('solve')
i1.setConvType(None)
i1.setDetector('V_1')
result = i1.execute()

V_1 = roundN(result.solve)
V_1_ok = sp.sympify('Matrix([[I_s*R_s]])')

if V_1 == V_1_ok:
    print('smallestMatrix: solve OK!')
else:
    print('smallestMatrix: solve not OK:', V_1)

i1.setDataType('laplace')
result = i1.execute()

V_1 = roundN(result.laplace)
V_1_ok = sp.sympify('I_s*R_s')

if V_1 == V_1_ok:
    print('smallestMatrix: laplace OK!')
else:
    print('smallestMatrix: laplace not OK:', V_1)
