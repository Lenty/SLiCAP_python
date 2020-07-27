#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 19:15:00 2020

@author: anton
"""

from SLiCAP import *
t1 = time()

prj = initProject('NMOS EKV polts') # Creates the SLiCAP libraries and the
                             # project HTML index page

fileName = 'mosEKVplots.cir'
i1 = instruction()           # Creates an instance of an instruction object
i1.setCircuit(fileName)      # Checks and defines the local circuit object and
                             # sets the index page to the circuit index page

data = paramPlot()

# Ids-Vds with Vgs as parameter
data.xVar    = 'V_D'
data.sVar    = 'V_D'
data.yVar    = 'I_DS_X1'
data.pVar    = 'V_G'
data.sStart  = 0
data.sStop   = 1.8
data.sNum    = 50
data.sMethod = 'lin'
data.pStart  = 0
data.pStop   = 1.8
data.pNum    = 10
data.pMethod = 'lin'
i1.stepParams(data)
fig_Ids_Vds = plotParams('IdsVds', '$I_{ds}(V_{ds})$', data, xunits = 'V', yunits = 'A', punits = 'V', yscale = 'u')

# Ids-Vgs with Vds as parameter
data.xVar    = 'V_G'
data.sVar    = 'V_G'
data.pVar    = 'V_D'
i1.stepParams(data)
fig_Ids_Vgs = plotParams('IdsVgs', '$I_{ds}(V_{gs})$', data, xunits = 'V', yunits = 'A', punits = 'V', yscale = 'u')

# gm-Ids with Vds as parameter, sweep parameter = Vgs
data.xVar    = 'I_DS_X1'
data.sVar    = 'V_G'
data.yVar    = 'g_m_X1'
i1.stepParams(data)
fig_gm_Ids = plotParams('gmIds', '$g_{m}(I_{ds})$', data, xunits = 'A', yunits = 'S', punits = 'V', xscale = 'u', yscale = 'u')

# fT-Ids with Vds as parameter, sweep parameter = Vgs
data.xVar    = 'I_DS_X1'
data.sVar    = 'V_G'
data.yVar    = 'f_T_X1'
i1.stepParams(data)
fig_fT_Ids = plotParams('fTIds', '$f_{T}(I_{ds})$', data, xunits = 'A', yunits = 'Hz', punits = 'V', xscale = 'u', yscale = 'G')

# Ciss-Vgs with Vds as parameter
data.xVar    = 'V_G'
data.yVar    = 'c_iss_X1'
i1.stepParams(data)
fig_CissVg = plotParams('CissVg', '$c_{iss}(V_{gs})$', data, xunits = 'V', yunits = 'F', punits = 'V', xscale = '', yscale = 'f')

htmlPage('Circuit data')
netlist2html(fileName)
elementData2html(i1.circuit)
params2html(i1.circuit)
# Put the plots on a page
htmlPage('CMOS18 EKV model plots')
fig2html(fig_Ids_Vds, 600)
fig2html(fig_Ids_Vgs, 600)
fig2html(fig_gm_Ids, 600)
fig2html(fig_fT_Ids, 600)
fig2html(fig_CissVg, 600)

t2=time()
print t2-t1,'s'