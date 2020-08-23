==================
Parameter stepping
==================

SLiCAP can execute an instruction while stepping the value of one or more circuit parameters. 

Functions for parameters stepping will be discussed below

.. _parameterStepping:

----------------------
Define the step method
----------------------

SLiCAP has four methods for parameter stepping, three of them are intended for stepping of a single parameter:

- linear stepping: ``stepMethod('lin')``
- logarithmic stepping: ``stepMethod('log')``
- stepping through a list of values ``stepMethod('list')``

One method is intended for concurrently stepping of multiple parameters:

- array stepping: ``stepMethod('array')``

.. code-block:: matlab

    stepMethod('?')         % returns the current setting for the step method, this can be 'lin', 'log', list or array
    stepMethod('lin');      % sets the step method to linear stepping and returns 'lin'    
    stepMethod('log');      % sets the step method to logarithmic stepping and returns 'log'    
    stepMethod('list');     % sets the step method to list stepping and returns 'list' 
    stepMethod('array');    % sets the step method to array stepping and returns 'array' 
    
---------------------------
Define the step variable(s)
---------------------------

Linear, log and list stepping
-----------------------------

The step variable for linear logarithmic and list stepping can be selected from the available circuit parameters. A list of available circuit parameters can be obtained by evoking the ``params()`` function.

.. code-block:: matlab

    stepVar('?')            % returns the current value of the step parameter
    var = stepVar('C1');    % makes 'C1' step parameter and assigns 'C1' to 'var' if this parameter exists

Array stepping
--------------

As with single parameters stepping, the step variables can be selected from all available circuit parameters. The step variables need to be defined with an cell array:

.. code-block:: matlab

    stepVars('?')             % Returns a list with the current step parameters
    stepVars({'C_1' 'R_1'});  % Defines C_1 and R_1 as step parameters for array stepping
    stepVars({'C_1', 'R_1'}); % Similar as above

----------------------
Define the step values
----------------------

Linear and logarithmic stepping
-------------------------------

Linear and logarithmic stepping required the definition of the step variable, the start value, the stop value and the number of steps.

.. code-block:: matlab

    stepVar('?')            % returns the current value of the step parameter
    var = stepVar('C1');    % makes 'C1' step parameter and assigns 'C1' to 'var' if this parameter exists
    stepStart('?')          % returns the current start value of the step parameter
    start = stepStart(10);  % sets the start value of the step parameter to 10 and assigns this value to 'start'
    start = stepStart('1p');% sets the start value of the step parameter to 1e-12 and assigns this value to 'start'
    stepStop('?')           % returns the current stop value of the step parameter
    stop = stepStop(100);   % sets the stop value of the step parameter to 100 and assigns this value to 'stop'
    stop = stepStop('10p'); % sets the stop value of the step parameter to 10e-12 and assigns this value to 'stop'
    stepNum('?')            % returns the current setting for the number of steps of the step parameter
    num = stepNum(20);      % sets the number of steps to 20 and assigns this value to 'num'

With logarithmic stepping SLiCAP calculates the number of decades from the start and stop value and the datapoints from the number of decades and the number of steps. Logarithmically stepping through zero is not allowed.

Stepping through a list of values
---------------------------------

The function `stepList(<listOfValues>)` is used to define a list of step values for a step variable.

.. code-block:: matlab

    stepList('?')             % returns a list with the current values of the step variable.
    stepList([1 1e-5 10e6])   % defines a the sequence of values of the step parameter as 1, 1e-5, 10e6
    stepList([1, 1e-5, 10e6]) % as above

Array stepping
--------------

For array stepping the step values need to be provided in the form of a matrix. Each row in the matrix carries the values of the subsequent step variables defined with the ``stepVars()`` function (see above) for each run. Hence, the number of rows equals the number of runs that will be executed.

.. code-block:: matlab

    stepVars({'C_1' 'R_1'});       % Defines C_1 and R_1 as step parameters for array stepping
    stepArray([1e-9 10; 1e-8, 20]) % This will cause a two step execution: one run with C_1=1e-9 and R_1=10 and a second run with C_1=1e-8 and R_1=20
    stepArray('?')                 % returns the current step array

------------------------------------
Enable or disable parameter stepping
------------------------------------

Parameter stepping can be enabled or disabled without affecting the settings for parameter stepping, such as, the step variable, the step mthod, etc.

.. code-block:: matlab

    stepOn();               % Enables parameter stepping (does not affect the settings for stepping)
    stepOff();              % Disables parameter stepping (does not affect the settings for stepping)


.. _parameterPlotting:

----------------------------------
Plot parameters against each other
----------------------------------

In SLiCAP you may define parameters that depend on other parameters. This feature is used e.g. in transistor models that have their small-signal parameters defined as a function of operating conditions. 

SLiCAP offers the possibility to obtain the value of all circuit parameters as a function of the step variable. This function can be used to obtain graphs of a buit-in parametric model or user defined parametric model.

In the example below we will plot the transconductance of a MOSFET versus the drain current using a built-in EKV model of a MOS transistor available in the SLiCAP library. The code below shows the netlist of the single-MOS circuit, it doesn't need anything else than the MOS transistor.

.. code-block:: text

    "Parameter sweep demo"
    * netlist file: paramSweep.cir
    .include SLiCAP.lib
    X1 d g 0 0 CMOS18N W=3u L=180n ID={I_D}
    .end


After checking of the circuit, a list with available circuit parameters is obtained by evoking the command ``params()`` in the MATLAB Command Window. The MATLAB output in the Command Window is shown below. The parameter ``g_m_X1`` is the forward transconductance of the MOS transistor in the subn ciruit X1.

.. code-block:: matlab

    >> params()
     
    ans =
     
    [ E_CRIT_X1, IC_CRIT_X1, N_X1, Theta_X1, U_T, IC_X1, I_D, g_m_X1, VAL_X1, g_o_X1, g_b_X1, C_0_X1, C_O_X1, c_gs_X1, c_dg_X1, I_0_X1, mu_0_X1, TOX_X1, epsilon_0, epsilon_SiO2, V_GS_X1, V_T_X1]
     
    >>


Example parameter plot
----------------------

Below a the project file for generating the plot that shows the transconductance as a function of the drain current of the above CMOS18N sub circuit.
The function ``getStepParams({<P1>, <P2>})`` returns a structured array with the two fields ``.P1`` and ``.P2`` that contain the list of values for parameter ``P1`` and ``P2``, respectively.

.. code-block:: matlab

    initProject('paramSweep', mfilename);
    checkCircuit('paramSweep');
    stepVar('I_D');
    stepStart(0);
    stepStop('5m');
    stepNum(100);
    stepMethod('lin');
    stepOn();
    paramData = getStepParams({'I_D', 'g_m_X1'});
    figure();
    plot(paramData.I_D, paramData.g_m_X1);
    xlabel('I_D');
    ylabel('g_m');
    title('g_m versus I_D');
    stophtml();   % This closes the circuit index HTML page
    stophtml();   % This closes the project index HTML page

The resulting :math:`g_m` versus :math:`I_D` plot has been shown below.

.. figure:: /img/g_m-I_D.svg
    :width: 500px
    :alt: Transconductance versus drain current of a MOSFET

Example using built-in parameter plot function
----------------------------------------------

SLiCAP has a buld-in parameter plot function that helps you plotting graphs of parametric models such as device models for transistors.
The function``plotParams(<structured array>)`` plots one parameter versus another one, with a thirs one as step parameter.
The names of the variables, the ranges and the legend entries are defined as fields of the structured array, which is the argument of the function.
Fields with a default value are not obligatory.

.. code-block:: text

    plotData.sweepVar   : sweep parameter, this must be an independent variable in the parameter expressions
    plotData.start      : start value of the sweep parameter
    plotData.stop       : stop value of the sweep parameter
    plotData.num        : number of values of the sweep parameter, default = 50
    plotData.stepMethod : sweep method of the sweep variable, default = 'lin', can also be 'log'
    plotData.stepVar    : name of a step parameter, the sweep variable will be swept with this variable as parameter
    plotData.stepVarName: name of the step parameter to be placed in the legend
    plotData.parSteps   : array with step values, the sweep value will be swept for each value of this list, default = []
    plotData.xVar       : x-axis parameter name, can be any parameter, does not need to be the sweep variable
    plotData.xVarName   : x-axis name to be displayed as axis label, default = plotData.xvar
    plotData.yVar       : y-axis parameter name
    plotData.yVarName   : y-axis name to be displayed as axis label, default = plotData.yvar
    plotData.title      : Title of the plot, default = yVarName(xVarName)

Example of a g_m(I_DS) of an NMOS using the CMOS18N_V subcircuit from the SLiCAP library. This sub circuit accepts nodal voltages of the MOS and calculates the drain current, the forward and reverse inversion coefficients and the small-signal parameters.

The circuit file:

.. code-block:: text

    mosEKVplots
    * SLiCAP netlist file: mosEKVplots.cir
    .include SLiCAP.lib
    X1 d g s 0 CMOS18N_V W={W} L={L} VD={V_D} VG={V_G} VS={V_S}
    .param V_D=1.8 V_G=0.5 V_S=0 W=220n L=180n
    .end

The SLiCAP file:

.. code-block:: matlab

    clear all;
    initProject('MOS EKV project', mfilename);
    checkCircuit('mosEKVplots');
    %
    htmlPage('Circuit data');
    netlist2html('mosEKVplots');
    elementData2html();
    params2html();
    %
    htmlPage('NMOS characteristics');
    %
    defPar('W',1e-6); % changes the width of the MOS
    %
    stepOn();
    %
    plotData.start      = 0;
    plotData.stop       = 1.8;
    plotData.num        = 50;
    plotData.stepMethod = 'lin';
    plotData.parSteps   = [0.2, 0.6, 1.0, 1.4, 1.8];
    plotData.stepVar    = 'V_D';
    plotData.stepVarName= 'V_D';
    plotData.sweepVar   = 'V_G';
    plotData.xVar       = 'I_DS_X1';
    plotData.xVarName   = 'I_D_S';
    plotData.yVar       = 'g_m_X1';
    plotData.yVarName   = 'g_m';
    plotData.stepVar    = 'V_D';
    plotData.stepVarName= 'V_D';
    plotData.title      = 'g_m(I_D_S), W=1u, L=180n'
    %
    GM_IDS = plotParams(plotData);
    fig2html(GM_IDS, 'GM_IDS.svg', 600)
    stophtml()
    stophtml()

Below the figure generated by the above script.

.. figure:: /img/GM_IDS.svg
    :width: 800px
    :alt: Transconductance versus drain current of a MOSFET

