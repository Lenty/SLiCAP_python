# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 11:28:37 2020

@author: luc_e
"""
from SLiCAP import *

def test_pytest():
    assert 4==4
    
def test_CSresnoise():
    ini.installPath = "C:\\Users\\luc_e\\Documents\\git\\SLiCAP_python\\"
    ini.projectPath = "C:\\Users\\luc_e\\Documents\\git\\SLiCAP_python\\examples\\CSstage\\"
    
    t1 = time()
    prj = initProject('CS stage noise with resistive source')
    ini.circuitPath = "examples\\CSstage\\cir\\"
    ini.maxima = 'C:\\maxima-5.42.2\\bin\\maxima.bat'
    fileName = 'CSresNoise.cir'
    i1 = instruction()
    i1.setCircuit(fileName)
    # Set value of 1/f noise to zero and define drain current at critical inversion
    i1.simType = 'numeric'
    i1.defPar('KF_N18', 0)
    I_D     = i1.getParValue('ID')
    IC      = i1.getParValue('IC_X1')
    IC_CRIT = i1.getParValue('IC_CRIT_X1')
    I_D     = I_D*IC_CRIT/IC
    
    i1.circuit.defPar('ID', I_D)
    R_N   = i1.getParValue('R_N_X1')
    R_s   = i1.getParValue('R_s')
    f_T   = i1.getParValue('f_T_X1')
    g_m   = i1.getParValue('g_m_X1')
    Width = i1.getParValue('W')
    
    i1.setSource('V1')
    i1.setDetector('V_out')
    i1.setGainType('vi')
    i1.setDataType('noise')
    i1.setSimType('numeric')
    noise_result = i1.execute()
    # plotSweep('Inoise', 'Source-referred noise spectrum', noise_result, 1e8, 1e11, 100, funcType = 'inoise', show=False)
    
    # Calculate the noise figure at critical inversion and the given width
    tot_inoise      = rmsNoise(noise_result, 'inoise', 1e9, 5e9)
    tot_inoise_src  = rmsNoise(noise_result, 'inoise', 1e9, 5e9, source = noise_result.source)
    
    NF              = 20*sp.log(tot_inoise/tot_inoise_src)/sp.log(10)
    print(NF)
    shifted = int(NF*1000)
    assert shifted == 652
    