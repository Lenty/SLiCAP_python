=======================
Python-Maxima interface
=======================

Maxima CAS will be used as symbolic math tool for:

#. Evaluation of the determinant of a matrix
#. Evaluation of the inverse Laplace Transform of a (factorized) Laplace rational.
   
   Factorization will be done in Sympy and the poles and zeros will be determined with numpy.

The Python-Maxima interface is defined in the file: ``SLiCAPpythonMaxima.py``:

.. literalinclude:: ../SLiCAPpythonMaxima.py
    :language: python
    :linenos: 
    :lines: 1-84
    :lineno-start: 1
