=====================
Define an instruction
=====================

All the aspects of an instruction can at any time be changed from the MATLAB® environment. An instruction can be executed if the instruction data is complete and consistent (this will be checked by SLiCAP).

In the following sections the instruction data and their default values will be discussed.

---------------	  
Simulation type
---------------

SLiCAP uses symbolic calculation methods, even if the data is numerical. If the simulation type has been set to NUMERIC, parameter values are recursively substituted into the expressions for the circuit elements.

The default simultion mode is 'NUMERIC'. The simulation type can be set with the function ``simType.m``. This function returns the setting for the simulation type.

.. code-block:: matlab

	currentSimType = simType('?');   % Assigns the current simulation type setting to the MATLAB® variable 'currentSimType'
	newSimType = simType('numeric'); % Sets the simulation type to 'numeric' and assigns the simulation type to the MATLAB variable 'newSimType'
	simType('symbolic');             % Sets the simulation mode to 'symbolic'

---------
Gain type
---------

SLiCAP can provide expressions for:

	1. Nodal voltages or currents through elements that have been defined in current-controlled notation (the volhage has been defined as a function of the current)

	2. Transfer functions of the asymptotic-gain model:
	
		a) gain
		
			This is the transfer from the source to the detector
				
		b) asymptotic-gain 
		
			This is the transfer for infinite loop gain
				
		c) loop gain
		
			This is the transfer of the controlled source selected by the loop gain reference variable, multiplied with the transfer from the output quantity of this variable to its input quantity.
				
		d) direct transfer
		
			This is the transfer from source to the detector with the gain of the loop gain reference variable set to zero
				  
		e) servo function
		
			This is :math:`\frac{-L}{1-L}` in which :math:`L` is the loop gain according to the definition above.

The gain type can be defined with the function: ``gaintype.m``.

.. code-block:: matlab

	currentGainType = gainType('?') % Assigns the current setting of the gain type to the MATLAB® variable 'currentGainType'
	gainType('asymptotic');         % Calculates asymptotic-gain according to the asymptotig-gain model requires source, detector and loop gain reference
	gainType('direct');             % Calculates direct transfer according to the asymptotig-gain model requires source, detector and loop gain reference
	gainType('gain');               % Calculates the source to detector transfer requires, source and detector
	gainType('loopgain');           % Calculates the loop gain according to the asymptotig-gain model requires a loop gain reference
	gainType('servo');              % Calculates servo function according to the asymptotig-gain model requires loop gain reference
	gainType('vi');                 % Calculates voltage or current; default gain type
                                    % requires detector, except for data types 'matrix', 'solve' and 'DCsolve'

-------------
Signal source
-------------

Any independent current source or independent voltage source in the circuit can be selected as signal source. A source can be defined with the function: ``source.m``.  The argument of the function should be the name (identifier) of an inpependent source in the circuit. A list of available independent sources in the circuit can be obtained with the function: ``indepVars.m``. 

.. code-block:: matlab

    availableSources = indepVars(); % Assigns a symbolic list with independent variables to the MATLAB® variable 'availableSources'
    source('Vs');                   % Defines the voltage source 'Vs' as signal source
    source('I3');                   % Defines the current source 'I3' as signal source

--------
Detector 
--------
	  
In order to limit the execution time, SLiCAP calculates only one current, voltage or differential voltage or one transfer function. This variable is defined by the detector: ``detector.m``. The name of this function should be composed as follows:

- In the case of a voltage detector, the name should be the concatenation of 'V\_' and the name of the output node; in general: 'V_<outputNode>'. For the voltage difference between two nodes, simply use two arguments (see example below)

- In the case of a current detector, the name should be the concatenation of 'I\_' and the name of the element (identifier) whose current is taken as detector current.

Any dependent circuit variable can be selected as detector quantity. A symbolic list with available dependent variables can be obtained with the function ``depVars.m``.

.. code-block:: matlab

	availableDets = depVars();      % Assigns a symbolic list with available dependent variables to the MATLAB® variable 'availableDets'
	currentDet = detector('?');     % Assigns the name of the current detector to the MATLAB® variable 'currentDet'
	detector('V_out');              % Defines the voltage detector at node 'out'
	detector('V_pos', 'V_neg');     % Defines a differential voltage detector between node 'pos' en node 'neg'
	detector('I_Vs');               % Defines a current detector that measures the current through 'Vs'

-------------------
Loop gain reference
-------------------

The asymptotic-gain negative-feedback model uses one controlled source of the circuit as so-called loop gain reference variable. A list with controlled sources that are available for this purpose can be obtained with the fuction ``controlled.m``. 

One of the controlled sources of this list can be assigned as loop gain reference variable. This can be done with the function ``lgRef.m``. 

.. code-block:: matlab

	availableRefs = controlled();   % Assigns a symbolic list with available controlled sources to the MATLAB® variable 'availableRefs'
	currentRef = lgRef('?');        % Assigns the name of the loop gain reference variable to the MATLAB® variable 'currentRef'
	lgRef('gm_M1');                 % Defines the controlled source with name 'gm_M1'  as loop gain reference variable

---------
Data type
---------

SLiCAP can provide many types of data. The data type can be defined with the function: ``dataType.m``. Below the syntax for setting the data type and the meaning of the different data types.

.. code-block:: matlab

	dataType('dc')          % Calculates DC value of the detector voltage or the detector current; only for gain type 'vi'
	dataType('dcsolve')     % Calculates DC solution of the network; only for gain type 'vi'
	dataType('dcvar')       % Calculates source-referred and detector-referred variance due to variances of all voltage and current sources; only for gain type 'vi'
	dataType('denom')       % Calculates denominator of laplace transform of gain type; default data type
	dataType('impulse')     % Calculates inverse laplace transform of gain type not for gain type 'vi'; may not work with symbolic values
	dataType('laplace')     % Calculates laplace transform of gain type; default data type
	dataType('matrix')      % Calculates matrix equation of the circiut; default data type
	dataType('noise')       % Calculates source-referred and detector-referred noise contributions of all noise sources; only for gain type 'vi'
	dataType('numer')       % Calculates numerator of laplace transform of gain type; default data type
	dataType('poles')       % Calculates complex solutions of laplace transform of 'denom' not for gain type 'vi'; may not work with symbolic values
	dataType('pz')          % Calculates poles and zeros (with pole-zero canceling) and DC gain not for gain type 'vi'; may not work with symbolic values
	dataType('solve')       % Calculates the network solution; only for gain type 'vi'
	dataType('step')        % Calculates inverse laplace transform of (1/s) * gain type not for gain type 'vi'; may not work with symbolic values
	dataType('time')        % Calculates inverse laplace transform of detector voltage or current only for gain type 'vi'; may not work with symbolic values
	dataType('zeros')       % Calculates complex solutions of laplace transform of 'numer' not for gain type 'vi'; may not work with symbolic values
