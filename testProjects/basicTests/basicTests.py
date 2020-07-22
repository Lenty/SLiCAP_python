#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 13:24:50 2020

@author: anton
"""

from SLiCAP import *

prj = initProject('Basic tests')
i1 = instruction()

# Check if default model parameters are passed to an element of which the
# model needs to be expanded. This is done for a bipolar transistor model 'QV'.
i1.checkCircuit('defaultParams.cir')
htmlPage('Circuit data')
netlist2html('defaultParams.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)

# Check if parameters are passed correctly to models
i1.checkCircuit('params2model.cir')
htmlPage('Circuit data')
netlist2html('params2model.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)

# Check if parameters are passed correctly to subcircuits
i1.checkCircuit('params2subckt.cir')
htmlPage('Circuit data')
netlist2html('params2subckt.cir')
elementData2html(i1.circuit)
params2html(i1.circuit)

circuits = ['E', 'EZ', 'F', 'G', 'H', 'HZ'];
results = {'E': sp.sympify('-(A_v*R_2*(s*tau_z + 1))/((2*R_1 + R_2)*(s*tau_p + 1))'),
           'EZ': sp.sympify('-(A_v*R_2*(s*tau_z + 1)*(s*tau_zp + 1))/((s*tau_p + 1)*(R + 2*R_1 + R_2 + R*s*tau_zz + 2*R_1*s*tau_zp + R_2*s*tau_zp))'),
           'F': sp.sympify('-(A_i*R_2*(s*tau_z + 1))/((2*R_1 + R_2)*(s*tau_p + 1))'),
           'G': sp.sympify('-(A_y*R_2*R_3*(s*tau_z + 1))/((s*tau_p + 1)*(2*R_1 + R_2 + R_3))'),
           'H': sp.sympify('-(A_z*(s*tau_z + 1))/(2*R_1*(s*tau_p + 1))'),
           'HZ': sp.sympify('-(A_z*(s*tau_z + 1)*(s*tau_zp + 1))/((s*tau_p + 1)*(R + 2*R_1 + R*s*tau_zz + 2*R_1*s*tau_zp))')}
for i in range(len(circuits)):
    print '\nLoop gain test:', circuits[i]
    i1.checkCircuit(circuits[i] + '.cir')
    i1.simType  = 'symbolic'
    i1.dataType = 'laplace'
    i1.gainType = 'loopgain'
    i1.lgRef    = circuits[i] + '1'
    result      = i1.execute()
    lgLaplace   = result.laplace
    if sp.simplify(results[circuits[i]] - lgLaplace) == 0:
        print 'OK!'
    else:
        print lgLaplace
        #print sp.simplify(results[circuits[i]]/lgLaplace)
        print 'Wrong answer.'