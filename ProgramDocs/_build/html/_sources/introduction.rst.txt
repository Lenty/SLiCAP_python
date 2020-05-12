==================
SLiCAP open-source
==================

------------
Introduction
------------

#. Why open source

   Matlab is not free of costs, slow and not as easy to maintain as open-source versions.

----------
Technology
----------

#. Python

   - sympy
   - numpy
   - matplotlib or pyqtgraph (faster)
   - Cypy (faster than sympy)
   - Jupyter notebooks
   - ipython

#. Maxima CAS

   - fast symbolic math (LISP based)

#. HTML + CSS

#. LaTeX + MathJax

-------------
Functionality
-------------

As the current MATLAB version of SLiCAP but with improvements:

#. Labels for equations, figures and headings
#. Units for expressions and equations
#. Free to write to any HTML page
#. saveTeX(): write equation or expression in LaTeX format to a file
#. saveMathML(): write equation or expression in mathML format to a file
#. Change device values from the script (defVal(< deviceName >))
#. Import java scripts for live updates of variables and/or plots in html pages
#. Compile the SLiCAP library, this speeds up circuit checking. Models are compiled into a dictionary with SLiCAP model objects and sub circuits into a dictionary with SLiCAP circuit objects. When SLiCAP is started, automatic recompilation will be done if the library is newer than the precompiled version.
#. Select and generate circuit objects for instruction
#. Live scripts with jupyter or ipython

OR?? Make the instructions more Python like ...

.. code::

   instr = instruction()
   instr.circuit = myCircuit
   instr.source  = 'V1'
   # etc.

-----------------------------------------
Community for development and maintenance
-----------------------------------------

#. See: `TUDAT <http://tudat.tudelft.nl/index.html>`_
#. Documentation: 
   - Sphinx read-the-docs style
   - Wiki
