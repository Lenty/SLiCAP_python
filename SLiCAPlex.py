#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
SLiCAPlex.py

Tokenizer for SLiCAP netlist files

Created on Mon May  4 12:32:13 2020

@author: anton
"""
from SLiCAPhtml import *

# list of token names

tokens = ('PARDEF', 'EXPR', 'SCI', 'SCALE', 'FLT', 'INT', 'CMD', 'FNAME', 
          'PARAMS', 'ID', 'QSTRING', 'PLUS', 'LEFTBR', 'RIGHTBR', 'COMMENT')

SCALEFACTORS    =  {'y':'-24','z':'-21','a':'-18','f':'-15','p':'-12','n':'-9',
                    'u':'-6','m':'-3','k':'3','M':'6','G':'9','T':'12','P':'15',
                    'E':'18','Z':'21','Y':'24'}

t_FLT     = r'[+-]?\d+\.\d*'
t_INT     = r'[+-]?\d+'
t_FNAME   = r'/?[^\s]+\.[a-zA-Z]+'
t_ID      = r'[a-zA-Z]\w*'
t_QSTRING = r'"(.*)"'
t_PLUS    = r'\+'



def t_PARDEF(t):
    r"""[a-zA-Z]\w*\s*\=\s*({[\w\(\)\/*+-\^ .]*}
    |([+-]?\d+\.?\d*[eE][+-]?\d+)
    |([+-]?\d+\.?\d*[yzafpnumkMGTPEZY])
    |([+-]?\d+\.\d*)
    |([+-]?\d+))"""
    t.value = t.value.replace(' ', '')
    t.value = t.value.split('=')
    # replace scale factors in t.value[1]
    t.value[1] = replaceScaleFactors(t.value[1])
    if t.value[1][0] == '{' and t.value[1][-1] == '}':
        # remove the curly brackets before turing it into a Sympy expression.
        t.value[1] = t.value[1][1:-1]
    try:
        t.value[1] = sp.sympify(t.value[1])
    except:
        printError("Error in expression.", lexer.lexdata.splitlines()[lexer.lineno], find_column(t))
        lexer.errCount += 1
    return t

def t_CMD(t):
    r'\.[a-zA-Z]+'
    """
    Caplitalize commands.
    """
    t.value = t.value[1:].upper()
    return t

def t_COMMENT(t):
    r'\*.*|(\;.*)'
    """
    Comment is ignored.
    """
    pass

def t_LEFTBR(t):
    r'\('
    """
    Start of model parameters can be ignored.
    """
    pass

def t_t_RIGHTBR(t):
    r'\)'
    """
    End of model parameters can be ignored.
    """
    pass

def t_PARAMS(t):
    r'((?i)(params:))'
    """
    Start of sub circuit parameters can be ignored
    """
    pass

def t_EXPR(t):
    r'{[\w\(\)\/*+-\^ .]*}'
    """
    Replaces scale factors in expressions and converts the expression into
    a sympy object.
    """
    t.value = replaceScaleFactors(t.value)
    try:
        t.value = sp.sympify(t.value[1:-1])
    except:
        lexer.errCount += 1
        printError("Error in expression:", lexer.lexdata.splitlines[lexer.lineno], find_column(t))
    return t          

def t_SCI(t):
    r'[+-]?\d+\.?\d*[eE][+-]?\d+'
    try:
        t.value = float(t.value)
        t.type = 'FLT'
    except:
        printError('Cannot convert number to float.', lexer.lexdata.splitlines[lexer.lineno], find_column(t))
    return t  
          
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def find_column(token):
    """
    Compute column of token
    """
    line_start = lexer.lexdata.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1
 
 # Error handling rule
def t_error(t):
    t.lexer.errCount += 1
    printError("Error: illegal character.", lexer.lexdata.splitlines()[lexer.lineno], find_column(t))
    t.lexer.skip(1)

# Define a rule for numbers with scale factors (postfixes)
def t_SCALE(t):
    r'[+-]?\d+\.?\d*[yzafpnumkMGTPEZY]'
    """
    Replaces scale factors in numbers and converts numbers into floats.
    """
    try:
        t.value = float(replaceScaleFactors(t.value))
        t.type = 'FLT'
    except:

        printError('Cannot convert number to float.', lexer.lexdata.splitlines[lexer.lineno], find_column(t))
        lexer.errCount += 1
    return t 

def replaceScaleFactors(txt):
    """
    Replaces scale factors in expressions with their value in scientific notation.
    """
    pos = 0
    out = ''
    for m in re.finditer(r'\d+\.?\d*([yzafpnumkMGTPEZY])', txt):
        out += txt[pos: m.end()-1] + 'E' + SCALEFACTORS[m.group(0)[-1]]
        pos = m.end()
    out += txt[pos:]
    return out  

def tokenize(cirFileName):
    """
    Reset the lexer, and create the tokens for the new data.
    """
    lexer.errCount = 0
    lexer.lineno = 0
    f = open(cirFileName, 'r')
    data = f.read()
    f.close()
    lexer.input(data)
    return lexer

def tokenizeTxt(textString):
    """
    Reset the lexer, and create the tokens for the new data.
    """
    lexer.errCount = 0
    lexer.lineno = 0
    lexer.input(textString)
    return lexer

def printError(msg, line, pos):
    """
    Print the line with the error, an error message and show the position
    of the error.
    """
    out = '\n' + line + '\n'
    for i in range(pos-1):
        out += '.'
    out += '|\n' + msg
    print out

# Initialize the lexer
lexer = lex.lex()
lexer.errCount = 0   
   
if __name__ == '__main__':
    """
    files = os.listdir('Project/cir')
    for fi in files:
        [cirFileName, ext] = fi.split('.')
        if ext.lower() == 'cir':"""
    fi = 'testCircuit.cir'
    print fi
    lexer = tokenize('Project/cir/' + fi)
    tok = lexer.token()
    
    while tok:
        print tok
        tok = lexer.token()
    
    print '\nnumber of errors =', lexer.errCount, '\n'