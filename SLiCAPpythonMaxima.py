#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 13:57:02 2020

@author: anton
"""

import subprocess
import re

def sympy2maximaMatrix(M):
    """Converts a sympy two-dimensional matrix with REAL coefficients into a Maxima matrix."""
    return(str(M).replace('Matrix([','matrix(').replace(']])','])').replace('**', '^'))
    
def maxEval(maxExpr):
    """Evaluates maxExpr in Maxima format with Maxima CAS and returns an
    expression in plain text format.
    
    expr: expression in Maxima format to be evaluated.
    
    The variable that needs to be output must be named: 'result'."""
    
    # LISP command for a  a single-line output in text format:
    maxStringConv = ":lisp (mfuncall '$string $result);"
    maxInput = maxExpr + maxStringConv
    output = subprocess.Popen(['maxima', '--very-quiet', '-batch-string', maxInput],stdout=subprocess.PIPE).stdout
    # The last line of the output stream is the result                              
    result = output.readlines()[-1]
    output.close()
    # Convert big float notation '12345b+123' to float notation '12345e+123':
    result = re.sub(r'(([+-]?)(\d+)(\.?)(\d*))b(([+-]?)(\d+))', r'\1e\6', result)
    # Convert complex number notation:
    result = re.sub(r'%j','j', result)
    # Convert 'e' (natural base) notation:
    result = re.sub(r'%e','e', result)
    # ToDo
    # Other conversions
    return(result)