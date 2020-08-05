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
                             # sets the index page to the circuit index page

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
figdBmag = plotSweep('dBmag', 'dB magnitude', result, 1, 1e3, 100, sweepScale = 'k', funcType = 'dBmag')
figMag   = plotSweep('mag', 'Magnitude', result, 1, 1e3, 100, sweepScale = 'k', funcType = 'mag', yUnits = '-')
figPhase = plotSweep('phase', 'Phase', result, 1, 1e3, 100, sweepScale = 'k', funcType = 'phase')
figDelay = plotSweep('delay', 'Delay', result, 1, 1e3, 100, sweepScale = 'k', yScale = 'u', funcType = 'delay')
figPolar = plotSweep('polar', 'Polar' , result, 1, 1e3, 100, sweepScale = 'k', axisType = 'polar', funcType = 'mag')
figdBpolar = plotSweep('dBpolar', 'dB polar' , result, 1, 1e3, 100, funcType = 'dBmag', sweepScale = 'k', axisType = 'polar')
figPZ = plotPZ('PZ', 'Poles and zeros', pzResult, xmin = -100, xscale = 'M', yscale = 'M')
figPZd = plotPZ('PZd', 'Dominant poles and zeros', pzResult, xmin = -100, xmax = 0, ymin = -50, ymax = 50, xscale = 'k', yscale = 'k')

i1.setGainType('asymptotic')
asymptotic = i1.execute()
i1.setGainType('loopgain')
loopgain = i1.execute()

# Let us calculate the phase margin

print phaseMargin(loopgain.laplace)

i1.setStepVar('I_D')
i1.setStepMethod('log')
i1.setStepNum(25)
i1.setStepStart('10p')
i1.setStepStop('1m')
i1.stepOn()
loopgainStepped = i1.execute()
PM2p95 = [i1.stepList, phaseMargin(loopgainStepped.laplace)[0]]
i1.defPar('C_ph', '1.5p')
loopgainStepped_1p5 = i1.execute()
PM1p5 = [i1.stepList, phaseMargin(loopgainStepped_1p5.laplace)[0]]
plotData = {'$C_{ph}=2.95$p': PM2p95, '$C_{ph}=1.5$p': PM1p5}
figPM = plot('PM', 'Phase margin versus $I_D$', 'semilogx', plotData, xName = '$' + sp.latex(i1.stepVar) + '$', xScale = 'u', xUnits = 'A', yName = 'Phase margin', yUnits = 'deg', show = True)

i1.defPar('C_ph', '2.95p')
i1.stepOff()
i1.setGainType('servo')
servo = i1.execute()
i1.setGainType('direct')
direct = i1.execute()
figdBmagA = plotSweep('magA', 'dB magnitude feedback model', [result, asymptotic, loopgain, servo, direct], 1, 1e3, 100, funcType = 'dBmag', sweepScale = 'k')

i1.setDataType('step')
i1.setGainType('gain')
a_t = i1.execute()

figStep = plotSweep('step', 'step response', a_t, 0, 50, 100, sweepScale = 'u', yUnits = 'V')

i1.stepOn()
i1.setStepNum(7)
i1.setStepStart('1p')
i1.setStepStop('1u')
i1.setGainType('gain')
i1.setDataType('laplace')
FsStepped = i1.execute()

figdBs = plotSweep('dBs', 'dB magnitude step I_D', FsStepped, 1, 1e3, 100, funcType = 'dBmag', sweepScale = 'k')

i1.setDataType('poles')
i1.setStepNum(200)
polesStepped = i1.execute()
figRL = plotPZ('RL', 'Root Locus I_D', polesStepped, xmin = -180, xmax = 20, ymin = -100, ymax = 100, xscale = 'k', yscale = 'k')

i1.setDataType('step')
i1.setStepNum(7)
a_tStepped = i1.execute()
figStepped = plotSweep('stepped', 'step response I_D', a_tStepped, 0, 50, 100, sweepScale = 'u', yUnits = 'V')

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
eqn2html('a_t', a_t, label = 'eq_step')

htmlPage('Plots')
fig2html(figdBmag, 600, label = 'figdBmag',  caption='dB magnitude plot of the PIVA transfer.')
fig2html(figMag, 600, label = 'figMag', caption='Magnitude plot of the PIVA transfer.')
fig2html(figPhase, 600, label = 'figPhase', caption='Phase plot of the PIVA transfer.')
fig2html(figDelay, 600, label = 'figDelay', caption='Group delay of the PIVA transfer.')
fig2html(figdBmagA, 600, label = 'figdBmagA', caption='Asymptotic-gain model parameter dB magnitude plots of the PIVA transfer.')
fig2html(figPM, 600, label = 'figPM', caption='Phase margin versus drain current for different values of the phantom zero capacitance.')
fig2html(figPolar, 600, label = 'figPolar', caption ='Polar plot of the PIVA transfer.')
fig2html(figdBpolar, 600, label = 'figdBpolar', caption ='dB polar plot of the PIVA transfer.')
fig2html(figStep, 600, label = 'figStep', caption='Unit step response of the PIVA.')
fig2html(figStepped, 600, label = 'figStepped', caption='Unit step response of the PIVA versus $I_D$.')
fig2html(figPZ, 600, label = 'figPZ', caption='Poles and zeros of the gain of the PIVA.')
fig2html(figPZd,  600, label = 'figPZd', caption='Dominant poles of the gain of the PIVA.')
fig2html(figdBs, 600, label = 'figdBs', caption='dB magnitude plot of the PIVA transfer for different values of the drain current.')
fig2html(figRL, 600, label = 'figRL', caption='Poles of the gain for different values of the drain current.')

links2html()
t2=time()
print '\nTotal time: %3.1fs'%(t2-t1)
#os.system('firefox html/index.html')