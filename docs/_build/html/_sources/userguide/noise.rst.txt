============
Noise design
============

SLiCAP has a number of built-in scripts to support circuit designers with the analysis and design of the stationary noise behavior of electronic circuits. These functions can be used to process the result of the execution of an instruction with the data type set to *noise*. 

Please notice that some of these functions use symbolic integration which may fail if the frequency dependency of the spectra becomes too complex.

-----------------------
Define a noise analysis
-----------------------

.. code-block:: python

    >>> from SLiCAP import *
    >>> prj = initProject('noiseProject') 

---------
RMS noise
---------

The function **SLiCAPpythonMaxima.rmsNoise(*args)** can be used to calculate the total RMS noise over a frequency range. See `SLiCAPpythonMaxima.py <../reference/SLiCAPpythonMaxima.html>`_ for more information.
