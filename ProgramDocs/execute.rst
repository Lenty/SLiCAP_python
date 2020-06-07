=======
Execute
=======

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
