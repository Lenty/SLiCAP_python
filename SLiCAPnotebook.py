#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 23:28:32 2020

@author: anton
"""

from IPython.core.display import HTML, SVG
from IPython.core.magic import register_cell_magic, register_line_magic
from IPython.display import Image
from SLiCAP import *

# Work around for displaying rst in jupyter notebooks

@register_cell_magic
def rst(line, cell):
    """
    Render ReStructuredText:
        
        %%rst
        ============
         Main title
        ============
    """
    writer = docutils.writers.html5_polyglot.Writer()
    return HTML(docutils.core.publish_string(cell, writer=writer).decode('UTF-8'))

@register_line_magic
def rstfile(filename):
    """
    Render ReStructuredText file:
    
        %rstfile <file name>
    """
    writer = docutils.writers.html5_polyglot.Writer()
    with open(filename, 'r') as file:
        cell = file.read()
    return HTML(docutils.core.publish_string(cell, writer=writer).decode('UTF-8'))