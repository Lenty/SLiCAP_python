#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 10:47:15 2020

@author: anton
"""    
from SLiCAP import *
t1 = time()
prj = initProject('CMOS 18 amplifier project') # Creates the SLiCAP libraries and the
                             # project HTML index page

fileName = 'MOSamp.cir'
i1 = instruction()           # Creates an instance of an instruction object
i1.setCircuit(fileName)      # Checks and defines the local circuit object and
                             # sets the index page to the circuit index page

i1.setSource('V1')
i1.setDetector('V_out')

i1.setGainType('vi')
i1.setSimType('symbolic')
i1.setDataType('matrix')
matrixResult = i1.execute()

i1.setSimType('numeric')
i1.setGainType('gain')
i1.setLGref('Gm_M1_X1')
i1.setDataType('poles')
polesResult = i1.execute()
i1.setDataType('zeros')
zerosResult = i1.execute()
i1.setDataType('pz')
pzResult = i1.execute()
i1.setDataType('step')
mu_t = i1.execute().stepResp
i1.setDataType('denom')
denom = i1.execute().denom
i1.setDataType('numer')
numer = i1.execute().numer
i1.setDataType('laplace')
Fs = i1.execute().laplace

i1.setStepVar('I_source')
i1.setStepMethod('lin')
i1.setStepNum(10)
i1.setStepStart(0)
i1.setStepStop('1u')

FsStepped = i1.execute().laplace

i1.setDataType('pz')
result              = i1.execute()
polesStepped        = result.poles
zerosStepped        = result.zeros
dcValStepped        = result.DCvalue

i1.setStepVars(['I_source', 'I_sink'])

i1.stepArray        = [[0, '10n', '100n', '1u', '10u'], ['10u', '1u', '100n', '10n', 0]]

i1.stepMethod = 'array'
i1.stepOn()

resultArray         = i1.execute()

polesSteppedArray   = resultArray.poles
zerosSteppedArray   = resultArray.zeros
dcValSteppedArray   = resultArray.DCvalue

# Generate HTML report. Run this section twice if you use forward references.
htmlPage('Circuit data')     # Creates an HTML page and a link on the index page
                             # of this circuit
img2html('MOSamp.svg', 800, label = 'figMOS2', caption = 'Schematic diagram of the MOS amplifier')
netlist2html(fileName)       # Netlist of the circuit
elementData2html(i1.circuit) # Element data of a circuit
params2html(i1.circuit)      # Parameters of the last circuit checked

htmlPage('Symbolic matrix equation')
matrices2html(matrixResult, label = 'eq_MNA')

htmlPage('Poles and zeros')
pz2html(polesResult, label = 'tab_poles')
pz2html(zerosResult, label = 'tab_zeros')
pz2html(pzResult, label = 'tab_pz')

htmlPage('Denominator, nominator and transfer function')
eqn2html('D_s', denom, label = 'eq_denom')
eqn2html('N_s', numer, label = 'eq_numer')
eqn2html('F_s', Fs, label = 'eq_gain')

t2=time()
print '\nTotal time: %3.1fs'%(t2-t1)
#os.system('firefox html/index.html')