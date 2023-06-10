#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 17:34:52 2021

@author: anton
"""
from SLiCAP import *
from SLiCAP.SLiCAPdocTools import *

SHOW = True
fileName = 'myFirstVampOPA211compensated';
prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName + '.cir');

i1.setSimType('numeric');
i1.setSource('V1');
i1.setDetector('V_out');
i1.setLGref('E_O1');
i1.setDataType('laplace');
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

figMag = plotSweep('magComp', 'Magnitude plots', 
                   [asymptotic, loopgain, servo, direct, gain], 
                   100, 10e6, 500, funcType='dBmag', show = SHOW);
figPhase = plotSweep('phaseComp', 'Phase plots', 
                     [asymptotic, loopgain, servo, direct, gain], 
                     100, 10e6, 500, funcType='phase', show = SHOW);

i1.setGainType('gain');
i1.setDataType('pz');
gainPZ = i1.execute()

i1.setGainType('loopgain');
i1.setDataType('pz');
lgPZ = i1.execute();

i1.setGainType('servo');
i1.setDataType('poles');
i1.setStepVar('A_0');
i1.setStepNum(100);
i1.setStepStart(1);
i1.setStepStop(667E3);
i1.setStepMethod('log');
i1.stepOn();
RL = i1.execute();
RLplot = plotPZ('RLcomp', 'Root Locus', [lgPZ, RL], 
                xmin=-6, xmax=0, xscale='M', ymin=-3, ymax=3, yscale='M', show = SHOW);

i1.setDataType('step');
i1.setGainType('gain');
i1.stepOff();
figStep = plotSweep('stepComp', 'Unit step response', 
                    i1.execute(), 0, 2, 200, sweepScale='u', show = SHOW);

transferCoeffs = coeffsTransfer(gain.laplace)
# Generate report data
saveRST(netlist2RST(fileName + '.cir', lineRange='5-9', firstNumber='5'), fileName + '_netlist')
saveRST(elementData2RST(i1.circuit, label='table-elementData'), fileName + '_elementData')
saveRST(parDefs2RST(i1.circuit), fileName + '_parDefs')
saveRST(params2RST(i1.circuit), fileName + '_params')
saveRST(matrices2RST(gain.Iv, gain.M, gain.Dv), fileName + '_matrices')
saveRST(eqn2RST(sp.Symbol('A_v'), gain.laplace), fileName + '_gain')
saveRST(eqn2RST(sp.Symbol('A_v_oo'), asymptotic.laplace), fileName + '_asymptotic')
saveRST(eqn2RST(sp.Symbol('L'), loopgain.laplace), fileName + '_loopgain')
saveRST(eqn2RST(sp.Symbol('S'), servo.laplace), fileName + '_servo')
saveRST(eqn2RST(sp.Symbol('rho'), direct.laplace), fileName + '_direct')
saveRST(pz2RST(gainPZ), fileName + '_gainPZ')

saveTEX(netlist2TEX(fileName + '.cir', lineRange=''), fileName + '_netlist')
saveTEX(elementData2TEX(i1.circuit), fileName + '_elementData')
saveTEX(parDefs2TEX(i1.circuit), fileName + '_parDefs')
saveTEX(params2TEX(i1.circuit), fileName + '_params')
saveTEX(matrices2TEX(gain.Iv, gain.M, gain.Dv), fileName + '_matrices')
saveTEX(eqn2TEX(sp.Symbol('A_v'), gain.laplace), fileName + '_gain')
saveTEX(eqn2TEX(sp.Symbol('A_v_oo'), asymptotic.laplace), fileName + '_asymptotic')
saveTEX(eqn2TEX(sp.Symbol('L'), loopgain.laplace), fileName + '_loopgain')
saveTEX(eqn2TEX(sp.Symbol('S'), servo.laplace), fileName + '_servo')
saveTEX(eqn2TEX(sp.Symbol('rho'), direct.laplace), fileName + '_direct')
saveTEX(pz2TEX(gainPZ), fileName + '_gainPZ')
saveTEX(coeffsTransfer2TEX(transferCoeffs, caption='Normalized coefficients of the gain.'), fileName + '_gainCoeffs')