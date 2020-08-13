====================
Work with parameters
====================

'circuit parameters' are symbolic variables found in expressions in the netlist. They can be assigned a value using the SPICE '.PARAM' directive in the netlist. These values may again be given in the form of expressions with symbolic variables. When SLiCAP is working in numeric simulation mode, parameter values will recursively be substituted in expressions. 

--------------------------
Get all circuit parameters
--------------------------

A symbolic list of all circuit parameters can be obtained with the function ``params.m``: In the following example we assing the list with parameter definitions to the variable ``allParams``:

.. code-block:: matlab

		allParams = params();

-----------------------------
Get all parameter definitions
-----------------------------

A symbolic list with all circuit parameters that have been assigned a value can be obtained with the function ``parDefs.m``. In the following example we assign this list to the variable ``allParamsAssigned``:

.. code-block:: matlab

		allParamsDefined = parDefs();

----------------------------------
Assign a definition to a parameter
----------------------------------

A parameter can be given a value with the function ``defPar.m``. Below three diferent ways in which way the MATLAB® variable ``R_pi`` will obtain the value of the circuit parameter ``R_pi``, while the latter will be assigned a new value in the same statement.

.. code-block:: matlab

		R_pi = defPar('R_pi','2.5k');
		R_pi = defPar('R_pi', 2500);
		R_pi = defPar('R_pi', 'beta_DC/I_c/40');

------------------------------------------
Get the definition or value of a parameter
------------------------------------------

The function ``getParValue.m`` returns the value of a parameter. If the simulation type (simType) has been set to 'symbolic' it returnsthe symbolic definition of the parameter. If the simulation type has been set to 'numeric' it returns its value after recursive substitution of all parameter definitions:

.. code-block:: matlab

        defPar('r_pi', 'beta_DC/I_c/40');
        defPar('beta_DC', 100);
        defPar('I_c', '1m');
        getParValue('r_pi');

This returns 2500. If the parameter does not have a numeric value, the function returns the definition of the parameter with as many numeric subsitutions as possible.

-----------------------------------------
Assign definitions to multiple parameters
-----------------------------------------

Multiple parameter definitions can be passed with the function ``defPars.m``. The instruction below assigns 100 to the parameter ``R_f`` and 10e-12 to the parameter ``C_ell``. The return value is similar as that of the ``parDefs()`` instruction, it will be assigned to ``allParams``:

.. code-block:: matlab
 
        syms('R_f', 'C_ell');
		allParams = defPars([R_f == 500, C_ell == 10E-12]);

Please notice that the use of metric prefixes, such as, k for kilo and M for mega, is not allowed in the argument of the defPars() function. The function arguments should be symbolic equations and cannot contain character strings.

-----------------------------
Delete a parameter definition
-----------------------------

You can delete a parameter definition using the function ``delPar.m``. This function does not delete the circuit parameter itself. It only clears its definition so that it can be used as a symbolic variable in numeric simulations.

.. code-block:: matlab

		delPar('r_pi');
