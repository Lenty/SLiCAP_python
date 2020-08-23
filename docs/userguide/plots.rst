============
Create plots
============

Plotting of the results can be performed with the aid of the MATLAB built-in plot functions. SLiCAP provides some plot functions that facilitate easy plotting of graphs from execution results, with automatic determination of colors and markers and generation of plot legends and axis labels. These plots have been described in the following sections.

------------------------------
Pole-zero and root-locus plots
------------------------------

The function ``plotPZ.m`` can be used to make pole-zero plots and root-locus plots. Axis labels and legends will be created automatically but can be redefined. Below the syntax for plotting the results of a pole-zero analysis in the MATLAB workspace.

``plotPZ(< title >, [r1 (, r2, ...)], 'auto'|[xMin,xMax], 'auto'|[yMin,yMax]);``

Below the syntax for creating a MATLAB figure object from the results of a pole-zero analysis.

``myPZfig=plotPZ(< title >, [r1 (, r2, ...)], 'auto'|[xMin,xMax], 'auto'|[yMin,yMax]);``

In which:

    - ``title`` is a character string for the title of the plot. It will be placed on top of the figure.
    - ``[r1 (, r2, ...)]`` is an array with execution results of instructions with the data type set to poles, zeros of pz.
    - ``'auto'|[xMin,xMax]`` is the x-axis (real part of s/(2π)) frequency range in [Hz]:
    
    
	      * ``'auto'``: auto-scaling of the x-axis
	      * ``[xMin,xMax]``: Array with two doubles ``xMin`` and ``xMax``, representing the minimum frequency and the maximum frequency [Hz] of the x-axis, respectively
	      
    - ``'auto'|[yMin,yMax]`` is the y-axis (imag part of s/(2π)) frequency range in [Hz]:
    
	      * ``'auto'``: auto-scaling of the y-axis
	      * ``[yMin,yMax]``: Array with two doubles yMin and yMax, representing the minimum frequency and the maximum frequency in [Hz] of the y-axis, respectively

Below an example for plotting the results of multiple single-run pole-zero analysis in one figure. 

Assume we have checked the netlist of a circuit and found no errors. We also have defined the source, the detector and the loop gain reference variable. Also assume all parameters have numerical values assigned. Under these conditions we may plot the poles and the zeros for the five transfer functions of the asymptotic-gain model: the asymptotic-gain, the direct transfer, the loop gain, the servo function and the gain, with the instructions below:

.. code-block:: matlab

    stepOff()
    %
    simType('numeric')
    dataType('pz')
    %
    gainType('asymptotic');
    pz(1) = execute()
    %
    gainType('direct');
    pz(2) = execute()
    %
    gainType('loopgain');
    pz(3) = execute())
    %
    gainType('servo');
    pz(4) = execute()
    %
    gainType('gain');
    pz(5) = execute()
    %
    plotPZ('Poles and zeros', pz, 'auto', 'auto');
    
All these results will be plotted in one figure with a legend with 10 entries. The zeros will be plotted with marker ``'o'`` and the poles with marker ``'x'``. The default colors of these markers depend on the gain type as listed below.

		- ``ASYMPTOTIC``:	red
		- ``DIRECT``:	green
		- ``LOOPGAIN``:	black
		- ``SERVO``:	magenta
		- ``GAIN``:	blue

Below an example of plotting a root locus.

SLiCAP can plot the positions of the poles and the zeros of a transfer as a function of any circuit parameter. Generally, the root locus shows the position of the poles of the servo function while stepping the root-locus gain or the zero-frequency loop gain. Branches of such a root locus plot start on the poles of the loop gain and end on the zeros of the loop gain. Assume the DC loopgain of the above circuit can varied with the parameter A₀ that has a nominal value of 10⁶. The script below plots:

		1. The root-locus: 101 magenta dots ``.``, one dot for each pole for each value of the step parameter A₀=0 .. 10⁶, 100 steps
		2. A magenta ``'x'`` for at the start point of the root locus
		3. A magenta ``'+'`` at the end point of the root locus
		4. The zeros of the loop gain: one black ``'o'`` for each zero of the loop gain
		5. The poles of the loop gain: one black ``'x'`` for each pole of the loop gain

The plot will have five legend entries: one for each item of the above list.

.. code-block:: matlab

    stepVar('A_0');
    stepStart(0);
    stepStop(1E6);
    stepNum(100);
    stepMethod('lin');
    stepOn();
    simType('numeric');
    gainType('servo');
    dataType('poles');
    pz1 = execute();
    stepOff();
    gainType('loopgain');
    dataType('pz');
    pz2 = execute();
    plotPZ('Root Locus', pz, 'auto', 'auto');
    
For the design of electronic circuits, other root locus plots such as a plot of the pole positions versus a compensation capacitance can be more of interest. Assume hereto that the parameter A₀ has been given its nominal value, while the value of a compensation capacitor ``C_c`` steps from 5pF to 10pF in five steps (six values). We will plot the poles of the gain as a function of this capacitance in the same figure. The instruction below will add six blue dots for each pole of the gain, including a blue marker ``'x'`` for each pole at the start value of the step parameter and a blue marker ``'+'`` at the end value of the step parameter. It will add three items to the legend: one for the starting value of the step parameter ``C_c``, one for the dotted trace and one for the end value of the step parameter.

.. code-block:: matlab

    stepVar('C_c');
    stepStart('5p');
    stepStop('10p');
    stepNum(5);
    stepMethod('lin');
    gainType('gain');
    dataType('poles');
    pz3 = execute();
    plotPZ('Root Locus', pz, 'auto', 'auto');


----------------------
Frequency domain plots
----------------------

Frequency domain plots have the frequenncy in [Hz] plotted along the x-axis.

dB magnitude plot
-----------------

The function ``plotdBmag.m`` can be used to plot the magnitude of a transfer or of a voltage or current versus frequency. The frequency is plotted on a logarithmic scale. The vertical 'dB' axis has a linear scale. Axes labels and plot legend will be generated automatically, but they can be redefined.

Below the syntax for plotting a dB magnitude plot in the MATLAB workspace from the results of one or more Laplace transfer function analyses. The y-axis variable of a Laplace transfer function H(s) is defined as:

.. math::

		y=20{\log}_{10} |\left( H(s)_{s=j2\pi f} \right|

The y-axis has a linear scale and the frequency axis has a logarithmic scale. The syntax is:

``plotdBmag(< title >, [r1 (, r2, ...)], fMin, fMax, < nPts >);``

In which:

    - ``title`` is a character string for the title of the plot. It will be placed on top of the figure.
    - ``[r1 (, r2, ...)]`` is a structured array with execution results of instructions with the data type set to ``LAPLACE``.
    - ``fStart`` is the start frequency in [Hz], a positive number (double) smaller than ``fStop``
    - ``fStop`` is the stop frequency in [Hz], a positive number larger (double) than ``fStart``
    - ``nPts`` is an integer representing the number of frequency points to be evaluated

Like with the ``plotPZ.m`` function, execution results of multiple analysis with and without parameter stepping can be plotted in one figure. The example below shows in which way the dB magnitude characteristics of all the gain types of the asymptotic-gain model can be plotted in one figure with a frequency scale from 1Hz to 10MHz and 200 data points.

.. code-block:: matlab

    stepOff();
    %
    simType('numeric');
    dataType('laplace');
    %
    gainType('asymptotic');
    H(1) = execute();
    %
    gainType('direct');
    H(2) = execute();
    %
    gainType('loopgain');
    H(3) = execute());
    %
    gainType('servo');
    H(4) = execute();
    %
    gainType('gain');
    H(5) = execute();
    %
    plotdBmag('dB magnitude asymptotic-gain model', H, 1, 10e6, 200);

The figure generated by the above script has five legend entries and uses the colors as described above. Both frequency domain plotting an time domain plotting behave different from complex frequency domain plotting (``plotPz.m``) when using parameter stepping. It is not recommended to combine the results of instructions with parameter stepping and without parameter stepping in one plot. All curves for one gain type will then obtain the color for that gain type.

Below an example of a dB magnitude plot of the gain for the six values of a compensation capacitance ``C_s`` as shown in the example for the root locus plot.

.. code-block:: matlab

    stepVar('C_c');
    stepStart('5p');
    stepStop('10p');
    stepNum(5);
    gainType('gain');
    dataType('laplace');
    plotdBmag('dB magnitude GAIN, step C_c', execute(), 1, 10e6, 200);

The traces will now have the default MATLAB colors and each trace will have its own legend entry.

Logarithmic magnitude plot
--------------------------

The function ``plotMag.m`` can be used for plotting the magnitude on logarithmic scale. It has the same syntax and shows the same behavior as the function ``plotdBmag.m``. The y-axis variable is now defined as:

.. math::

		y=|\left( H(s)_{s=j2\pi f} \right|

Both the frequency axis and the y-axis have a logarithmic scale. Axes labels and plot legend will be generated automatically, but they can be redefined.

Linear magnitude plot
---------------------

The function ``plotMagLin.m`` can be used for plotting the magnitude on a linear scale. It has the same syntax and shows the same behavior as the function ``plotdBmag.m``. The y-axis variable is now defined as:

.. math::

		y=|\left( H(s)_{s=j2\pi f} \right|

The frequency axis has a logarithmic scale and the y-axis has a linear scale. Axes labels and plot legend will be generated automatically, but they can be redefined.

Real part plot
--------------

The function ``plotReal.m`` can be used for plotting the real part on a linear scale. It has the same syntax and shows the same behavior as the function ``plotMagLin.m``. The y-axis variable is now defined as:

.. math::

		y=\mathrm{Re}\left( H(s)_{s=j2\pi f} \right)

The frequency axis has a logarithmic scale and the y-axis has a linear scale. Axes labels and plot legend will be generated automatically, but they can be redefined.

Imaginary part plot
-------------------

The function ``plotImag.m`` can be used for plotting the imaginary part on a linear scale. It has the same syntax and shows the same behavior as the function ``plotReal.m``. The y-axis variable is now defined as:

.. math::

		y=\mathrm{Im}\left( H(s)_{s=j2\pi f} \right)

The frequency axis has a logarithmic scale and the y-axis has a linear scale. Axes labels and plot legend will be generated automatically, but they can be redefined.

Phase plot
----------

The function ``plotPhase.m`` can be used to plot the group delay versus frequency. It has the same syntax and shows the same behavior as the function ``plotDelay.m``. The y-axis variable is now defined as:

.. math::

		y=\frac{180}{\pi} \arctan\left( \frac{\mathrm{Im}(H(s))}{\mathrm{Re}(H(s))} \right)_{s=j2\pi f}

The frequency axis has a logarithmic scale and the y-axis has a linear scale. The phase will be unwrapped. Axes labels and plot legend will be generated automatically but can be redefined.

Delay plot
----------

The function ``plotDelay.m`` can be used to plot the phase. It has the same syntax and shows the same behavior as the function ``plotdBmag.m``. The y-axis variable is now defined as:

.. math::

		y= -\frac{d}{d(2\pi f)} \left(\arctan\left( \frac{\mathrm{Im}(H(s))}{\mathrm{Re}(H(s))} \right)_{s=j2\pi f}\right)

The frequency axis has a logarithmic scale and the y-axis has a linear scale. Axes labels and plot legend will be generated automatically but can be redefined.

-----------
Polar plots
-----------

Polar plots have the frequency in [Hz] as parameter along the curve and display the magnitude and phase on a polar grid.

Polar linear magnitude
----------------------

The function ``plotPolarLin.m`` plots :math:`H(s)` on a polar grid with a linear magnitude scale. It has the same behavior as the function ``plotMag.m``.


The syntax for ``plotPolarLin.m`` is:

``plotPolarLin(< title >, [r1 (, r2, ...)], fStart, fStop, < nPts >);``

where ``ri`` is a structured array obtained from an ``execute()`` instruction with data type set to ``LAPLACE``. 

Polar dB magnitude
------------------

The function ``plotPolardB.m`` plots :math:`H(s)` on a polar grid with a linear dB scale for the magnitude. It has the same behavior as the function ``plotPolarLin.m``.

The syntax for ``plotPolardB.m`` is:

``plotPolardB(< title >, [r1 (, r2, ...)], fStart, fStop, < nPts >);``

where ``ri`` is a structured array obtained from an ``execute()`` instruction with data type set to ``LAPLACE``. 

Nyquist plot
------------

The function ``plotNyquist.m`` only works with gain type ``LOOPGAIN``. It plots :math:`-L(s)` on a polar grid; where :math:`L(s)` is the loop gain according to the asymptotic-gain model. The function has the same behavior as the function ``plotPolarLin.m``.

The syntax for ``plotNyquist.m`` is:

``plotNyquist(< title >, [r1 (, r2, ...)], fStart, fStop, < nPts >);``

where ``ri`` is a structured array obtained from an ``execute()`` instruction with data type set to ``LAPLACE`` and gain type set to ``LOOPGAIN``. 

-----------------
Time domain plots
-----------------

The function ``plotTime.m`` has about the same syntax and similar behavior with respect to parameter stepping as ``plotdBmag.m``. The y-axis variable depends on the data type of the instruction. Both the time axis and the y-axis have a linear scale. A plot legend will be generated automatically but it can be redefined. A label for the vertical axis needs to be added with the MATLAB® function: ``ylabel(< 'labelText' >)``.

The syntax for this function is:

``plotTime(< title >, [r1 (, r2, ...)], tStart, tStop, < nPts >);``

In which:

		- ``plotTitle`` is a character string for the title of the plot. It will be placed on top of the figure.
		- ``[r1 (, r2, ...)]`` is a structured array with execution results of instructions with the data type set to ``IMPULSE``, ``STEP`` or ``TIME``.
		-	``tStart`` is the start time in [s], zero or a positive number (double) smaller than ``tStop``
		- ``tStop`` is the stop time in [s], a positive number larger (double) than ``tStart``
		- ``nPts`` is an integer representing the number of time points to be evaluated

-----------
Noise plots
-----------

Output noise
------------

The function ``plotOnoise.m`` has the same syntax and shows similar behavior as ``plotdBmag.m``. The y-axis variable is now defined as the spectral density of the detector-referred noise in [V/ :math:`\sqrt{Hz}` ] or [A/ :math:`\sqrt{Hz}` ], depending on the detector type. Since the gain type for noise analysis should be VI, colors for traces without parameter stepping are mapped to their corresponding post processing type rather than to their gain type. This has been listed below.

		- ``None``:	blue
		- ``Integrated``:	green
		- ``CDS``:	red
		- ``CDS-int``:	black

Both the frequency axis and the y-axis have a logarithmic scale. A plot legend will be generated automatically but it can be redefined. A label for the vertical axis needs to be added with the MATLAB function: ``ylabel(< 'labelText' >)``.

The syntax is:

``plotOnoise(< title >, [r1 (, r2, ...)], fMin, fMax, < nPts >);``

In which:

		- ``title`` is a character string for the title of the plot. It will be placed on top of the figure.
		- ``[results1 (, results 2, ...)]`` is an array with execution results of instructions with the data type set to NOISE. 
		
		It can also be the result of one of the noise postprocessing functions:
		
				* ``doNoiseInt.m``
				* ``doCDS.m``
				* ``doCDSint.m``
		
		Plot legend and labels are automatically adapted to the type of post processing function
		
		- ``fStart`` is the start frequency in [Hz], a positive number (double) smaller than ``fStop``
		- ``fStop`` is the stop frequency in [Hz], a positive number larger (double) than ``fStart``
		- ``nPts`` is an integer representing the number of frequency points to be evaluated

Input noise
-----------

The function ``plotInoise,m`` has the same syntax and shows similar behavior as ``plotOnoise.m``. The y-axis variable is now defined as the spectral density of the detector-referred noise in [V/ :math:`\sqrt{Hz}` ] or [A/ :math:`\sqrt{Hz}` ], depending on the detector type. Available post processing functions for ``plotInoise.m`` are: ``None`` and ``Integrated``.

--------------------------------
Step variable as x-axis variable
--------------------------------

The function ``plotVsStep..`` plots a curve that can be derived from the execution results as a function of the step variable. The step variable values are taken as x-axis variables and the results of a goal function such as ``{'totalOnoise', 1, 10e6}`` operating on the execution results with or without post processing function are plotted along the y-axis. Labels for the frequency axis and the vertical axis are automatically added, but can be redefined. A legend has to be added manually.

The syntax for this function is:

``plotVsStep(< title >, [r1 (, r2, ...)], {< goalFuncArgs >});``

In which:

		- ``title`` is a character string for the title of the plot. It will be placed on top of the figure.
		- ``[r1 (, r2, ...)]`` is an array with execution results of instructions with parameter stepping. The values of the step variable are plot along the x-axis.
		- ``goalFuncArgs`` is a character array with arguments for the specific goal function. Currently implemented goal functions have been listed below.

--------------
Goal functions
--------------

Total detector noise versus step variable
-----------------------------------------
		
The goal function argument ``{'totalOnoise', fMin, fMax [, tau]}`` calculates the total detector-referred RMS noise over the frequency range specified by ``fMin`` and ``fMax``. This goal function requires execution results of an instruction with data type set to ``NOISE`` and its post processing field set to ``none`` or ``CDS``. The optional parameter ``tau`` is the 
CDS delay time.

The goal function argument ``{'totalInoise', fMin, fMax[, tau]}`` calculates the total source-referred RMS noise over the frequency range specified by ``fMin`` and ``fMax``. This goal function requires execution results of an instruction with data type set to ``NOISE`` and its post processing field set to ``none``.

The script below plots the total RMS noise after correlated double sampling over a frequency range from 1Hz to 10MHz as a function of the source capacitance ``C_s``. The value of this capacitance ranges from 5pF to 10pF.

.. code-block:: matlab

    gainType('VI');
    dataType('noise');
    stepVar('C_s');
    stepStart('5p');
    stepStop('10p');
    stepNum('20');
    stepOn();
    tauCDS = 1E-6;
    result = execute();
    CDSresult = doCDS(result, tauCDS);
    goalFunction = {'totalOnoise', 1, 10e6, tauCDS};
    plotVsStep('Total output noise after CDS', CDSresult, goalFunction);
    legend({'onoiseCDS'}, 'location', 'eastoutside', 'Box', 'off');

Noise Figure versus step variable
---------------------------------

The goal function argument ``{'noiseFigure', fMin, fMax [, tau]}``calculates the noise figure over the frequency range specified by ``fMin`` and ``fMax``. This goal function requires execution results of an instruction with data type set to ``NOISE`` and the definition of a signal source. The optional parameter ``tau`` is the CDS delay time.
    
DC value at detector versus step variable
-----------------------------------------

The goal function argument ``{'dc'}`` plots the DC value at the detector against the step variable.


Detector-referred DC variance versus step variable
--------------------------------------------------

The goal function argument ``{'detVariance'}`` plots the contributions to the variance at the detector of all the independent sources in the circuit, against the step variable.


Detector-referred DC standard deviation versus step variable
------------------------------------------------------------

The goal function argument ``{'detStdev'}`` plots the standard deviation at the detector, against the step variable.


Source-referred DC variance versus step variable
------------------------------------------------

The goal function argument ``{'srcVariance'}`` plots the equivalent source contributions of all the independent sources in the circuit, against the step variable.


Source-referred DC standard deviation versus step variable
----------------------------------------------------------

The goal function argument ``{'srcStdev''}`` plots the equivalent source standard deviation, against the step variable.
