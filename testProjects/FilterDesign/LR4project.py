#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 10:48:40 2020

@author: anton
"""

from SLiCAP import *
t1 = time()

prj = initProject('4-th order Linkwitz-Riley Filter') 
                             # Creates the SLiCAP libraries and the
                             # project HTML index page
fileName = 'LowPassLR.cir'
i1 = instruction()           # Creates an instance of an instruction object
i1.checkCircuit(fileName)    # Checks and defines the local circuit object and
                             # resets the index page to the project index page
                             
i1.source   = 'V1'
i1.detector = 'V_out'
i1.simType  = 'symbolic'
i1.gainType = 'gain'
i1.dataType = 'laplace'
resultLapl  = i1.execute()
transfer    = resultLapl.laplace
i1.gainType = 'vi'
i1.dataType = 'solve'
resultSolve = i1.execute()
solution    = resultSolve.solve
Dv          = resultSolve.Dv

f_o         = sp.Symbol('f_o')
protoType   = sp.sympify('1/(1 + sqrt(2)*s/2/pi/f_o + (s/2/pi/f_o)^2)^2')

protoType   = protoType.subs(f_o, 2000)

compValues  = equateCoeffs(protoType, transfer, noSolve = [f_o])

i1.defPars(compValues)
  
i1.simType  = 'numeric'
i1.gainType = 'gain'
i1.dataType = 'laplace'
result      = i1.execute()
 
figdBmag    = plotdBmag('LR4dBmag', 'dB magnitude characteristic', result, 20, 20e3, 100, xscale='k')
figPgase    = plotPhase('LR4phase', 'phase characteristic', result, 20, 20e3, 100, xscale='k')

htmlPage('Report')

head2html('Prototype function')
eqn2html('P_s', protoType)

head2html('Circuit implementation')
img2html('LowPassLR.svg', 400)

head2html('Transfer of the network')
eqn2html('T_s', transfer)

head2html('Component values')
for key in compValues.keys():
    eqn2html(key, compValues[key])
elementData2html(i1.circuit)  
params2html(i1.circuit)
head2html('solution of the network')
eqn2html(Dv, solution)

head2html('Plots')
img2html('LR4dBmag.svg', 600, caption='dB magnitude of the LR4 filter transfer.')  
img2html('LR4phase.svg', 600, caption='phase plot of the LR4 filter transfer.')    
t2 = time()
print t2-t1, 's'