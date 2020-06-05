=========================
Building the MNA matrices
=========================

The MNA matrices are built with matrix stamps of basic elements. The position of the stamp in the matrix follows from the postion of the dependent variables (nodal voltages and branch currents) of these elements. They are stored in the .depVars attribute of the circuit object.

Matrices can be built with symbolic or numeric. 

.. literalinclude:: ../SLiCAPmatrices.py
    :language: python
    :linenos: 
    :lines: 1-299
    :lineno-start: 1
