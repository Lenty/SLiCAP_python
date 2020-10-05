# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 11:28:37 2020

@author: luc_e
"""
from SLiCAP import *
import os

def test_pytest():
    assert 4==4

def test_lex():
    fi = 'tests/test_files/myFirstRCnetwork.cir'
    print(fi)
    lexer = tokenize(fi)
    tok = lexer.token()
    while tok:
        print(tok)
        tok = lexer.token()
    print('\nnumber of errors =', lexer.errCount, '\n')
    #Add assert statement

def test_lex2():
    #Alter circuit to cause an error
    fi = 'tests/test_files/myFirstRCnetwork.cir'
    print(fi)
    lexer = tokenize(fi)
    tok = lexer.token()
    while tok:
        print(tok)
        tok = lexer.token()
    print('\nnumber of errors =', lexer.errCount, '\n')
    #Add assert statement

def test_matrix():
        s = ini.Laplace
        MNA = matrix([[5.0e-12*s + 0.01, 0, 0, -5.0e-12*s - 0.01, 0, 0, 0, 0, 1],
                      [0, 1.98e-11*s + 0.0001, -1.2e-11*s, -1.8e-12*s - 1.0e-5, 0, 0, 0, 0, 0],
                      [0, -1.2e-11*s, 2.8e-11*s + 0.001, 0, -1.0e-11*s - 0.001, 0, 0, -1, 0],
                      [-5.0e-12*s - 0.01, -1.8e-12*s - 1.0e-5, 0, 1.0068e-9*s + 0.01101, 0, 0, 1, 0, 0],
                      [0, 0, -1.0e-11*s - 0.001, 0, 1.0e-11*s + 0.001, 1, 0, 1, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, -1.0e-6*s, -3.1623e-11*s, 0],
                      [0, 0, -1, 0, 1, 0, -3.1623e-11*s, -1.0e-9*s, 0],
                      [2.048e-20*s**3 + 2.688e-11*s**2 + 0.0016*s + 1, 0, 0, 0, 0, 0, 0, 0, 0]])
        print(MNA.determinant())

def test_yacc():
    ini.installPath = os.getcwd() + '/'
    ini.projectPath = ini.installPath + 'examples/CSstage/'
    ini.circuitPath = ini.projectPath + 'cir/'
    ini.htmlPath    = ini.projectPath + 'html/'
    ini.htmlIndex   = 'index.html'
    ini.lastUpdate  = datetime.now()
    LIB = makeLibraries()
    fi = 'CSresNoise.cir'
    print("\nCheking:", fi)
    myCir = checkCircuit(fi)
    keys = list(myCir.elements.keys())

    for key in keys:
        el = myCir.elements[key]
        print('\nElement    :', key)
        print('Nodes      :', el.nodes)
        print('Refs       :', el.refs)
        print('Model      :', el.model)
        print('Params     :')
        for par in list(el.params.keys()):
            print(' ', par, '=', el.params[par])

    print('\nCircuit parameter definitions:')
    for par in list(myCir.parDefs.keys()):
        print(' ', par, '=', myCir.parDefs[par]    )
    for el in list(myCir.elements.keys()):
        for par in list( myCir.elements[el].params.keys()):
            parNum = fullSubs(myCir.elements[el].params[par], myCir.parDefs)
            print(el,'\t', par, sp.N(parNum, ini.disp))

def test_execute():
    s = sp.Symbol('s')
    loopGainNumer = -s*(1 + s/20)*(1 + s/40)/2
    loopGainDenom = (s + 1)**2*(1 + s/4e3)*(1 + s/50e3)*(1 + s/1e6)
    loopGain        = loopGainNumer/loopGainDenom
    r = findServoBandwidth(loopGain)
    print(r)

def test_instruction():
    i = instruction()
    i.circuit = circuit()
    i.gainType = 'loopgain'
    i.dataType = 'zeros'
    i.simType = 'numeric'
    i.detector = 'V_11'
    i.source = 'V1'
    i.lgRef = 'G1'
    i.step = True
    i.stepMethod = 'lin'
    i.stepNum = '5a'
    i.execute()

def test_math():
    s = ini.Laplace

    MNA = matrix([[5.0e-12*s + 0.01, 0, 0, -5.0e-12*s - 0.01, 0, 0, 0, 0, 1],
                  [0, 1.98e-11*s + 0.0001, -1.2e-11*s, -1.8e-12*s - 1.0e-5, 0, 0, 0, 0, 0],
                  [0, -1.2e-11*s, 2.8e-11*s + 0.001, 0, -1.0e-11*s - 0.001, 0, 0, -1, 0],
                  [-5.0e-12*s - 0.01, -1.8e-12*s - 1.0e-5, 0, 1.0068e-9*s + 0.01101, 0, 0, 1, 0, 0],
                  [0, 0, -1.0e-11*s - 0.001, 0, 1.0e-11*s + 0.001, 1, 0, 1, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0, -1.0e-6*s, -3.1623e-11*s, 0],
                  [0, 0, -1, 0, 1, 0, -3.1623e-11*s, -1.0e-9*s, 0],
                  [2.048e-20*s**3 + 2.688e-11*s**2 + 0.0016*s + 1, 0, 0, 0, 0, 0, 0, 0, 0]])

    DET = MNA.determinant()
    t1=time()
    roots1 = numRoots(DET,s)
    t2=time()
    print(roots1, t2-t1)
    MOD = MNA.Cramer([0,0,0,1,0,-1,0,0,0],3)
    DET = MOD.determinant()
    roots2 = numRoots(DET,s)
    print(roots2)
    a = phase_f(DET)
    print(sp.N(a.subs(ini.frequency, 100)))
    loopgain_numer   = sp.sympify('-s*(1 + s/20)*(1 + s/40)/2')
    loopgain_denom   = sp.sympify('(s + 1)^2*(1 + s/4e3)*(1 + s/50e3)*(1 + s/1e6)')
    loopgain         = loopgain_numer/loopgain_denom
    servo_info       = findServoBandwidth(loopgain)
    print(servo_info)

def test_python_maxima():
    print(maxILT(1, ini.Laplace**2 + sp.Symbol('a')**2, numeric = False))
    proto_transfer = sp.sympify('0.3*(1/(1+s*0.6))')
    circuit_transfer = sp.sympify('R_1/(R_1 + R_2)/(1 + s*R_1*R_2/(R_1 + R_2)*10e-6)')
    circuit_component_values = equateCoeffs(proto_transfer, circuit_transfer)
    print(circuit_component_values)
    proto_transfer = sp.sympify('A/(1+s*tau)')
    circuit_component_values = equateCoeffs(proto_transfer, circuit_transfer, noSolve=['A','tau'], numeric=False)
    print(circuit_component_values)
