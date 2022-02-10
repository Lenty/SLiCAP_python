===========================
Initialize a SLiCAP project
===========================

You start SLiCAP by importing of the scripts and initialization of a python project:

.. code-block:: python

    >>> from SLiCAP import * # This imports the SLiCAP scripts
    >>> prj = initProject('My SLiCAP project')

The function ``initProject<projectName>`` creates the (missing parts) of the directory structure in the working directory. Directories once created will not be overwritten. 

The settings are stored in the `ini()` object. You can view these settings by entering:

.. code-block :: python

    >>> ini.dump()
    Hz................ : True
    Laplace........... : s
    MaximaMatrixDim... : 25
    MaximaTimeOut..... : 5
    circuitPath....... : /home/anton/SLiCAP/Project/cir/
    csvPath........... : /home/anton/SLiCAP/Project/csv/
    defaultColors..... : ['r', 'b', 'g', 'c', 'm', 'y', 'k']
    defaultLib........ : /home/anton/SLiCAP/lib
    defaultMarkers.... : ['']
    disp.............. : 4
    docPath........... : /home/anton/SLiCAP/docs
    factor............ : False
    figureAxisHeight.. : 5
    figureAxisWidth... : 7
    figureFileType.... : svg
    frequency......... : f
    gainColors........ : {'gain': 'b', 'asymptotic': 'r', 'loopgain': 'k', 'direct': 'g', 'servo': 'm', 'vi': 'c'}
    htmlIndex......... : index.html
    htmlLabels.keys(). : []
    htmlPage.......... : 
    htmlPages......... : ['index.html']
    htmlPath.......... : /home/anton/SLiCAP/Project/html/
    htmlPrefix........ : 
    imgPath........... : /home/anton/SLiCAP/Project/img/
    installPath....... : /home/anton/.local/lib/python3.8/site-packages/SLiCAP/
    lastUpdate........ : 2021-03-23 13:28:34.371803
    latexPath......... : /home/anton/SLiCAP/Project/tex/
    legendLoc......... : best
    libraryPath....... : /home/anton/SLiCAP/Project/lib/
    ltspice........... : /home/anton/.wine/drive_c/Program Files/LTC/LTspiceXVII/XVIIx64.exe
    mathml............ : False
    mathmlPath........ : /home/anton/SLiCAP/Project/mathml/
    maxRecSubst....... : 12
    maxSolve.......... : True
    maxima............ : maxima
    netlist........... : lepton-netlist -g spice-noqsi
    normalize......... : True
    notebook.......... : True
    plotFontSize...... : 12
    projectPath....... : /home/anton/SLiCAP/Project/
    simplify.......... : False
    stepFunction...... : True
    tableFileType..... : csv
    txtPath........... : /home/anton/SLiCAP/Project/txt/

Below the meaning of the variables.

Hz
--

#. True:

   - The functions: findServoBandwidth(), listPZ and pz2html will return/display poles and zeros in [Hz]. 
   - Frequency domain plots will have the frequency scale in [Hz].
   - Pole-zero plots will have the frequency scale in [Hz].

#. False: the functions: findServoBandwidth(), listPZ and pz2html will return/display poles and zeros in [rad/s]. 

**Default value** is *True*

Execution results of poles and zeros analysis are always in [rad/s].

Noise spectra always have the frequency scale in [Hz].


Laplace
-------

Sympy symbol that will be used as Laplace variable.

**Default value** is s

MaximaMatrixDim
---------------

Maximum number of rows or columns of the MNA matrix for which *maxima CAS* will use the *Gentleman-Johnson* method for determination of the determinant. Above this number *maxima CAS* is forced to use *recursive expansion of minors*.

**Default value** is 25

MaximaTimeOut
-------------

Many symbolic and numeric math functions are performed by *maxima CAS*. Currently the python subprocess module is used for this purpose. If for some reason *maxima CAS* required input that cannot be passed to this subprocess, the execution of this subprocess is times out after ``MaximaTimeOut`` seconds. 

**Default value** is 5 seconds

circuitPath
-----------

Search path for schematic files and netlist files. 

**Default value** is defined in *SLiCAPconfig.py* in the project directory.

It will be used by:

#. SLiCAPinstruction.instruction.checkCircuit(<netlist file name>)
#. SLiCAPinstruction.instruction.setCircuit(<netlist file name>)
#. SLiCAPprotos.circuit.checkCircuit(<netlist file name>)
#. SLiCAP.makeNetlist(<schematics file name>, <circuit title>)
#. SLiCAPhtml.netlist2html(<netlist file name>)

csvPath
-------

Search path for csv files.

**Default value** is defined in *SLiCAPconfig.py* in the project directory.

It will be used by:

#. SLiCAP_html.csv2html(<csv file name>)
#. SLiCAP_plots.csv2traces(<csv file name>)

defaultColors
-------------

List with matplotlib color names that will be used for plotting multiple graphs on one axis.

**Default value** is ['r', 'b', 'g', 'c', 'm', 'y', 'k'].

defaultLib
----------

Search path for system library files with SPICE definitions of sub circuits and models.

**Default value** is determined during installation.

defaultMarkers
--------------

List with matplotlib marker names to be used in plots.

**Default value** is: ['']

disp
----

Number of digits for displaying floats on html pages.

**Default value** is: 4

docPath
-------

Path to the SLiCAP html documentation

**Default value** is determined during installation.

factor
------

Setting for factorization of expressions.

**Default value** is False

figureAxisHeight
----------------

Height of a figure object (depends on DPI).

**Default value** is 5

figureAxisWidth
---------------

Width of a figure object (depends on DPI).

**Default value** is 7

figureFileType
--------------

File type for saving matplotlib figures (graphs).

**Default value** is *svg* (scalable vector graphics).

frequency
---------

Sympy symbol used for frequency.

**Default value** is *f*.

gainColors
----------

Dictionary with agin types and associated colors for plotting.

**Default value** is *{'gain': 'b', 'asymptotic': 'r', 'loopgain': 'k', 'direct': 'g', 'servo': 'm', 'vi': 'c'}*.

htmlIndex
---------

Active html index page. Links to new pages created with *htmlPage()* will be placed on this page.

**Default value** directly after initialization of a project is *index.html*.

htmlLabels.keys()
-----------------

Keys of the dictionary with html labels that have been defined in this project.

**Default value** is [].

htmlPage
--------

Active html page to which html output will be written.

**Default value** is ''.

htmlPages
---------

List with html pages created in this project.

**Default value** directly after initialization of a project is ['index.html'].

htmlPath
--------

Path to the html output generated by this project.

**Default value** is defined in *SLiCAPconfig.py* in the project directory.

htmlPrefix
----------

Prefix that will be added to the html page file names. This string consists of the netlist file name + '_'.

**Default value** directly after initialization of a project is ''.

imgPath
-------

Search path for img2html().

**Default value** is defined in *SLiCAPconfig.py* in the project directory.

installPath
-----------

SLiCAP install path.

**Default value** is determined during installation.

lastUpdate
----------

Last date/time of execution of the project.

**Default value** is the date time directly after initialization of the project.

latexPath
---------

Path for exporting LaTeX output (not used in current version).

**Default value** is defined in *SLiCAPconfig.py* in the project directory.

legendLoc
---------

Location of legend on plots.

**Default value** is *best*.


libraryPath
-----------

Path to user libraries with definitions of sub circuits and models.

**Default value** is defined in *SLiCAPconfig.py* in the project directory.

ltspice
-------

Path to LTspice executable (required for makeNetlist().

**Default value** is automatically determined during installation.

mathml
------

Setting for math output in html pages (not yet implemented)

**Default value** is *False*.

mathmlPath
----------

Path for exporting mathml output (not used in current version).

**Default value** is defined in *SLiCAPconfig.py* in the project directory.

maxRecSubst
-----------

Setting for maximum number of recursisve substitutions.

**Default value** is 12.

maxSolve
--------

Setting for using maxima CAS for finding the complete network solution.

**Default value** is *True*.

maxima
------

Command for running maxima CAS.

**Default value** is determined during installation.

netlist
-------

Command for generating a netlist from a '.sch' schematic file.

**Default value** is determined during installation.

normalize
---------

Setting for normalization of rational functions. If *True*, the coefficient of the lowest order of the denominator will be normalized to unity.

**Default value** True

notebook
--------

Will be set to *True* if SLiCAP runs from an ipython environment (some additional scripts will be loaded).

**Default value** is *False*.

plotFontSize
------------

Font size used in plots.

**Default value** is 12.

projectPath
-----------

Path to the project files for the current project.

**Default value** is determined during the initialization of a project.

simplify
--------

Setting for simplifying expressions.

**Default value** is *False*.

stepFunction
------------

Setting for parameter stepping.

#. True

   The determinant of a matrix is calculated using symbolic step variable(s). 

#. False

   Numeric values of step variable(s) are substituted in the metrices before calculation of the determinant. This can be faster if many step variables are used.


**Default value** is *True*.


tableFileType
-------------

File extension for *comma seperated value* table files.

**Default value** is *csv*.

txtPath
-------

Search paths for importing text files with text2html().

**Default value** is defined in *SLiCAPconfig.py* in the project directory.

