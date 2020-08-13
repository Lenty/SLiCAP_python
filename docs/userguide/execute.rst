======================
Execute an instruction
======================

The SLiCAP function ``execute.m`` evokes the execution of an instruction. It returns a MATLAB® structured array with all relevant data of the executed instruction. If the instruction contains errors, these errors will be written to the log page and execution is aborted. Below the SLiCAP syntax for execution of an instruction and unpacking of the execution results.

.. code-block:: matlab

	result             = execute();        % execute() returns a structured array with the fields described below
	calculatedResult   = result.results    % results of the execution, nested lists depend on setting of dataType
	instrSimType       = result.simType    % setting of the simulation type for this instruction
	instrGainType      = result.gainType   % setting of the gain type for this instruction
	instrDataType      = result.dataType   % setting of the data type for this instruction
	instrSource        = result.source     % name of the signal source for this instruction
	instrDetector      = result.detector   % setting of the detector for this instruction
	instrLgRef         = result.lgRef      % setting of the loop gain reference variable for this instruction
	instrStepTrueFalse = result.step       % setting of parameter stepping for this instruction
	instrStepVar       = result.stepVar    % name of the step parameter for this instruction
	instrStepMethod    = result.stepMethod % setting of the step method for this instruction
	instrStepList      = result.stepList   % step list generated from start value stop value and step method
	instrPostProc      = result.postProc   % post processing field will be discussed below

The contents of the ``.results`` field depends on the data type. This will be discussed in more detail in the corresponding sections below. The other fields carry the setting of the corresponding instruction variable at the time of the execution with exception of the ``.stepList`` field. This attributes carries the list of values for the step variable, based on the settings of step start, step stop, step number and step method.

-----------------
Execution results
-----------------

The contents and the structure of the ``execute.results`` field depends on the data type. Below, this contents will be discussed in detail for each data type.

Data type MATRIX
----------------

The structure of the results field for this data type is: ``[..., [MNA_Ii, MNA_Gi, MNA_Di], ...]``

1. ``MNA_Ii`` is the vector with the values of the independent sources for the i-th run.

2. ``MNA_Gi`` is the admittance matrix according to modified nodal analysis for the i-th run, adapted to the gain type.

3. ``MNA_Di`` is the vector with the dependent variables: the nodal voltages and the currents through elements that have been defined by a current-controlled notation for the i-th run.

.. code-block:: matlab

	dataType('matrix');
	result           = execute();
	runResults       = result.results
	firstRunMatrices = runResults(1)
	MNA_I1           = firstRunMatrices(1) % Vector with independent variables
	MNA_G1           = firstRunMatrices(2) % Square MNA matrix
	MNA_D1           = firstRunMatrices(3) % Vector with dependent variables

Data type LAPLACE
-----------------

The structure of the results field for this data type is: ``[..., H_si, ...]``, in which ``H_si`` is the Laplace transform of the voltage of a voltage across a voltage detector, the current though a current detector or of a transfer function, for the i-th run.

.. code-block:: matlab

	dataType('laplace');
	result     = execute();
	runResults = result.results
	H_s1       = runResults(1)
	
		
Data type SOLVE
-----------------

The structure of the results field for this data type is: ``[..., [MNA_D_i, SOL_i], ...]``, in which ``MNA_D`` is the vector with dependent variables for the i-th run, and ``SOL_i`` is the network solution for the i-th run.

Note:

Although MuPAD can handle very large symbolic expressions, MathJax may not be able to render them on a web page.

.. code-block:: matlab

	gainType('vi');
	dataType('solve');
	result          = execute();
	runResults      = result.results;
	firstRunResults = runResults(1);
	depVariables    = firstRunResults(1);
	solution        = firstRunResults(2);
    htmlPage('Results');
    eqn2html(depVariables, solution);

Data type NUMER
---------------

The structure of the results field for this data type is: ``[..., N_si, ...]``, in which ``N_si`` is the numerator of the Laplace transform of the voltage across a voltage detector, the current though a current detector or of a transfer function, for the i-th run.

.. code-block:: matlab

	dataType('numer');
	result     = execute();
	runResults = result.results
	N_s1       = runResults(1);   

Data type DENOM
---------------

The structure of the results field for this data type is: ``[..., D_si, ...]``, in which ``D_si`` is the denominator of the Laplace transform of the voltage across a voltage detector, the current though a current detector or of a transfer function, for the i-th run.

.. code-block:: matlab

	dataType('denom');
	result     = execute();
	runResults = result.results
	D_s1       = runResults(1)

Data type IMPULSE
-----------------

The structure of the results field for this data type is: ``[..., h_ti, ...]``, in which ``h_ti`` is the inverse Laplace transform of a transfer function, for the i-th run.

.. code-block:: matlab

	dataType('impulse');
	result     = execute();
	runResults = result.results
	h_t1       = runResults(1)

Data type STEP
--------------

The structure of the results field for this data type is: ``[..., a_ti, ...]``, in which ``a_ti`` is the inverse Laplace transform of :math:`\frac{1}{s} \times` the Laplace transform of a transfer function, for the i-th run.

.. code-block:: matlab

	dataType('step');
	result     = execute();
	runResults = result.results
	a_t1       = runResults(1)

Data type TIME
--------------

The structure of the results field for this data type is: ``[..., f_ti, ...]``, in which ``f_ti`` is the inverse Laplace transform of the voltage across a voltage detector or the current though a current detector, for the i-th run.

.. code-block:: matlab

	dataType('time');
	result     = execute();
	runResults = result.results
	f_t1       = runResults(1)

Data type POLES
---------------

The structure of the results field for this data type is: ``[..., [p_1i, p_2i, ... p_ji, ...], ...]``, in which ``p_ji`` is the j-th complex solution in [rad/s] of the denominator of the Laplace transform of a transfer function, for the i-th run. Poles with identical complex frequencies will be listed separately.

.. code-block:: matlab

	dataType('poles');
	result     = execute();
	runResults = result.results;
	polesRun1  = runResults(1);
	p_1_1      = polesRun1(1);    % frequency in [rad/s] of first pole from the first run


Data type ZEROS
---------------

The structure of the results field for this data type is: ``[..., [z_1i, z_2i, ... z_ji, ...], ...]``, in which ``z_ji`` is the j-th complex solution in [rad/s] of the numerator of the Laplace transform of the voltage across a voltage detector, the current though a current detector or of a transfer function, for the i-th run. Zeros with identical complex frequencies will be listed separately.

.. code-block:: matlab

	dataType('zeros');
	result     = execute();
	runResults = result.results;
	zerosRun1  = runResults(1);
	z_1_1      = zerosRun1(1);    % frequency in [rad/s] of first zero from the first run

Data type PZ
------------

The structure of the results field for this data type is: ``[..., [ [p_1i, p_2i, ... p_ji, ...], [z_1i, z_2i, ... z_ki, ...], DCgain_i ], ...]``, in which:

1. ``p_ji`` is the j-th complex solution in [rad/s] of the denominator of the Laplace transform of the voltage across a voltage detector, the current though a current detector or of a transfer function, for the i-th run. Poles with identical complex frequencies will be listed separately.

2. ``z_ki`` is the k-th complex solution in [rad/s] of the numerator of the Laplace transform of the voltage across a voltage detector, the current though a current detector or of a transfer function, for the i-th run. Zeros with identical complex frequencies will be listed separately.

3. ``DCgain_i`` is the zero-frequency transfer for the i-th run. If there exists a pole at s=0, the zero-frequency transfer is set to the MuPAD® boolean FALSE.

Note: poles and zeros with a relative frequency difference smaler than :math:`10^{DISP}` [1]_ will be cancelled.

.. [1] DISP is the number of digits for displaying floating point numbers.

.. code-block:: matlab

	dataType('pz');
	result     = execute();
	runResults = result.results; % results of all runs
	pzDCrun1   = runResults(1);  % results of first run
	polesRun1  = pzDCrun1(1);    % frequencies in [rad/s] of the poles of the first run
	zerosRun1  = pzDCrun1(2);    % frequencies in [rad/s] of the zeros of the first run
	DCgainRun1 = pzDCrun1(3);    % DC value of the gain of the first run
		
Data type NOISE
---------------

The structure of the results field for this data type is: ``[..., [ sourceNames, sourceSpectra_i, onoiseTerms_i, inoiseTerms_i, onoise_i, inoise_i, units ], ...]``, in which:

1. ``sourceNames = [ ..., N_j, ... ]``, in which ``N_j`` is the name (identifier) of the j-th noise source in the circuit netlist.

2. ``sourceSpectra_i = [ ..., S_j, ... ]``, in ``which S_j`` is spectral density in [V²/Hz] or in [A²/Hz] of the j-th noise source, for the i-th run.

3.  ``onoiseTerms_i = [ ..., So_ji, ... ]``, in which ``So_ji`` is the contribution of the noise source ``N_j`` to the spectral density at the detector in [V²/Hz] or in [A²/Hz], for the i-th run.

4. ``inoiseTerms_i = [ ..., Si_ji, ... ]``, in which ``Si_ji`` is the source-referred contribution of the noise source ``N_j`` in [V²/Hz] or in [A²/Hz], for the i-th run.

5. ``onoise_i`` is the spectral density of the total detector-referred noise in [V²/Hz] or in [A²/Hz], for the i-th run.

6. ``inoise_i`` is the spectral density of the total source-referred noise in [V²/Hz] or in [A²/Hz], for the i-th run.

7. ``units = [ uD, uS]``

    - ``uD`` represents the units of the detector: A for a current detector and V for a voltage detector.

    - ``uS`` represents the units of the signal source: A for a current source and V for a voltage source.

Below an example how to unpack the results structure of a noise calculation.

.. code-block:: matlab

	dataType('noise');
	result                              = execute();
	runResults                          = result.results;
	noiseRun1                           = runResults(1);
	noiseNames                          = noiseRun1(1);
	noiseName1                          = char(noiseNames(1));
	noiseSourceSpectra1                 = noiseRun1(2);
	detectorReferredNoiseContributions1 = noiseRun1(3);
	sourceReferredNoiseContributions1   = noiseRun1(4);
	detectorReferredNoiseSpectrum1      = noiseRun1(5);
	sourceReferredNoiseSpectrum1        = noiseRun1(6);
	units                               = noiseRun1(7);
	detectorReferredNoiseSpectumUnits   = char(units(1)^2/sym('Hz'));
	sourceReferredNoiseSpectumUnits     = char(units(2)^2/sym('Hz'));
	
Data type DC
------------

The structure of the results field for this data type is: ``[..., DC_i, ...]``, in which ``DC_i`` is the DC voltage at the voltage detector or the DC current though a current detector, for the i-th run.

.. code-block:: matlab

	dataType('dc');
	result     = execute();
	runResults = result.results
	DC_1       = runResults(1)

Data type DCVAR
---------------

The structure of the results field for this data type is: ``[..., [ sourceNames, sourceVar_i, detVarTerms_i, srcVarTerms_i, detVar_i, srcVar_i, detRelVarTerms_i, srcRelValTerms_i, detVarRel_i, srcVarRel_i, units_i, Dvect_i, DCsol_i], ...]``, in which:

1. ``sourceNames = [ ..., N_j, ... ]``, in which ``N_j`` is the name (identifier) of the j-th source in the circuit netlist.

2. ``sourceVar_i = [ ..., Var_j, ... ]``, in ``which Var_j`` is variance in [V²] or in [A²] of the j-th source, for the i-th run.

3.  ``detVarTerms_i = [ ..., Vout_ji, ... ]``, in which ``Vout_ji`` is the contribution of the source ``N_j`` to the variance at the detector in [V²] or in [A²], for the i-th run.

4. ``srcVarTerms_i = [ ..., Vin_ji, ... ]``, in which ``Vin_ji`` is the contribution to the source-referred variance of source ``N_j`` in [V²] or in [A²], for the i-th run.

5. ``detVar_i`` is the detector-referred variance in [V²] or in [A²], for the i-th run.

6. ``srcVar_i`` is the source-referred variance in [V²] or in [A²], for the i-th run.

7. ``detRelVarTerms_i`` as (3) but now relative to the DC value of the detector quantity (current or voltage), for the i-th run.

8. ``srcRelValTerms_i`` as (4) but now relative to the DC value of the detector quantity (current or voltage), for the i-th run.

9.  ``detVarRel_i`` as (5) but now relative to the DC value of the detector quantity (current or voltage), for the i-th run.

10.  srcVarRel_i`` as (6) but now relative to the DC value of the detector quantity (current or voltage), for the i-th run.

11. ``units_i = [ uD, uS]``

    - ``uD`` represents the units of the detector for run i: A for a current detector and V for a voltage detector.

    - ``uS`` represents the units of the signal source for run i: A for a current source and V for a voltage source.
    
12.  ``Dvect_i`` the vector with independent variables, for the i-th run.
 
13.  ``DCsol_i`` the DC solution of the network: the values of the variables in ``Dvect_i``, for the i-th run. 

Below an example how to unpack the results structure of a dc variance calculation.

.. code-block:: matlab

	dataType('dcvar');
	result                              = execute();
	runResults                          = result.results;
	varRun1                             = runResults(1);
	varNames                            = varRun1(1);
	varName1                            = char(varNames(1));
	varSource1                          = varRun1(2);
	detectorReferredVarContributions1   = varRun1(3);
	sourceReferredVarContributions1     = varRun1(4);
	totalDetectorReferredVariance1      = varRun1(5);
	totalSourceReferredVariance         = varRun1(6);
	detectorReferredRelativeVarContrs1  = varRun1(7);
	sourceReferredRelativeVarContrs1    = varRun1(8);
	totalRelativeDetReferredVariance1   = varRun1(9);
	totalRelativeSrcReferredVariance1   = varRun1(10);
	units                               = varRun1(11);
	detectorReferredVarianceUnits       = char(units(1)^2);
	sourceReferredVarianceUnits         = char(units(2)^2);
	vectorDependentVariables            = varRun1(12);
	DCnetworkSolution                   = varRun1(13);
		
Data type DCSOLVE
-----------------

The structure of the results field for this data type is: ``[..., [MNA_D_i, DCsol_i], ...]``, in which ``MNA_D`` is the vector with dependent variables for the i-th run, and ``DCsol_i`` is the DC network solution for the i-th run.

.. code-block:: matlab

	dataType('dcsolve');
	result          = execute();
	runResults      = result.results
	firstRunResults = runResults(1)
	depVariables    = firstRunResults(1)
	DCsolution      = firstRunResults(2)
