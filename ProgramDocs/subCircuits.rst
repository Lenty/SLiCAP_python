============
Sub circuits
============

Sub circuits will be converted into a collection of elements that will be added to the ``.elements`` attribute (dictionary) of the parent circuit.

The parsing of the sub circuits will be illustrated below.

.. code::

    "My parent circuit"
    *
    * sub circuit =definition for 'myChildCircuit':
    X1 1 2 3 4 myCildCircuit av={10*A}
    .subckt myChildCircuit a b c d av=10 ci={C_i}
    E1 a b c d E value={av}
    R1 c 0     R value={R_i}
    C1 1 d     C value={C_i}
    .param R_i={1/2*pi*f*C_i*alpha} Ci=10p f={f_max}
    .ends
    *
    .end

The expasion of the circuit has the following equivalent netlist file:

.. code::

    "My parent circuit"
    *
    E1_X1 1    2   3   4   E value={10*A}
    R1_X1 c    0           R value={R_i_X1}
    C1_X1 1_X1 d           C value={C_i_X1}
    .param R_i_X1={1/2*pi*f*C_i_X1*alpha_X1} Ci={C_i} f={f_max_X1}
    *
    .end

Parsing of the nodes
====================

Node '0' is a global node. 

Nodes a, b, c, d of elements of the child circuit be be replaced with the corresponding nodes of the parent element (1,2,3,4, respectively). 

Other nodes of the elements of the child circuit are local nodes and obtain the suffix : ``'_' + < parentElement.refDes >``.

Parsing of the parameters
=========================

The values of the parameters 'av' and 'ci' are passed from the parent circuit element to the elements and the parameter definitions of the child circuit.

The parameter 'pi' in the child circuit is a global parameter. The global parameter 'f' in the child circuit is redefined as shown.

All other parameters are local and obtain the suffix: ``'_' + < parentElement.refDes >``.

The above is done as follows:

#. Create a substitution dictionary:

   .. code:: python
   
       substDict = {}

#. Both keys and values in this dict need to be sympy objects. The keys and values are obtained in the following order:

   #. The keys from the .params attribute (dictionary) of the parent element converted from ``str`` to ``sympy.Symbol``. Their values are the corresponding values from the .params dictionary.
   #. All parameters in expressions of all the elements that are not yet in this substitution dictionary and that are not gobal parameters. Their values are: sympy.Symbol(str(< parName >)+ '_' + < parentElement.refDes >).
   #. All the keys of the .parDefs attribute (dictionary) of the child circuit that are not yet in this substitution dictionary and that are not gobal parameters. Their values are: sympy.Symbol(str(< parName >)+ '_' + < parentElement.refDes >).
   #. All parameters in the expressions of .parDefs attribute (dictionary) of the child circuit that are not yet in this substitution dictionary and that are not gobal parameters. Their values are: sympy.Symbol(str(< parName >)+ '_' + < parentElement.refDes >).
