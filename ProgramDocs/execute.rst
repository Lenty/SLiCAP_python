=======
Execute
=======

Considerations
==============

SLiCAP is a symbolic simulator designed to set-up or generate design equations for electronic circuits.

Design equations write the design parameters of a circuit as a function of performance parameters, cost factors and/or operating conditions. Examples of circuit design parameters are:

#. The values of resistors, capacitors, inductors, etc.
#. The values of the geometry parameters of transistors, such as the width and the length of the channel and the number of 'fingers' for MOS devices, the emmitter area and the number of base contacts and collector contacts for bipolar transistors.
#. Budgets for error sources, such as:
   #. The mean value and the standard deviation of DC error sources
   #. The spectral densities of noise sources
#. The circuit topology (structure of the circuit)

Performance parameters 

The functions that need to be realized with the circuit be considered as a high-level performance parameter. It can be regarded as the driving parameter for the structure of the topology of the circuit. The resolution of an arbitrary function into elementary basic functions



They can be obtained from circuit analysis if:

#. Device models are kept as simple as possible, modeling only the 



The file ``SLiCAPexecute.py`` contains the scripts for execution of an instruction.

Execution ``instruction.execute()`` proceeds as follows:

#. The instruction will be checked, execution will onnly proceed if no errors are found. Checking of the instruction is done by the method ``instruction.check()``  of the instruction object.
#. If no errors are found, ``instruction.execute()`` calls ``doInstruction()``, which performs the actual execution of the instruction.

Execute without stepping
========================

#. Build the matrices: makeGainType()
#. Do the instruction

Stepping of parameters
======================

*not yet implemented*

Single-parameter stepping
-------------------------

(step methods: 'lin', 'log' and 'list') proceeds as follows:

#. The matrices will be build with the step variable as symbolic parameter: makeGainType()
#. The numerator and/or denominator will be calculated
#. For each step, the step parameter value will be substituted.
#. For data types: 'poles', 'zeros', and 'pz' the solutions will then be calculated for each function.
#. For data types: 'impulse', 'step' and 'time', first the poles and the zeros will be determinated and then the time-domain responses will be calculated using the Inverse Laplace Transform.

Multi-parameter stepping
-------------------------

(step method: 'array') proceeds as follows:

#. For each set of step values, the matrix will be build and the complete analysis will be done.

.. literalinclude:: ../SLiCAPexecute.py
    :language: python
    :linenos:
