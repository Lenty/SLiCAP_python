=========================
Building the MNA matrices
=========================

SLiCAP math library
===================

The SLiCAP math library contains a matrix class which is a sub class of the Sympy Matrix class. The execution time of the methods belonging to this class is shorter than comparable methods in Sympy, but still much slower than comparable methods in Maxima CAS.

.. literalinclude:: ../SLiCAPmath.py
    :language: python
    :linenos: 
    :lines: 1-140
    :lineno-start: 1

MNA matrices
============

The MNA matrices are built with matrix stamps of basic elements. The position of the stamp in the matrix follows from the postion of the dependent variables (nodal voltages and branch currents) of these elements. They are stored in the .depVars attribute of the circuit object.

Matrices can be built with symbolic or numeric. 

.. literalinclude:: ../SLiCAPmatrices.py
    :language: python
    :linenos: 
    :lines: 1-255
    :lineno-start: 1
