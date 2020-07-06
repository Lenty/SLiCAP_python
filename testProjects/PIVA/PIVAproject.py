#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 10:47:15 2020

@author: anton
"""

from SLiCAP import *
t1 = time()

prj = initProject('My first SLiCAP project') # Creates the SLiCAP libraries and the
                          # project HTML index page

fileName = 'PIVA.cir'
i1 = instruction()           # Creates an instance of an instruction object
i1.checkCircuit(fileName)    # Checks and defines the local circuit object and
                             # resets the index page to the project index page

i1.defPar('C_ph', '2.95p')

i1.gainType         = 'vi'
i1.simType          = 'symbolic'
i1.dataType         = 'matrix'
i1.source           = 'V1'
i1.detector         = ['V_Out', 'V_0']
matrixResult        = i1.execute()

i1.simType          = 'numeric'
i1.gainType         = 'gain'
i1.lgRef            = 'F1'

i1.dataType         = 'poles'
polesResult         = i1.execute()

i1.dataType         = 'zeros'
zerosResult         = i1.execute()

i1.dataType         = 'pz'
pzResult            = i1.execute()

i1.dataType         = 'denom'
denom               = i1.execute().denom

i1.dataType         = 'numer'
numer               = i1.execute().numer

i1.dataType         = 'laplace'
result              = i1.execute()
Fs                  = result.laplace
transferCoeffs      = coeffsTransfer(Fs)

# Frequency-domain plots
plotdBmag('magdB', 'dB magnitude', result, 1, 1e3, 100, xscale = 'k')
plotMag('mag', 'Magnitude', result, 1, 1e3, 100, xscale = 'k', yunits = '-')
plotPhase('phase', 'Phase', result, 1, 1e3, 100, xscale = 'k')
plotDelay('delay', 'Delay', result, 1, 1e3, 100, xscale = 'k', yscale = 'u')
plotPZ('pz', 'Poles and zeros', pzResult, xmin = -100, xscale = 'M', yscale = 'M')
plotPZ('pzDominant', 'Dominant poles and zeros', pzResult, xmin = -100, xmax = 0, ymin = -50, ymax = 50, xscale = 'k', yscale = 'k')

i1.gainType         = 'asymptotic'
asymptotic          = i1.execute()
i1.gainType         = 'loopgain'
loopgain            = i1.execute()
i1.gainType         = 'servo'
servo               = i1.execute()
i1.gainType         = 'direct'
direct              = i1.execute()
plotdBmag('magdBfeedbackModel', 'dB magnitude feedback model', [result, asymptotic, loopgain, servo, direct], 1, 1e3, 100, xscale = 'k')

i1.dataType         = 'step'
i1.gainType         = 'gain'
result              = i1.execute()
mu_t                = result.stepResp
# Time-domain plot
plotTime('step', 'Unit step response', result, 0, 50, 100, xscale = 'u', yunits = 'V')

# Find the network solution
i1.gainType         = 'vi'
i1.dataType         = 'solve'
result              = i1.execute()
solution            = result.solve
Dv                  = result.Dv

i1.gainType         = 'gain'
i1.dataType         = 'laplace'
i1.stepVar          = 'I_D'
i1.stepMethod       = 'log'
i1.stepNum          = 7
i1.stepStart        = '1p'
i1.stepStop         = '1u'
i1.step             = True
ini.stepFunction    = True
FsStepped           = i1.execute()

plotdBmag('magdBstepped', 'dB magnitude step I_D', FsStepped, 1, 1e3, 100, xscale = 'k')

i1.dataType         = 'poles'
i1.stepNum          = 200
polesStepped        = i1.execute()
plotPZ('polesStepped', 'Root Locus I_D', polesStepped, xmin = -180, xmax = 20, ymin = -100, ymax = 100, xscale = 'k', yscale = 'k')

i1.dataType         = 'step'
i1.stepNum          = 7
mu_tStepped         = i1.execute().stepResp

# Generate HTML report. Run this section twice if you use forward references.                             
htmlPage('Circuit data')     # Creates an HTML page and a link on the index page
                             # of this circuit
img2html('PIVA.svg', 1200, label = 'figPIVA', caption = 'Schematic diagram of the PIVA')
netlist2html(fileName)       # Netlist of the circuit
elementData2html(i1.circuit) # Element data of a circuit
params2html(i1.circuit)      # Parameters of the last circuit checked

htmlPage('Symbolic matrix equation')
matrices2html(matrixResult, label = 'eq_MNA')

htmlPage('Poles and zeros')
pz2html(polesResult, label = 'tab_poles')
pz2html(zerosResult, label = 'tab_zeros')
pz2html(pzResult, label = 'tab_pz')

htmlPage('Denominator, nominator, transfer function and step response')
eqn2html('D_s', denom, label = 'eq_denom')
eqn2html('N_s', numer, label = 'eq_numer')
eqn2html('F_s', Fs, label = 'eq_gain')
coeffsTransfer2html(transferCoeffs)
eqn2html('f_t', mu_t, label = 'eq_step')

htmlPage('Network solution')
eqn2html(Dv, solution)

htmlPage('Plots')
img2html('magdB.svg', 600, caption='dB magnitude plot of the PIVA transfer.')
img2html('mag.svg', 600, caption='Magnitude plot of the PIVA transfer.')
img2html('phase.svg', 600, caption='Phase plot of the PIVA transfer.')
img2html('delay.svg', 600, caption='Group delay of the PIVA transfer.')
img2html('step.svg', 600, caption='Unit step response of the PIVA.')
img2html('pz.svg', 600, caption='Poles and zeros of the gain of the PIVA.')
img2html('pzDominant.svg', 600, caption='Dominant poles of the gain of the PIVA.')
img2html('magdBfeedbackModel.svg', 600, caption='dB magnitude plots of the of feedback model transfer functions of the PIVA.')
img2html('magdBstepped.svg', 600, caption='dB magnitude plot of the PIVA transfer for different values of the drain current.')
img2html('polesStepped.svg', 600, caption='Poles of the gain for different values of the drain current.')

t2=time()
print '\nTotal time: %3.1fs'%(t2-t1)
#os.system('firefox html/index.html')