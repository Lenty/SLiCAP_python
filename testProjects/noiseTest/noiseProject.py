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
i1.checkCircuit(fileName)    # Checks and defines the local circuit object and
                             # resets the index page to the project index page
i1.source            = 'V1'
i1.detector          = 'V_2'
i1.gainType          = 'vi'
i1.dataType          = 'noise'
i1.simType           = 'numeric'
noiseResults         = i1.execute()

fig_onoise           = plotNoise('onoise', 'Detector-refferred noise', noiseResults, 0.1, '1M', 200, noise='onoise', sources = 'all')

rmsInoise            = rmsNoise(noiseResults, 'inoise', 0.1, '1M')
rmsSnoise            = rmsNoise(noiseResults, 'inoise', 0.1, '1M', source = 'V1')

noiseFigure          = rmsInoise/rmsSnoise

i1.step = True
i1.stepMethod        = 'lin'
i1.stepVar           = 'R_p'
i1.stepStart         = 200
i1.stepStop          = '1k'
i1.stepNum           = '5'
ini.stepFunction     = True
noiseResultsStepped  = i1.execute() 
fig_onoiseStepped    = plotNoise('inoiseStepped', 'Source-refferred noise', noiseResultsStepped, 0.1, '1M', 200, noise='inoise', sources = 'I1')

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