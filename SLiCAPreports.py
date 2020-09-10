#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class SLiCAPproject(object):
    def __init__(self, projectName, creationDate, author):
        # attributes stored in the project.ini file:
        self.name    = projectName
        self.created = creationDate
        self.author  = author
        # attributes generated each time running initSLiCAP:
        self.updated = datetime.now() # Last updated
        self.data    = {}             # Project data dictionary with key-object pairs
        self.report  = []             # List of keys (links to the project data dictionary)
        self.newKey = 0
        
    def write(self, dataObject):
        if dataObject.label != '':
            self.data[dataObject.label] = dataObject
            self.report.append(dataObject.label)
        else:
            key = str(self.newKey) + '_' + dataObject.type
            self.data[key] = dataObject
            self.report.append(key)
            self.newKey += 1

    def move(self, label, beforeLabel):
        """
        moves 'label' to the next position of 'afterLabel'
        """
        self.report.insert(self.report.index(beforeLabel), self.report.pop(self.report.index(label)))
        
    def makeRST(self):
        rst = ''
        for key in self.report:
            item = self.data[key]
            function = getattr(item, 'makeRST')
            rst += function()
        return rst
            
    def makeTeX(self):
        tex = ''
        for key in self.report:
            item = self.data[key]
            function = getattr(item, 'makeTeX')
            tex += function()
        return tex
                
class head1(object):
    def __init__(self, txt):
        self.type = 'h1'
        self.txt = txt
        self.label = ''
        
    def makeRST(self):
        RST = ''
        if self.label != '':
            RST = '\n.. _' + self.label
        line = '\n'
        for i in range(len(self.txt)):
            line += '='
        return(RST + line + '\n' + self.txt + line +'\n')
        
    def makeTeX(self):
        tex = '\n\\chapter{' + self.txt
        if self.label != '':
            tex += '\\label{' + self.label + '}}\n'
        else:
            tex += '}\n'
        return(tex)
        
class head2(object):
    def __init__(self, txt):
        self.type = 'h2'
        self.txt = txt
        self.label = ''
        
    def makeRST(self):
        RST = ''
        if self.label != '':
            RST = '\n.. _' + self.label
        line = '\n'
        for i in range(len(self.txt)):
            line += '='
        return(RST + '\n' + self.txt +line + '\n')
        
    def makeTeX(self):
        tex = '\n\\section{' + self.txt
        if self.label != '':
            tex += '\\label{' + self.label + '}}\n'
        else:
            tex += '}\n'
        return(tex)

class head3(object):
    def __init__(self, txt):
        self.type = 'h3'
        self.txt = txt
        self.label = ''
        
    def makeRST(self):
        RST = ''
        if self.label != '':
            RST = '\n.. _' + self.label
        line = '\n'
        for i in range(len(self.txt)):
            line += '-'
        return(RST + '\n' + self.txt +line + '\n')  
        
    def makeTeX(self):
        tex = '\\subsection{' + self.txt
        if self.label != '':
            tex += '\\label{' + self.label + '}}\n'
        else:
            tex += '}\n'
        return(tex) 
        
class head4(object):
    def __init__(self, txt):
        self.type = 'h4'
        self.txt = txt
        self.label = ''
        line = '\n'
        for i in range(len(self.txt)):
            line += '~'
        return('\n' + self.txt +line + '\n')  
        
    def makeRST(self):
        RST = ''
        if self.label != '':
            RST = '\n.. _' + self.label
        line = '\n'
        for i in range(len(self.txt)):
            line += '~'
        return(RST + '\n' + self.txt +line + '\n')  
        
    def makeTeX(self):
        tex = '\\subsubsection{' + self.txt
        if self.label != '':
            tex += '\\label{' + self.label + '}}\n'
        else:
            tex += '}\n'
        return(tex)

class TxT(object):
    def __init__(self, txt):
        self.txt = txt
        self.type = 'txt'
        self.label = ''
    
    def makeRST(self):
        if type(txt) == str:
            return '\n' + txt + '\n'
        else:
            RST = '\n'
            for item in self.txt:
                if type(item) == str:
                    RST += item
                elif isinstance(item, tuple(sp.core.all_classes)):
                    RST += ':math:`' + sp.latex(item) + '`'
            RST += '\n'
        return RST
    
    def makeTeX(self):
        if type(txt) == str:
            return '\n' + txt + '\n'
        else:
            tex = '\n'
            for item in self.txt:
                if type(item) == str:
                    tex += item
                elif isinstance(item, tuple(sp.core.all_classes)):
                    tex += '$' + sp.latex(item) + '$'
            tex += '\n'
        return tex

class eqn(object):
    def __init__(self, lhs, rhs, inline = False, units = ''):
        self.type = 'eqn'
        self.lhs = lhs          # Sympy object
        self.rhs = rhs          # Sympy object
        self.units = units      # str
        self.label = ''         # str
        self.inline = inline    # bool
    
    def makeRST(self):
        if self.inline == True:
            RST = ':math:`' + sp.latex(self.lhs) + '=' + sp.latex(sp.N(self.rhs, DISP))
            if self.units != '':
                RST += '\\,\\mathrm{\\left[' + sp.latex(sp.sympify(self.units)) + '\\right]}'
            RST += '`'
        else:
            RST = '\n.. math::\n'
            if self.label != '':
                RST += '    :' + self.label + ':\n'
            RST += '\n    ' + sp.latex(self.lhs) + '=' + sp.latex(sp.N(self.rhs, DISP))
            if self.units != '':
                RST += '\\,\\mathrm{\\left[' + sp.latex(sp.sympify(self.units)) + '\\right]}\n'
            else:
                RST += '\n'
        return RST
            
    def makeTeX(self):
        if self.inline == True:
            tex = '$' + sp.latex(self.lhs) + '=' + sp.latex(sp.N(self.rhs, DISP))
            if self.units != '':
                tex += '\\,\\mathrm{\\left[' + sp.latex(sp.sympify(self.units)) + '\\right]}'
            tex += '$' 
        else:
            tex = '\n\\begin{equation}\n' + sp.latex(self.lhs) + '=' + sp.latex(sp.N(self.rhs, DISP))
            if self.units != '':
                tex += '\\,\\mathrm{\\left[' + sp.latex(sp.sympify(self.units)) + '\\right]}'
            if self.label != '':
                tex += '\\label{' + self.label + '}'
            tex += '\n\\end{equation}\n'
        return tex

class fig(object):
    def __init__(self, fileName, width):
        self.type = 'fig'
        self.file = fileName # str
        self.width = width   # int units = pixels
        self.label = ''      # str
        self.caption = ''    # str
        
    def makeTeX(self):
        dim = str(self.width*1.0 / DPI)
        tex = '\n\\begin{figure}[H]\n\\centering\\includegraphics[width=' + dim + 'in]{' + self.file +'}\n'
        tex += '\\caption{' + self.caption + '}\n'
        if self.label != '':
            tex += '\\label{' + self.label + '}\n'
        tex += '\\end{figure}\n'
        return tex
    
    def makeRST(self):
        if self.label != '':
            RST = '\n.. _' + self.label + ':\n.. figure:: ' + self.file + '\n'
        else:
            RST = '\n.. figure:: ' + self.file + '\n'
        RST += '    :width: %spx\n'%self.width
        RST += '    :align: center\n'
        RST += '    :caption: ' + self.caption + '\n'
        return RST
        

class table(object):
    def __init__(self, csvData):
        self.type = 'table'
        self.csvData = csvData # nested list
        self.cols = ['l' for i in range(len(csv[0]))]
        self.widths = [100./len(csv[0]) for i in range(len(csv[0]))]
        self.label = ''
        self.caption = ''
    
class ref(object):
    def __init__(self, label):
        self.type  = 'ref'
        self.label = label
        self.item  = ''
        
class fref(object):
    def __init__(self, fName):
        self.type = 'file'
        self.name = fName
        self.label = ''
        self.caption = ''
        
if __name__ == '__main__':
    import sympy as sp
    from sympy.parsing.sympy_parser import parse_expr
    from datetime import datetime
    DISP = 4
    DPI = 150
    report = []
    p=SLiCAPproject('MyProject', 'nu', 'ik')
    
    chap = head1('First chapter')
    chap.label = 'ch1'
    p.write(chap)
    
    txt = TxT(['This is some opening blah blah with an expression: ', sp.sympify('e^(i*pi)'), '.'])
    txt.label = 'introText'
    p.write(txt)
    
    sec = head2('New section')
    sec.label = 'sec-euler'
    p.write(sec)
    
    eqn1 = eqn(sp.sympify('e^(i*pi)'), sp.sympify(-1), units = 'V^2/sqrt(Hz)')
    eqn1.label = 'euler'
    eqn1.inline = False
    p.write(eqn1)
    
    f = fig('myFig.svg', 800)
    f.label = 'fig-myFig'
    #f.caption = 'The latest figure.'
    p.write(f)
    
    #p.move('euler', 'introText')
    
    print p.report
    print p.makeTeX()
    print p.makeRST()