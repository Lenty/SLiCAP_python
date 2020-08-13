=====================
Work with the results
=====================

SLiCAP has predefined functions for plotting, displaying tables and generation of web pages with beautifully typeset expressions, tables, figures and files. SLiCAP also has a lot of postprocessing functions available for finding budgets for various performance parameters of electronic components, based upon the target performance specification of the circuit. There are many examples available for the design of the high-frequency behavior and the noise behavior of amplifiers.
    
It will be clear that once you have the (symbolic) matrix equation of a circuit and:

- you have sufficient knowledge of Structured Analog Design

- you are familiar with MATLAB®, 

SLiCAP can help you with setting up and solving design equations for almost any design problem. Ultimately, it facilitates the automation of design engineering.

But there is more: while doing your design work with SLiCAP, you generate a collection of linked HTML pages that document your work. This helps you to discuss your work with colleagues or present it to students, on any platform that has a browser and a network connection.

On this page the currently implemented post processing functions will be discussed.

--------------------
List poles and zeros
--------------------

This function ``listPZ.m`` can be used to present the results of a pole-zero analysis (data type: ``'POLES'``, ``'ZEROS'``, ``'PZ'``) in table form. It lists the real part, the imaginary part, the magnitude and the quality factor of poles and zeros in [Hz]. The quality factor of a pole or zero is defined as the absolute value of the ratio of its imaginary part and its real part. If the data type is PZ, the zero-frequency value (DC value) of the gain is also evaluated and displayed.

In the following example we assume a loop gain reference variable has been defined.

.. code-block:: matlab

		gainType('loopgain');
		dataType('PZ')
		loopgainPZG = execute();
		listPZ(loopgainPZG);
