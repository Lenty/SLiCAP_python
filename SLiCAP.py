#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 20:29:52 2020

@author: anton
"""
from SLiCAPpythonMaxima import *

def initProject(projectName):
    makeLibraries()
    startHTML(projectName)
    return
  
if __name__ == '__main__':
    t1 = time()
    #### initProject #########################################################
    initProject('Test project')
    t2=time()
    #### Select file #########################################################
    fi = 'MOSamp.cir'
    #### checkCircuit() ######################################################
    print "\nCheking:", fi
    myCir = checkCircuit(fi )
    t3 = time()
    if myCir.errors == 0:
        #### HTML circuit data ###############################################
        htmlPage('Circuit data')
        netlist2html()
        #elementData2html()
        #params2html()
        t4 = time()
        #### MNA symbolic ####################################################
        MNA = makeMatrices(myCir, False)
        htmlPage('Symbolic matrix equation')
        matrices2html(MNA)
        t5 = time()
        #### MNA numeric #####################################################
        MNA = makeMatrices(myCir, True)
        htmlPage('Numeric matrix equation')
        matrices2html(MNA)
        t6=time()
        #### determinant #####################################################
        charpolyM = maxDet(MNA[1])
        htmlPage('Dynamic system analysis')
        text2html('The characteristic equation of the network is:')
        eqn2html(0, charpolyM)
        t7=time()
        #### poles ###########################################################
        roots = numRoots(charpolyM, LAPLACE)
        pz2html((roots, [], False)) # arg = (poles, zeros, DC gain)
        t8=time()
        #### rebuild Laplace rational ########################################
        Fs = makeLaplaceRational(1, [], roots)
        t9=time()
        #### inverse Laplace Transform #######################################
        ft = maxILT(Fs)
        text2html('The inverse Laplace Transform is found as:')
        eqn2html('F(s)', ft)
        t10=time()
        
        print "\ninit project                 : %fs."%(t2-t1)
        print "checkCircuit                 : %fs."%(t3-t2)
        print "circuit data on HTML         : %fs."%(t4-t3)
        print "makeMatrices symbolic        : %fs."%(t5-t4)
        print "makeMatrices numeric         : %fs."%(t6-t5)
        print "determinant Maxima           : %fs."%(t7-t6)
        print "poles with Numpy             : %fs."%(t8-t7)
        print "construct Fs                 : %fs."%(t9-t8)
        print "inverse Laplace with Maxima  : %fs.\n"%(t10-t9)
        print "Total time                   : %fs."%(t10-t1)
    else:
        print "Errors found."