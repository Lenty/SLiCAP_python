#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 20:29:52 2020

@author: anton
"""
from SLiCAPinstruction import *

class SLiCAPproject(object):
    """
    Prototype of a SLiCAPproject:
    
    - Copies the directory structure from the templates subdirectory to the
      project directory in the case it has not yet been created.
    - Creates index.html in the html directory
    - Creates the system libraries
    - Updates 'SLiCAPconfig.py'
    """
    def __init__(self, name):
        self.name = name
        self.lastUpdate = datetime.now()
        self.author = getpass.getuser()
        try:
            ct(INSTALLPATH + 'templates/html', PROJECTPATH + 'html')
        except:
            pass
        try:
            ct(INSTALLPATH + 'templates/cir', PROJECTPATH + 'cir')
        except:
            pass
        try:
            ct(INSTALLPATH + 'templates/csv', PROJECTPATH + 'csv')
        except:
            pass
        try:
            ct(INSTALLPATH + 'templates/img', PROJECTPATH + 'img')
        except:
            pass
        try:
            ct(INSTALLPATH + 'templates/lib', PROJECTPATH + 'lib')
        except:
            pass
        try:
            ct(INSTALLPATH + 'templates/mathml', PROJECTPATH + 'mathml')
        except:
            pass
        try:
            ct(INSTALLPATH + 'templates/tex', PROJECTPATH + 'tex')
        except:
            pass
        try:
            ct(INSTALLPATH + 'templates/txt', PROJECTPATH + 'txt')
        except:
            pass
        if not os.path.exists(PROJECTPATH + 'SLiCAPconfig.py'):
            f = open(INSTALLPATH + 'SLiCAPconfig.py', 'r')
            txt = f.read()
            f.close()
            txt += '\n\n# Project information'
            txt += '\nPROJECT    = ' + '\'' + self.name + '\'' 
            txt += '\nAUTHOR     = ' + '\'' + self.author + '\'' 
            txt += '\nCREATED    = ' + '\'' + str(self.lastUpdate) + '\'' 
            txt += '\nLASTUPDATE = ' + '\'' + str(self.lastUpdate) + '\'' 
            f = open(PROJECTPATH + 'SLiCAPconfig.py', 'w')
            f.write(txt)
            f.close()
        else:
            f = open(PROJECTPATH + 'SLiCAPconfig.py', 'r')
            lines = f.readlines()[0:-1]
            f.close()
            lines.append('LASTUPDATE = ' + '\'' + str(self.lastUpdate) + '\'')
            f = open(PROJECTPATH + 'SLiCAPconfig.py', 'w')
            f.writelines(lines)
            f.close()
        startHTML(name)
        makeLibraries()
    def close(self):
        """
        This clears the list of pages and the dictionaries with labels.
        """
        clearPages()
        clearLabels()
        clearEqLabels()

def initProject(name):
    prj = SLiCAPproject(name)
    return prj

if __name__ == '__main__':
    t1 = time()
    #### initProject #########################################################
    prj = initProject('Test project')
    t2=time()
    #### Select file #########################################################
    fi = 'PIVA.cir'
    #### checkCircuit() ######################################################
    print "\nCheking:", fi
    myCir = checkCircuit(fi )
    t3 = time()
    if myCir.errors == 0:
        #### HTML circuit data ###############################################
        htmlPage('Circuit data')
        img2html('PIVA.svg', 1000, caption='Schematic diagram of the PIVA')
        netlist2html('PIVA.cir')
        elementData2html(myCir, label='elData')
        params2html(myCir, label = 'params')
        t4 = time()
        #### MNA symbolic ####################################################
        MNA = makeMatrices(myCir, myCir.parDefs, numeric = False)
        htmlPage('Symbolic matrix equation')
        matrices2html(MNA)
        csv2html('opAmpSpec.csv', caption = 'Some opamp spec', label='tab-spec')
        t5 = time()
        #### MNA numeric #####################################################
        MNA = makeMatrices(myCir, numeric = True)
        htmlPage('Numeric matrix equation')
        matrices2html(MNA, label='numMat')
        t6=time()
        #### determinant #####################################################
        charpolyM = maxDet(MNA[1])
        htmlPage('Dynamic system analysis')
        text2html('The characteristic equation of the network is:')
        eqn2html(0, charpolyM)
        t7=time()
        text2html('The time function is given by: ' + eqref('eq:ft') +'.')
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
        eqn2html('F(t)', ft, units = '1/sqrt(Hz)', label= 'eq:ft')
        text2html('You can find the matrix equation ' + href('numMat', 'here') + ' and the element data ' + href('elData', 'here'))
        t10=time()
        ######################################################################
        print "init project                 : %fs."%(t2-t1)
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
    #prj.close()
