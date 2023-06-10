#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 18:09:50 2021

@author: anton
"""
from SLiCAP import *
SHOW = False
fileName = 'myFirstVampOPA211complete';
#prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName + '.cir');
htmlPage('Circuit Data');
img2html(fileName +'.svg', 800);
netlist2html(fileName + '.cir');
#
i1.setSimType('numeric');
i1.setSource('V1');
i1.setDetector('V_out');
i1.setLGref('E_O1');
i1.setDataType('laplace');
#
htmlPage('Dynamic behavior');
i1.setGainType('gain');
gain = i1.execute();
i1.setGainType('asymptotic');
asymptotic = i1.execute();
i1.setGainType('loopgain');
loopgain = i1.execute();
i1.setGainType('servo');
servo = i1.execute();
i1.setGainType('direct');
direct = i1.execute();
figMag = plotSweep('magComplete', 'Magnitude plots', [asymptotic, loopgain, servo, direct, gain], 1, 10e6, 500, funcType='dBmag', show = SHOW);
fig2html(figMag, 600);
figPhase = plotSweep('phaseComplete', 'Phase plots', [asymptotic, loopgain, servo, direct, gain], 1, 10e6, 500, funcType='phase', show = SHOW);
fig2html(figPhase, 600);
i1.setGainType('gain');
i1.setDataType('pz');
pz2html(i1.execute());
i1.setGainType('loopgain');
i1.setDataType('pz');
lgPZ = i1.execute();
pz2html(lgPZ);
i1.setGainType('servo');
i1.setDataType('poles');
i1.setStepVar('A_0');
i1.setStepNum(100);
i1.setStepStart(1);
i1.setStepStop(667E3);
i1.setStepMethod('log');
i1.stepOn();
RL = i1.execute();
RLplot = plotPZ('RLcomplete', 'Root Locus', [lgPZ, RL], xmin=-6, xmax=0, xscale='M', ymin=-3, ymax=3, yscale='M', show = SHOW);
fig2html(RLplot, 600);
i1.setDataType('step');
i1.setGainType('gain');
i1.stepOff();
figStep = plotSweep('stepComplete', 'Unit step response', i1.execute(), 0, 2, 200, sweepScale='u', show = SHOW);
fig2html(figStep, 600);