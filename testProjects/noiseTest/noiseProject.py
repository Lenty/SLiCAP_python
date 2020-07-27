#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 14:59:59 2020

@author: anton
"""
from SLiCAP import *
t1 = time()

prj = initProject('Noise project') # Creates the SLiCAP libraries and the
                             # project HTML index page

fileName = 'noiseTest.cir'
i1 = instruction()           # Creates an instance of an instruction object
i1.setCircuit(fileName)      # Checks and defines the local circuit object and
                             # sets the index page to the circuit index page
i1.setSource('V1')
i1.setDetector('V_2')
i1.setGainType('vi')
i1.setDataType('noise')
i1.setSimType('numeric')
noiseResults = i1.execute()

fig_onoise = plotSweep('onoise', 'Detector-refferred noise', noiseResults, 0.1, '1M', 200, noiseSources = 'all')

rmsInoise = rmsNoise(noiseResults, 'inoise', 0.1, '1M')
rmsSnoise = rmsNoise(noiseResults, 'inoise', 0.1, '1M', source = 'V1')

noiseFigure = rmsInoise/rmsSnoise

i1.stepOn()
i1.setStepMethod('lin')
i1.setStepVar('R_p')
i1.setStepStart(200)
i1.setStepStop('1k')
i1.setStepNum(5)
noiseResultsStepped = i1.execute() 

fig_onoiseStepped   = plotSweep('inoiseStepped', 'Source-refferred noise', noiseResultsStepped, 0.1, '1M', 200, funcType = 'inoise', noiseSources = 'I1')

htmlPage('Noise')
noise2html(noiseResults)
head2html('Intrgrated noise')
head3html('Source-referred RMS noise')
eqn2html('V_ns', rmsInoise, units='V')
text2html('The noise figure $F$ equals:')
eqn2html('F', 20*np.log10(float(noiseFigure)), units='dB')
fig2html(fig_onoise, 600)
fig2html(fig_onoiseStepped, 600)
t2 = time()
print '\n',t2-t1,'s'