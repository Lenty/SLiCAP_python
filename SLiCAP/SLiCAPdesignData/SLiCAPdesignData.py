#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 13:24:17 2022

@author: anton
"""
from SLiCAP.SLiCAPinstruction import *

class specItem(object):

    def __init__(self, symbol, description='', minValue='', typValue='', maxValue='', units='', specType=''):
        self.symbol      = symbol
        self.description = description
        self.minValue    = minValue
        self.typValue    = typValue
        self.maxValue    = maxValue
        self.units       = units
        self.spectype    = specType
        self.update()
        
    def update(self):
        self.specType    = str(self.spectype).lower()
        self.symbol      = sp.Symbol(str(self.symbol))
        if self.minValue != '':
            self.minValue = checkExpression(self.minValue)
        if self.typValue != '':
            self.typValue = checkExpression(self.typValue)
        if self.maxValue != '':
            self.maxValue = checkExpression(self.maxValue,)
        if self.units != '':
            self.units = sp.sympify(str(self.units)) # TODO a SLiCAP function: checkUnits!
        
    def csvLine(self):
        # symbol
        csv      = str(self.symbol) + ','
        # description
        csv      += self.description + ','
        # minValue
        if self.minValue != None:
            csv  += str(self.minValue) + ','
        else:
            csv  += ','
        # typValue    
        if self.typValue != None:
            csv  += str(self.typValue) + ','
        else:
            csv  += ','
        # maxValue    
        if self.maxValue != None:
            csv  += str(self.maxValue) + ','
        else:
            csv  += ','
        # units
        if self.units != None:
            csv  += str(self.units) + ','
        else:
            csv  += ','
        # spectype
        csv      += self.specType + '\n'
        return csv
            
    def htmlLine(self):
        # symbol
        html     = '<td class="left">$' + sp.latex(self.symbol) + '$</td>'
        # description
        html     += '<td class="left">' + self.description + '</td>'
        # minValue
        if type(self.minValue) == str:
            html += '<td></td>'
        else:
            html += '<td class="left">$' + sp.latex(roundN(self.minValue)) + '$</td>' # minValue
        # typValue    
        if type(self.typValue) == str:
            html += '<td></td>'
        else:
            html += '<td class="left">$' + sp.latex(roundN(self.typValue)) + '$</td>' # typValue
        # maxValue    
        if type(self.maxValue) == str:
            html += '<td></td>'
        else:
            html += '<td class="left">$' + sp.latex(roundN(self.maxValue)) + '$</td>' # maxValue
        # units
        if type(self.units) == str:
            html += '<td></td></tr>\n'
        else:
            html += '<td class="left">$\\mathrm{' + sp.latex(self.units) + '}$</td></tr>\n'       # Units
        return html
    
    def rstLine(self):
        # symbol
        rst     = ':math:`' + sp.latex(self.symbol) + '`,'
        # description
        rst     += self.description + ','
        # minValue
        if type(self.minValue) == str:
            rst += ','
        else:
            rst += ':math:`' + sp.latex(roundN(self.minValue)) + '`,' # minValue
        # typValue    
        if type(self.typValue) == str:
            rst += ','
        else:
            rst += ':math:`' + sp.latex(roundN(self.typValue)) + '`,' # typValue
        # maxValue    
        if type(self.maxValue) == str:
            rst += ','
        else:
            rst += ':math:`' + sp.latex(roundN(self.maxValue)) + '`,' # maxValue
        # units
        if type(self.units) == str:
            rst += '\n'
        else:
            rst += ':amth:`\\mathrm{' + sp.latex(self.units) + '}`\n'  # Units
        return rst        

def specList2dict(specList):
    specDict = {}
    # Assign ID and update the spec
    for i in range(len(specList)):
        item = specList[i]
        if str(item.symbol) in list(specDict.keys()):
            print("Warning: symbol %s already used, its definition will be overwritten!"%(str(item.symbol)))
        item.update()
        specDict[str(item.symbol)] = item
    return specDict

def specs2csv(dictwithspecs, fileName):
    f = open(ini.csvPath + fileName, 'w')
    f.write("symbol, description, min, typ, max, units, type\n")
    for spec in list(dictwithspecs.keys()):
        item = dictwithspecs[spec]
        f.write(item.csvLine())
    f.close()
    
def csv2specs(specList, csvFile):
    f = open(ini.csvPath + csvFile)
    lines = f.readlines()
    f.close()
    for i in range(1, len(lines)):
        args = lines[i].strip().split(',')
        newSpecItem = specItem(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
        specList.append(newSpecItem)
    return specList
        
def specs2html(dictWithSpecs, types=False):
    keys = sorted(list(dictWithSpecs.keys()))
    html = {}
    for key in keys:
        if dictWithSpecs[key].specType not in list(html.keys()):
            html[dictWithSpecs[key].specType] =  '<h3>' + dictWithSpecs[key].specType + ' specification</h3>\n'
            html[dictWithSpecs[key].specType] += '<table><a id="table_' + dictWithSpecs[key].specType + '"></a><caption>Table ' + dictWithSpecs[key].specType + ' specification </caption>'
            html[dictWithSpecs[key].specType] += '<tr><th class="left">symbol</th><th class="left">description</th><th class="left">min</th><th class="left">typ</th><th class="left">max</th><th class="left">units</th></tr>\n'
            html[dictWithSpecs[key].specType] += dictWithSpecs[key].htmlLine()
        else:
            html[dictWithSpecs[key].specType] += dictWithSpecs[key].htmlLine()
    txt = ''
    if types:
        for spectype in types:
            try:
                txt += html[spectype] + '</table>\n'
            except BaseException:
                pass
    else:
        for key in list(html.keys()):
            txt += html[key] + '</table>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, txt)
    if ini.notebook:
        txt = txt.replace('$', '$$')
    return txt

def specs2rst(dictWithSpecs, types=False):
    keys = sorted(list(dictWithSpecs.keys()))
    html = {}
    for key in keys:
        if dictWithSpecs[key].specType not in list(html.keys()):
            html[dictWithSpecs[key].specType] =  '<h3>' + dictWithSpecs[key].specType + ' specification</h3>\n'
            html[dictWithSpecs[key].specType] += '<table><a id="table_' + dictWithSpecs[key].specType + '"></a><caption>Table ' + dictWithSpecs[key].specType + ' specification </caption>'
            html[dictWithSpecs[key].specType] += '<tr><th class="left">symbol</th><th class="left">description</th><th class="left">min</th><th class="left">typ</th><th class="left">max</th><th class="left">units</th></tr>\n'
            html[dictWithSpecs[key].specType] += dictWithSpecs[key].htmlLine()
        else:
            html[dictWithSpecs[key].specType] += dictWithSpecs[key].htmlLine()
    txt = ''
    if types:
        for spectype in types:
            try:
                txt += html[spectype] + '</table>\n'
            except BaseException:
                pass
    else:
        for key in list(html.keys()):
            txt += html[key] + '</table>\n'
    insertHTML(ini.htmlPath + ini.htmlPage, txt)
    if ini.notebook:
        txt = txt.replace('$', '$$')
    return txt

def htmlParValue(instr, parName):
    return '$' + str(sp.latex(roundN(instr.getParValue(parName)))) + '$'

def htmlElValue(instr, parName):
    elValue = checkExpression(str(instr.getElementValue(parName)).replace('{', '').replace('}', ''))
    if instr.numeric:
        elValue = fullSubs(elValue, instr.parDefs)
    return '$' + str(sp.latex(roundN(elValue))) + '$'

def specs2circuit(specList, instr):
    for item in specList:
        if item.minValue != '':
            value = item.minValue
        elif item.typValue != '':
            value = item.typValue
        elif item.maxValue != '':
            value = item.maxValue
        if value != '':
            instr.defPar(item.symbol, value)