#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 18:20:46 2021

@author: anton
"""
from SLiCAP import *
from SLiCAP.SLiCAPdocTools import *

SHOW = False
fileName = 'myFirstVampOPA211completeNoise';
prj = initProject(fileName)
i1 = instruction()
i1.setCircuit(fileName + '.cir');
htmlPage('Circuit Data');
img2html(fileName + '.svg', 1000);
netlist2html(fileName + '.cir');
#
htmlPage('Noise');
i1.setSimType('numeric');
i1.setSource('V1');
i1.setDetector('V_out');
i1.setDataType('noise');
i1.setGainType('vi');
noiseResult = i1.execute();

# maxima timeout fails under windows/anaconda

try:
    print("Trying symbolic integration with maxima CAS.")
    RMSout = rmsNoise(noiseResult, 'onoise', 100, 0.7854e6)
    RMSoutSource = rmsNoise(noiseResult, 'onoise', 100, 0.7854e6, source='V1')
    NF = 20*log10(RMSout/RMSoutSource);
    print("Performed symbolic integration with maxima CAS.")
except:
    try:
        print("Trying numeric integration with scipy.")
        from scipy.integrate import quad
        oNoise = sp.lambdify(ini.frequency, noiseResult.onoise)
        srcOnoise = sp.lambdify(ini.frequency, noiseResult.onoiseTerms['V1'])
        sqOnoise = quad(oNoise, 100, 0.7854e6)[0]
        sqOnoiseSrc = quad(srcOnoise, 100, 0.7854e6)[0]
        NF = sp.N(10*np.log10(sqOnoise/sqOnoiseSrc))
        print("Performed numeric integration with scipy.")
    except:
        print("Could not perform numeric integration with scipy.")

# RST report
        
saveRST(noiseContribs2RST(noiseResult), fileName + '_noise')
saveRST(eqn2RST(sp.Symbol('NF'), NF, units='dB'), fileName + '_NF')

substitutions = {}
substitutions['NF_num'] = expr2RST(NF, units='dB')
substitutions['NF_eqn'] = eqn2RSTinline(sp.Symbol('NF'), NF, units='dB')

save2RSTinline(substitutions, fileName + '_substitutions')

# TEX report

saveTEX(noiseContribs2TEX(noiseResult, append2caption=fileName, label='table-noiseContribs'), fileName + '_noiseContribs')
saveTEX(eqn2TEX('S_o', noiseResult.onoise, label='eq-onoise'), fileName + '_onoise')
saveTEX(eqn2TEX('NF', NF, units='dB'), fileName + '_NF')

substitutions = {}
substitutions['NF_num'] = expr2TEX(NF, units='dB')
substitutions['NF_eqn'] = eqn2TEXinline(sp.Symbol('NF'), NF, units='dB')

save2TEXinline(substitutions)