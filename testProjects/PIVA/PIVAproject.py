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
i1.setCircuit(fileName)      # Checks and defines the local circuit object and
                             # resets the index page to the project index page

i1.defPar('C_ph', '2.95p')

htmlPage('Circuit data')     # Creates an HTML page and a link on the index page
                             # of this circuit
img2html('PIVA.svg', 800, label = 'figPIVA', caption = 'Schematic diagram of the PIVA')
netlist2html(fileName)       # Netlist of the circuit
elementData2html(i1.circuit) # Element data of a circuit
params2html(i1.circuit)      # Parameters of the last circuit checked

i1.setGainType ('vi')
i1.setSimType('symbolic')
i1.setDataType('matrix')
i1.setSource('V1')
i1.setDetector(['V_Out', 'V_0'])
matrixResult = i1.execute()

i1.setSimType('numeric')
i1.setGainType('gain')
i1.setLGref('F1')
i1.setDataType('poles')
polesResult = i1.execute()

i1.setDataType('zeros')
zerosResult = i1.execute()

i1.setDataType('pz')
pzResult = i1.execute()

i1.setDataType('denom')
denom = i1.execute().denom

i1.setDataType('numer')
numer = i1.execute().numer

i1.setDataType('laplace')
result = i1.execute()
Fs = result.laplace
transferCoeffs = coeffsTransfer(Fs)

# Frequency-domain plots
figdBmag = plotdBmag('dBmag', 'dB magnitude', result, 1, 1e3, 100, xscale = 'k')
figMag   = plotMag('mag', 'Magnitude', result, 1, 1e3, 100, xscale = 'k', yunits = '-')
figPhase = plotPhase('phase', 'Phase', result, 1, 1e3, 100, xscale = 'k')
figDelay = plotDelay('delay', 'Delay', result, 1, 1e3, 100, xscale = 'k', yscale = 'u')
figPolar = plotPolar('polar', 'Polar' , result, 1, 1e3, 100, fscale = 'k')
figdBpolar = plotdBpolar('dBpolar', 'dB polar' , result, 1, 1e3, 100, fscale = 'k')
figPZ = plotPZ('PZ', 'Poles and zeros', pzResult, xmin = -100, xscale = 'M', yscale = 'M')
figPZd = plotPZ('PZd', 'Dominant poles and zeros', pzResult, xmin = -100, xmax = 0, ymin = -50, ymax = 50, xscale = 'k', yscale = 'k')

i1.setGainType('asymptotic')
asymptotic = i1.execute()
i1.setGainType('loopgain')
loopgain = i1.execute()
i1.setGainType('servo')
servo = i1.execute()
i1.setGainType('direct')
direct = i1.execute()
figdBmagA = plotdBmag('magA', 'dB magnitude feedback model', [result, asymptotic, loopgain, servo, direct], 1, 1e3, 100, xscale = 'k')

i1.setDataType('step')
i1.setGainType('gain')
result = i1.execute()
mu_t = result.stepResp
# Time-domain plot
figStep = plotTime('step', 'Unit step response', result, 0, 50, 100, xscale = 'u', yunits = 'V')

# Find the network solution
i1.setGainType('vi')
i1.setDataType('solve')
result = i1.execute()
solution = result.solve
Dv = result.Dv

i1.setGainType('gain')
i1.setDataType('laplace')
i1.setStepVar('I_D')
i1.setStepMethod('log')
i1.setStepNum(7)
i1.setStepStart('1p')
i1.setStepStop('1u')
i1.stepOn()
FsStepped = i1.execute()

figdBs = plotdBmag('dBs', 'dB magnitude step I_D', FsStepped, 1, 1e3, 100, xscale = 'k')

i1.setDataType('poles')
i1.setStepNum(200)
polesStepped = i1.execute()
figRL = plotPZ('RL', 'Root Locus I_D', polesStepped, xmin = -180, xmax = 20, ymin = -100, ymax = 100, xscale = 'k', yscale = 'k')

i1.setDataType('step')
i1.setStepNum(7)
mu_tStepped = i1.execute().stepResp

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
fig2html(figdBmag, 600, caption='dB magnitude plot of the PIVA transfer.')
fig2html(figMag, 600, caption='Magnitude plot of the PIVA transfer.')
fig2html(figPhase, 600, caption='Phase plot of the PIVA transfer.')
fig2html(figDelay, 600, caption='Group delay of the PIVA transfer.')
fig2html(figdBmagA, 600, caption='Asymptotic-gain model parameter dB magnitude plots of the PIVA transfer.')
fig2html(figPolar, 600, caption ='Polar plot of the PIVA transfer.')
fig2html(figdBpolar, 600, caption ='dB polar plot of the PIVA transfer.')
fig2html(figStep, 600, caption='Unit step response of the PIVA.')
fig2html(figPZ, 600, caption='Poles and zeros of the gain of the PIVA.')
fig2html(figPZd,  600, caption='Dominant poles of the gain of the PIVA.')
fig2html(figdBs, 600, caption='dB magnitude plot of the PIVA transfer for different values of the drain current.')
fig2html(figRL, 600, caption='Poles of the gain for different values of the drain current.')

t2=time()
print '\nTotal time: %3.1fs'%(t2-t1)
#os.system('firefox html/index.html')