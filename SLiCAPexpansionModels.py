#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 10:06:02 2020

@author: anton
"""
from SLiCAPprotos import circuit, element
from sympy import sympify

EXPANSIONMODELS = {}

###############################################################################
# D: DIODE
###############################################################################
newCircuit = circuit()
newCircuit.title = 'D'
newCircuit.nodes = ['a', 'c']

newElement = element()
newElement.refDes = 'Rs'
newElement.model  = 'r'
newElement.nodes  = ['a', '1']
newElement.params['value']  = sympify('rs') # will be replaced with value of parameter rs

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gd'
newElement.model  = 'g'
newElement.nodes  = ['1', 'c', '1', 'c']
newElement.params['value']  = sympify('gs') # will be replaced with value of parameter gs

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cd'
newElement.model  = 'C'
newElement.nodes  = ['1', 'c',]
newElement.params['value']  = sympify('cd') # will be replaced with value of parameter cd

newCircuit.elements[newElement.refDes] = newElement

EXPANSIONMODELS['D'] = newCircuit

###############################################################################
# J: JFET
###############################################################################
newCircuit = circuit()
newCircuit.title = 'J'
newCircuit.nodes = ['d', 'g', 's']

newElement = element()
newElement.refDes = 'Gm'
newElement.model  = 'g'
newElement.nodes  = ['d', 's', 'g', 's']
newElement.params['value']  = sympify('gm') # will be replaced with value of parameter gm

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Go'
newElement.model  = 'g'
newElement.nodes  = ['d', 's', 'd', 's']
newElement.params['value']  = sympify('go') # will be replaced with value of parameter go

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cgs'
newElement.model  = 'C'
newElement.nodes  = ['g', 's',]
newElement.params['value']  = sympify('cgs') # will be replaced with value of parameter cgs

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cdg'
newElement.model  = 'C'
newElement.nodes  = ['d', 'g',]
newElement.params['value']  = sympify('cdg') # will be replaced with value of parameter cdg

newCircuit.elements[newElement.refDes] = newElement

EXPANSIONMODELS['J'] = newCircuit


###############################################################################
# M: MOSFET
###############################################################################
newCircuit = circuit()
newCircuit.title = 'M'
newCircuit.nodes = ['d', 'g', 's', 'b']

newElement = element()
newElement.refDes = 'Gm'
newElement.model  = 'g'
newElement.nodes  = ['d', 's', 'g', 's']
newElement.params['value']  = sympify('gm') # will be replaced with value of parameter gm

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gb'
newElement.model  = 'g'
newElement.nodes  = ['d', 's', 'b', 's']
newElement.params['value']  = sympify('gb') # will be replaced with value of parameter gb

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Go'
newElement.model  = 'g'
newElement.nodes  = ['d', 's', 'd', 's']
newElement.params['value']  = sympify('go') # will be replaced with value of parameter go

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cgs'
newElement.model  = 'C'
newElement.nodes  = ['g', 's',]
newElement.params['value']  = sympify('cgs') # will be replaced with value of parameter cgs

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cgb'
newElement.model  = 'C'
newElement.nodes  = ['g', 'b',]
newElement.params['value']  = sympify('cgb') # will be replaced with value of parameter cgb

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cdg'
newElement.model  = 'C'
newElement.nodes  = ['d', 'g',]
newElement.params['value']  = sympify('cdg') # will be replaced with value of parameter cdg

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cdb'
newElement.model  = 'C'
newElement.nodes  = ['d', 'b',]
newElement.params['value']  = sympify('cdb') # will be replaced with value of parameter cdb

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Csb'
newElement.model  = 'C'
newElement.nodes  = ['s', 'b',]
newElement.params['value']  = sympify('csb') # will be replaced with value of parameter csb

newCircuit.elements[newElement.refDes] = newElement

EXPANSIONMODELS['M'] = newCircuit

###############################################################################
# MD:  MOSFET differential pair
###############################################################################

newCircuit = circuit()
newCircuit.title = 'MD'
newCircuit.nodes = ['d1', 'd2', 'g1', 'g2']

newElement = element()
newElement.refDes = 'Gm'
newElement.model  = 'g'
newElement.nodes  = ['d1', 'd2', 'g1', 'g2']
newElement.params['value']  = sympify('gm') # will be replaced with value of parameter gm

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Go'
newElement.model  = 'g'
newElement.nodes  = ['d1', 'd2', 'd1', 'd2']
newElement.params['value']  = sympify('go') # will be replaced with value of parameter go

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cgg'
newElement.model  = 'C'
newElement.nodes  = ['g1', 'g2',]
newElement.params['value']  = sympify('cgg') # will be replaced with value of parameter cgs

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cdd'
newElement.model  = 'C'
newElement.nodes  = ['d1', 'd2',]
newElement.params['value']  = sympify('cdd') # will be replaced with value of parameter cgb

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cdg1'
newElement.model  = 'C'
newElement.nodes  = ['d1', 'g1',]
newElement.params['value']  = sympify('cdg') # will be replaced with value of parameter cdg

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cdg2'
newElement.model  = 'C'
newElement.nodes  = ['d2', 'g2',]
newElement.params['value']  = sympify('cdg') # will be replaced with value of parameter cdg

newCircuit.elements[newElement.refDes] = newElement

EXPANSIONMODELS['MD'] = newCircuit

###############################################################################
# OV: Voltage feedback operational amplifier
###############################################################################

newCircuit = circuit()
newCircuit.title = 'OV'
newCircuit.nodes = ['inP', 'inN', 'out', 'ref']

newElement = element()
newElement.refDes = 'E'
newElement.model  = 'EZ'
newElement.nodes  = ['out', 'ref', 'inP', 'inN']
newElement.params['av'] = sympify(0) # will be replaced with value of parameter Av
newElement.params['zo'] = sympify(0) # will be replaced with value of parameter zo

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gd'
newElement.model  = 'g'
newElement.nodes  = ['inP', 'inN', 'inP', 'inN']
newElement.params['value']  = sympify('gd') # will be replaced with value of parameter gd

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gc1'
newElement.model  = 'g'
newElement.nodes  = ['inP', 'ref', 'inP', 'ref']
newElement.params['value']  = sympify('gc/2') # will be replaced with value of parameter gc/2
newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gc2'
newElement.model  = 'g'
newElement.nodes  = ['inN', 'ref', 'inN', 'ref']
newElement.params['value']  = sympify('gc/2') # will be replaced with value of parameter gc/2

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cc1'
newElement.model  = 'C'
newElement.nodes  = ['inP', 'ref']
newElement.params['value']  = sympify('cc/2') # will be replaced with value of parameter cc/2
newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cc2'
newElement.model  = 'C'
newElement.nodes  = ['inN', 'ref']
newElement.params['value']  = sympify('Cc/2') # will be replaced with value of parameter cc/2

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cd'
newElement.model  = 'C'
newElement.nodes  = ['inP', 'inN',]
newElement.params['value']  = sympify('cd') # will be replaced with value of parameter cd

newCircuit.elements[newElement.refDes] = newElement

EXPANSIONMODELS['OV'] = newCircuit

###############################################################################
# OC: Current feedback operational amplifier
###############################################################################

newCircuit = circuit()
newCircuit.title = 'OC'
newCircuit.nodes = ['inP', 'inN', 'out', 'ref']

newElement = element()
newElement.refDes = 'H'
newElement.model  = 'HZ'
newElement.nodes  = ['out', 'ref', '1', 'ref']
newElement.params['zt'] = sympify(0) # will be replaced with value of parameter zt
newElement.params['zo'] = sympify(0) # will be replaced with value of parameter zo

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gm'
newElement.model  = 'g'
newElement.nodes  = ['inP', 'inN', '1', 'inN']
newElement.params['value']  = sympify('gm') # will be replaced with value of parameter gm

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gpn'
newElement.model  = 'g'
newElement.nodes  = ['inP', 'inN', 'inP', 'inN']
newElement.params['value']  = sympify('gpn') # will be replaced with value of parameter gpn
newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gp'
newElement.model  = 'g'
newElement.nodes  = ['inP', 'ref', 'inP', 'ref']
newElement.params['value']  = sympify('gp') # will be replaced with value of parameter gp

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cpn'
newElement.model  = 'C'
newElement.nodes  = ['inP', 'inN']
newElement.params['value']  = sympify('cpn') # will be replaced with value of parameter cpn
newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cp'
newElement.model  = 'C'
newElement.nodes  = ['inP', 'ref']
newElement.params['value']  = sympify('Cp') # will be replaced with value of parameter cp

newCircuit.elements[newElement.refDes] = newElement

EXPANSIONMODELS['OV'] = newCircuit

###############################################################################
# QV: Vertical BJT
###############################################################################

newCircuit = circuit()
newCircuit.title = 'QV'
newCircuit.nodes = ['c', 'b', 'e', 's']

newElement = element()
newElement.refDes = 'Gm'
newElement.model  = 'g'
newElement.nodes  = ['c', 'e', '1', 'e']
newElement.params['value']  = sympify('gm') # will be replaced with value of parameter gm

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gpi'
newElement.model  = 'g'
newElement.nodes  = ['1', 'e', '1', 'e']
newElement.params['value']  = sympify('gpi') # will be replaced with value of parameter gpi

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Go'
newElement.model  = 'g'
newElement.nodes  = ['c', 'e', 'c', 'e']
newElement.params['value']  = sympify('go') # will be replaced with value of parameter go

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gbc'
newElement.model  = 'gbc'
newElement.nodes  = ['c', '1', 'c', '1']
newElement.params['value']  = sympify('gbc') # will be replaced with value of parameter gbc

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Rb'
newElement.model  = 'r'
newElement.nodes  = ['b', '1']
newElement.params['value']  = sympify('rb') # will be replaced with value of parameter rb

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cpi'
newElement.model  = 'C'
newElement.nodes  = ['1', 'e',]
newElement.params['value']  = sympify('cpi') # will be replaced with value of parameter cpi

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cbc'
newElement.model  = 'C'
newElement.nodes  = ['1', 'c',]
newElement.params['value']  = sympify('cbc') # will be replaced with value of parameter cbc

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cbx'
newElement.model  = 'C'
newElement.nodes  = ['b', 'c',]
newElement.params['value']  = sympify('cbx') # will be replaced with value of parameter cbx

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cs'
newElement.model  = 'C'
newElement.nodes  = ['c', 's',]
newElement.params['value']  = sympify('cs') # will be replaced with value of parameter cdb

newCircuit.elements[newElement.refDes] = newElement

EXPANSIONMODELS['QV'] = newCircuit

###############################################################################
# QL: Lateral BJT
###############################################################################

newCircuit = circuit()
newCircuit.title = 'QL'
newCircuit.nodes = ['c', 'b', 'e', 's']

newElement = element()
newElement.refDes = 'Gm'
newElement.model  = 'g'
newElement.nodes  = ['c', 'e', '1', 'e']
newElement.params['value']  = sympify('gm') # will be replaced with value of parameter gm

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gpi'
newElement.model  = 'g'
newElement.nodes  = ['1', 'e', '1', 'e']
newElement.params['value']  = sympify('gpi') # will be replaced with value of parameter gpi

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Go'
newElement.model  = 'g'
newElement.nodes  = ['c', 'e', 'c', 'e']
newElement.params['value']  = sympify('go') # will be replaced with value of parameter go

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gbc'
newElement.model  = 'gbc'
newElement.nodes  = ['c', '1', 'c', '1']
newElement.params['value']  = sympify('gbc') # will be replaced with value of parameter gbc

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Rb'
newElement.model  = 'r'
newElement.nodes  = ['b', '1']
newElement.params['value']  = sympify('rb') # will be replaced with value of parameter rb

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cpi'
newElement.model  = 'C'
newElement.nodes  = ['1', 'e',]
newElement.params['value']  = sympify('cpi') # will be replaced with value of parameter cpi

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cbc'
newElement.model  = 'C'
newElement.nodes  = ['1', 'c',]
newElement.params['value']  = sympify('cbc') # will be replaced with value of parameter cbc

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cbx'
newElement.model  = 'C'
newElement.nodes  = ['b', 'c',]
newElement.params['value']  = sympify('cbx') # will be replaced with value of parameter cbx

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cs'
newElement.model  = 'C'
newElement.nodes  = ['b', 's',]
newElement.params['value']  = sympify('cs') # will be replaced with value of parameter cdb

newCircuit.elements[newElement.refDes] = newElement

EXPANSIONMODELS['QL'] = newCircuit

###############################################################################
# QD: Vertical BJT differential pair
###############################################################################

newCircuit = circuit()
newCircuit.title = 'QV'
newCircuit.nodes = ['c1', 'c2', 'b1', 'b2']

newElement = element()
newElement.refDes = 'Gm'
newElement.model  = 'g'
newElement.nodes  = ['c1', 'c2', '1', '2']
newElement.params['value']  = sympify('gm') # will be replaced with value of parameter gm

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gbb'
newElement.model  = 'g'
newElement.nodes  = ['1', '2', '1', '2']
newElement.params['value']  = sympify('gbb') # will be replaced with value of parameter gpi

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gcc'
newElement.model  = 'g'
newElement.nodes  = ['c1', 'c2', 'c1', 'c2']
newElement.params['value']  = sympify('gcc') # will be replaced with value of parameter go

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gbc1'
newElement.model  = 'gbc'
newElement.nodes  = ['c1', '1', 'c1', '1']
newElement.params['value']  = sympify('gbc') # will be replaced with value of parameter gbc

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Gbc2'
newElement.model  = 'gbc'
newElement.nodes  = ['c2', '2', 'c2', '2']
newElement.params['value']  = sympify('gbc') # will be replaced with value of parameter gbc

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Rb1'
newElement.model  = 'r'
newElement.nodes  = ['b1', '1']
newElement.params['value']  = sympify('rb') # will be replaced with value of parameter rb

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Rb2'
newElement.model  = 'r'
newElement.nodes  = ['b2', '2']
newElement.params['value']  = sympify('rb') # will be replaced with value of parameter rb

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cbb'
newElement.model  = 'C'
newElement.nodes  = ['1', '2',]
newElement.params['value']  = sympify('cbb') # will be replaced with value of parameter cpi

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cbc1'
newElement.model  = 'C'
newElement.nodes  = ['1', 'c1',]
newElement.params['value']  = sympify('cbc') # will be replaced with value of parameter cbc

newElement = element()
newElement.refDes = 'Cbc2'
newElement.model  = 'C'
newElement.nodes  = ['2', 'c2',]
newElement.params['value']  = sympify('cbc') # will be replaced with value of parameter cbc

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cbx1'
newElement.model  = 'C'
newElement.nodes  = ['b1', 'c1',]
newElement.params['value']  = sympify('cbx') # will be replaced with value of parameter cbx

newCircuit.elements[newElement.refDes] = newElement

newElement = element()
newElement.refDes = 'Cbx2'
newElement.model  = 'C'
newElement.nodes  = ['b2', 'c2',]
newElement.params['value']  = sympify('cbx') # will be replaced with value of parameter cbx

newCircuit.elements[newElement.refDes] = newElement

EXPANSIONMODELS['QD'] = newCircuit

# Make all circuits in EXPANSIONMODELS sub circuits
for key in EXPANSIONMODELS.keys():
    EXPANSIONMODELS[key].subCircuit = True