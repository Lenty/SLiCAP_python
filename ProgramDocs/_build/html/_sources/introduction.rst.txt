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

   - sympy: basic symbolic math operations, such as:

     - Converting a textstring that represents an expression into an expression
     - Substitutions
     - Building matrices
     - Construction of numerator and denominator Polys from Laplace expressions

   - numpy: fast numeric calculations

     - Determination of poles and zeros (roots of polynomials)

   - scipy: special functions

     - Numeric calculation of residues for construction of the Inverse Laplace Transform of Laplace (numeric) rationals.

   - matplotlib: plotting

#. Maxima CAS: fast symbolic math (LISP based)

   - Symbolic calculation of the determinant of a matrix using the fast Johnson-Gentleman tree minor algorithm.
   - Comined symbolic and numerical integration
   - Solving equations
   - Determination of the real and the imaginary part of an expression
   - Calculation of the Inverse Laplace Transform of symbolic Laplace expressions
   - Setting assumtions for variables

#. HTML + CSS: reporting

#. LaTeX + MathJax + MathML: reporting and export equationa

-------------
Functionality
-------------

As the current MATLAB version of SLiCAP but with improvements:

#. User options:

   - Use :math:`f` [Hz] or :math:`\omega` [rad/s] for frequency
   - Select stepping method: 

     - Substitute the step variables while building the matrices
     - Substitufe the step variables after calculation of the determinant and/or the cofactors

   - Display the output from Maxima before converting it to a Sympy expression.
   - Use MathML of MathJaX cloud rendering of math in HTML pages 
   - Set the number of digits for displaying numeric values on HTML pages

#. Labels for equations, figures and headings
#. Units for expressions and equations
#. Free to write to any HTML page or HTML index page
#. saveTeX(): write equation or expression in LaTeX format to a file
#. saveMathML(): write equation or expression in mathML format to a file
#. Import java scripts for live updates of variables and/or plots in html pages
#. Compilation of the SLiCAP libraries at the initialization of a project.
#. Select or generate circuit objects for an instruction
#. Python like instructions:

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
