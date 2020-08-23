======================================
Download, install and configure SLiCAP
======================================

---------------------------
Download and Install SLiCAP
---------------------------

SLiCAP is available under the following license:

.. image:: https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png
    :target: http://creativecommons.org/licenses/by-nc-nd/4.0/
    :width: 88
    :alt: Creative Commons License

SLiCAP by `Anton Montagne <http://www.analog-electronics.eu>`_ is licensed under a `Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License <http://creativecommons.org/licenses/by-nc-nd/4.0/>`_. Based on a work at: `http://www.analog-electronics.eu/slicap/slicap.html <http://www.analog-electronics.eu/slicap/slicap.html>`_


Install SLiCAP
--------------

SLiCAP consists of a set of MATLAB® and MuPAD® scripts, symbols for schematic capture programs (LTspice and gSchem), style sheets for HTML pages and device library files. These files can be downloaded and installed from within MATLAB®. 

- Download `installSLiCAP.p <https://www.analog-electronics.eu/downloads/installSLiCAP.p>`_. 

- Simply run it in MATLAB®, it will ask for the 'SLiCAP_INSTALLPATH' and copy all the files to it.

In order to run SLiCAP you must have a valid license for running `MATLAB® <https://www.mathworks.com/products/matlab.html>`_ and its `Symbolic Math Toolbox <https://www.mathworks.com/products/symbolic.html>`_, version R2014a or later.


You can test the installation by typing:

- 'path' in the MATLAB® command window. This should display the MATLAB® search paths and the SLiCAP installation path should be included.

- 'Help' (with capital 'H') in the MATLAB® command window. The MATLAB® browser should then display the SLiCAP help file.

File extensions
---------------

The file extension for SLiCAP netlist files is ``"cir"``; it cannot be changed.

Use metric prefixes
-------------------

The following metric prefixes can be used:

.. csv-table:: SLiCAP metric prefixes
    :header: "name", "Symbol", "Base 10 value"
    :widths: 50, 10, 20

    "peta", "P", :math:`10^{15}`
    "tera", "T", :math:`10^{12}`
    "giga", "G", :math:`10^9`
    "mega", "M", :math:`10^6`
    "kilo", "k", :math:`10^3`
    "mili", "m", :math:`10^{-3}`
    "micro", "u", :math:`10^{-6}`
    "nano", "n", :math:`10^{-9}`
    "pico", "p", :math:`10^{-12}`
    "femto", "f", :math:`10^{-15}`
    "atto", "a", :math:`10^{-18}`

Please notice that these prefixes are case sensitive and differ from standard SPICE syntax.

From version 0.4 build 1350 the expression syntax checker can handle parameter names identical to metric prefixes. View the netlist syntax section for more information.


===========================
Initialize a SLiCAP project
===========================

Starting a SLiCAP project is as simple creating a project m-file that you store in some project directory. This m-file
starts with:

.. code-block:: matlab

    % Save this file in your project directory
    % Always run it from this directory
    %
    clear all;
    initProject('myProject', mfilename('fullpath'));
    % Here you can insert calls to m-files that belong to this project
    stophtml();

Running this file will:

#. Create the required sub directory structure
#. Create the MuPAD® startup file ``SLiCAPsettings.mu`` in the project directory
#. Copy the html style files to their required locations.

The MATLAB response to this code is:

.. code-block:: matlab

    ============================================================
    | SLiCAP_V06_2020a released or installed: 2020-04-25 09:14 |
    | Creative Commons 4.0 International License.              |
    | Type "Help" for help, or visit:                          |
    | www.analog-electronics.eu/slicap/slicap.html.            |
    | Book: Structured Electronic Design.                      |
    | Running project: myProject
    | SLiCAP (c) 2009-2020 Anton J.M. Montagne.                |
    ============================================================

Each time you run the above script after the directory structure has been created, the html style files will be overwritten. See section: :ref:`html` for more information on html documentation. 

After initialization of the project you will find the ``SLiCAPsettings.mu`` MuPAD script file in your project directory. This file can be edited, its contents will be described below.

The project files and the file ``SLiCAPsettings.mu`` will not be overwritten.

.. _globalParams:

------------------------
Configure SLiCAP options
------------------------

The main part of SLiCAP has been written in the script language of the Symbolic Math Toolbox MuPAD®. All MuPAD® functions, except those required for the initialization have been put together in the file ``SLiCAP.mu`` in the MuPAD subdirectory in the SLiCAP install path.

Knowledge of the MuPAD® scripting language is not required when working with SLiCAP. 

You can change the project-specific settings in the ``SLiCAP_settings.mu`` file in your project directory as described below.

SLiCAPsettings.mu
-----------------

.. code-block:: mupad

    // MuPAD settings, this MuPAD file should be edited with care!
    MATHJAXLOCAL := FALSE:  // TRUE if mathJax has been installed locally in the
                            // SLiCAP installation path, else FALSE.
    // User options:
    FMAX         := 1E13:   // Maximum absolute value of the frequency of poles
                            // and zeros in rad/s. This suppresses false poles
                            // and zeros generated by rounding errors.
    DISP         := 4:      // Number of significant digits to be displayed.
    CALC         := 20:     // Number of significant digits for calculation.
    MAXSUBS      := 10:     // Maximum number of nested substitutions.
    LTSPICE_XU2X := TRUE:   // Converts element identifier "XU" to "X".
    GLOBAL_DEFS  := [k = 1.38064852e-23, q = 1.60217662e-19, T = 300, U_T = k*T/q ,
                     epsilon_0 = 1/c^2/mu_0, epsilon_SiO2 = 3.9, mu_0=4*PI*1e-7,
                     c = 2.99792458e+08]:
    // SLiCAP search path settings:
    // "" = project directory.
    // "subdir/" = subdirectory "subdir" in project directory.
    CIRPATH      := "":     // Search path for schematics and netlist files:
                            // (.asc, .cir, .net, sch).
    TXTPATH      := "":     // Search path for text include files (file2html.m).
    CSVPATH      := "":     // Search path for CSV include files (csv2html.m).
    IMGPATH      := "":     // Search path for image include files (img2html.m).


MathJax
-------

SLiCAP uses MathJax to render LaTeX embedded in html. LaTeX is used for expressions. By default MathJax rendering of equations requires an Internet connection. The scripts of the `MathJax CDN`_ will then be used for this purpose. If you want to use MathJax without a web connection, you need to install it on the computer that needs to display your mathematical expressions. It should be installed in the directory: ``< SLiCAP_INSTALLPATH >/MathJax-latest/``. In that case you also need to change the setting of ``MATHJAXLOCAL`` to ``TRUE``. The best performance is obtained if you also install the MathJax fonts on your computer. 

For proper rendering of equations you need to have JavaScript enabled in your browser.

.. _MathJax CDN: https://www.mathjax.org/

Digits for calculation
----------------------

You can set the number of digits for floating point calculation by changing the value of ``CALC``. Its default value is 20. This number is only used after a number has been converted from a rational to a float. MuPAD® calculates in rationals with a very high precision.

Digits for displaying
---------------------

You can change the number of digits for displaying floating point numbers by changing the value of DISP. This number defaults to 4. 

Global parameters
-----------------

SLiCAP has a number of built-in parameters. These parameters and their definitions are collected in the ``GLOBAL_DEFS`` list of variables.

You can change the values of these parameters or add other global parameters and their definitions to this list. The built-in parameters are described in the table below:

.. csv-table:: SLiCAP built-in parameters
    :header: "name", "Description", "symbol", "value", "units"
    :widths: 20, 40, 10, 20, 10

    "F", "Frequency", :math:`F`, , "Hz"
    "k", "Boltzmann constant", :math:`k`, :math:`1.38064852{\cdot}10^{-23}`, "J/K"
    "q", "Unit charge", :math:`q`, :math:`1.60217662{\cdot}10^{-19}`, "C"
    "T", "Ambient temperature", :math:`T`, :math:`300`, "K"
    "c", "Speed of light", :math:`c`, :math:`2.9979245{\cdot}10^8`, "m/s"
    "mu_0", "Permeability of vacuum", :math:`{\mu_0}`, :math:`4{\pi}{\cdot}10^{-7}`, "H/m"
    "epsilon_0", "Permittivity of vacuum", :math:`{\epsilon_0}`, :math:`\frac{1}{c^2{\mu_0}}`, "F/m"
    "epsilon_SiO2", "Relative permittivity of SiO2", :math:`{\epsilon_{\mathrm{SiO_2}}}`, :math:`3.9`,
    "U_T", "Thermal voltage", :math:`U_T`, :math:`\frac{kT}{q}`, "V" 

These parameters are used in subcircuits in the ``slicap.lib`` library file. The parameter ``F`` is used in noise analysis. You can add global parameters in the ``GLOBAL_DEFS`` list. Deleting or changing existing parameter definitions may result in errors.

Path settings
-------------

Below the list of path settings:

#. CIRPATH

   By default, SLiCAP looks for circuit files (.asc, .sch, .net and .cir) in the project directory. This search path is defined by the variable CIRPATH. Its value can be modified: use forward slashes and terminate the path string with a forward slash '/' as shown in the example below.

.. code-block:: mupad

   
    CIRPATH      := "cir/": // Search path for schematics and netlist files:
                            // (.asc, .cir, .net, sch).
   
#. TXTPATH: sets the path for text files to be included on the HTML page (file2html.m).
#. CSVPATH: sets the path for .csv files to be included on the HTML page (csv2html.m).
#. IMGPATH: sets the path for image files to be included on the HTML page (img2html.m).

--------------
Way of working
--------------

The preferred way of working with SLiCAP is:

1. For each project create a project file. 
2. From that file you call scripts in the project directory that perform the actual analysis. 

Hence, you always execute the project file. This will properly update all html output files.

The project file has the following structure:

.. code-block:: matlab
    
    clear all;
    initProject('myProject', mfilename('fullpath'));
    scriptFile1();
    scriptFile2();
    .
    .
    .
    stophtml();  % This closes the project index page with a foottext and proper HTML tags.
    % Uncomment the last line if you have python-sphinx
    % with the sphinx_bootstrap_theme installed.
    % This will compile the REstructured text files into a website with navigation bars.
    
    %system('sphinx-build rst/ sphinx/'); 

A script file ``scriptFileN.m`` has the following structure:

.. code-block:: matlab

    % The following line is used for checking a netlist and converting it into matrix equations.
    checkCircuit('CircuitFileNameWithoutFileExtension'):
    % Start an HTML page for displaying results:
    htmlPage('Some title for a HTML page');
    %
    % SLiCAP and MATLAB instructions
    %
    % Close the current HTML with a foottext and proper HTML tags and start a new one:
    htmlPage('A title for a new HTML page') 
    %
    % SLiCAP and MATLAB instructions
    %
    stophtml();  % This closes the last HTML with a foottext and proper HTML tags.

------------
Getting Help
------------

Help is offered in three ways:

    1. Type 'Help' in the Matlab Command Window will display the HTML documentation in your browser.
    2. Type 'help' < functionName > in the Matlab Command Window will display help information for a specific function in the Matlab Command Window.
    3. Search the SLiCAP forum and/or open a new discussion.
