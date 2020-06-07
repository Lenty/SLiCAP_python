#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 10:47:15 2020

@author: anton
"""

from SLiCAP import *
t1 = time()
prj = initProject('PIVA') # Creates the SLiCAP libraries and the
                          # project HTML index page

fileName = 'PIVA.cir'
i1 = instruction()           # Creates an instance of an instruction object
i1.checkCircuit(fileName)    # Checks and defines the local circuit object and
                             # resets the index page to the project index page
                             
htmlPage('Circuit data')     # Creates an HTML page and a link on the index page
                             # of this circuit
img2html('PIVA.svg', 1000, label = 'figPIVA', caption = 'Schematic diagram of the PIVA')
netlist2html(fileName)       # Netlist of the circuit
elementData2html(i1.circuit) # Element data of a circuit
params2html(i1.circuit)      # Parameters of the last circuit checked

htmlPage('Symbolic matrix equation')
i1.gainType = 'vi'
i1.simType  = 'symbolic'
i1.dataType = 'matrix'
i1.source = 'V1'
i1.detector = ['V_Out', 'V_0']
matrices2html(i1.execute(), label = 'eq_MNA')

htmlPage('Poles and zeros')
i1.simType = 'numeric'
i1.gainType = 'gain'
i1.lgRef = 'F1'
i1.dataType = 'poles'
pz2html(i1.execute(), label = 'tab_poles')
i1.dataType = 'zeros'
pz2html(i1.execute(), label = 'tab_zeros')
i1.dataType = 'pz'
pz2html(i1.execute(), label = 'tab_pz')

htmlPage('Denominator, nominator and transfer function')
i1.dataType = 'denom'
eqn2html('D_s', i1.execute().results.denom, label = 'eq_denom')
i1.dataType = 'numer'
eqn2html('N_s', i1.execute().results.numer, label = 'eq_numer')
i1.dataType = 'laplace'
Fs = i1.execute().results.laplace
eqn2html('F_s', Fs, label = 'eq_gain')

t2=time()
print(t2-t1)
#os.system('firefox html/index.html')