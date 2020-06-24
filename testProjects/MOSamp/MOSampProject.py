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
i1.checkCircuit(fileName)    # Checks and defines the local circuit object and
                             # resets the index page to the project index page
                  
i1.gainType = 'vi'
i1.simType  = 'symbolic'
i1.dataType = 'matrix'
i1.source = 'V1'
i1.detector = 'V_out'
matrixResult = i1.execute()

i1.simType = 'numeric'
i1.gainType = 'gain'
i1.lgRef = 'Gm_M1_X1'
i1.dataType = 'poles'
polesResult = i1.execute()
i1.dataType = 'zeros'
zerosResult = i1.execute()
i1.dataType = 'pz'
pzResult = i1.execute()
i1.dataType = 'step'
mu_t = i1.execute().stepResp
i1.dataType = 'denom'
denom = i1.execute().denom
i1.dataType = 'numer'
numer = i1.execute().numer
i1.dataType = 'laplace'
Fs = i1.execute().laplace

i1.step             = True

ini.stepFunction    = True
i1.stepVar          = 'I_source'
i1.stepMethod       = 'lin'
i1.stepNum          = 10
i1.stepStart        = 0
i1.stepStop         = '1u'

FsStepped           = i1.execute().laplace

i1.dataType         = 'pz'

result              = i1.execute()
polesStepped        = result.poles
zerosStepped        = result.zeros
dcValStepped        = result.DCvalue

ini.stepFunction    = True
i1.stepVars         = ['I_source', 'I_sink']
i1.stepArray        = [[0, '10n', '100n', '1u', '10u'], ['10u', '1u', '100n', '10n', 0]]
i1.stepMethod = 'array'

resultArray         = i1.execute()
polesSteppedArray   = resultArray.poles
zerosSteppedArray   = resultArray.zeros
dcValSteppedArray   = resultArray.DCvalue

# Generate HTML report. Run this section twice if you use forward references.
htmlPage('Circuit data')     # Creates an HTML page and a link on the index page
                             # of this circuit
img2html('MOSamp.svg', 800, label = 'figPIVA', caption = 'Schematic diagram of the MOS amplifier')
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