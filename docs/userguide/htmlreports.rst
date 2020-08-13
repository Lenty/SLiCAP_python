=====================
Generate HTML reports
=====================

Writing design documentation is often something that needs to be done after the design work has been finished. By then, all kinds of information needs to be collected and structured in a document, while in many cases new projects are already taking most of the time. This undesirable but almost always inevitable practice can be prevented if the design work goes hand in hand with generation of the design documents. SLiCAP supports this with the generation of web-based design documentation in which figures, tables, expressions and ASCII files can be updated while running SLiCAP-MATLAB scripts. In this way, presentations and documentation can be kept up to date with the actual status of the design.

.. _html:

-------------------
HTML site structure
-------------------

The structure of the project web site that can be generated with SLiCAP will be discussed below.

Main Index.html
---------------

Initialization of a project generates an ``index.html`` file in the ``html`` subdirectory. This file will hold the main table of contents of your project. Each time you check a circuit netlist that resides in the project directory, a list entry will be generated in this index file. 

Below the preferred way of working if you have SLiCAP-MATLAB installed in ``/home/myName/SLiCAP/`` and your work needs to be stored in the project directory ``/home/myName/myProject/``. The script below should be executed in this project directory.

.. code-block:: matlab

    % move to the project directory (here: '/home/myName/SLiCAP/')
    cd /home/myName/SLiCAP/
    % Clear the MATLAB and the symbolic toolbox environment
    clear all;
    %
    % Initialize a project (here: 'myProject') in this directory 
    initProject(myProject', mfilename);
    %
    % Here you can put your SLiCAP-MATLAB instructions
    % ...
    %
    % Close the index.html file properly
    stophtml();

Circuit index file
------------------

Each time you check a circuit as described in: ':ref:`checkCircuit`', the following will happen (assume the name of the netlist file is ``circuitName.cir``:

- A file ``circuitName_index.html`` will be created. This file will hold the table of contents of the html pages for this circuit.
- A file ``circuitName_log.html`` will be created and a link to this file will be created in the ``circuitName_index.html`` file.
- A link to the ``circuitName_index.html`` file will be created in the main ``index.html`` file that was created at the initialization of the project. 

A good practice is to start a new active html page after checking the circuit, this prevents output to be writen to index files which would mess up the table of contents.

---------------------
Start a new html page
---------------------

A new html page can be created by evoking the command ``htmlPage(< pageTitle >)``, in which ``pageTitle`` is the title of the new page (character string). The following will occur:

1. The current active html page will be closed with the correct html tags.
2. A html page with the file name: ``< circuitName >_< pageTitle >.html`` in which ``circuitName`` is the name of the circuit will be created.
3. It makes this new page the active html page
4. It places a top-level page heading (H1) with ``pageTitle`` on this page

The return value of ``htmlPage('pageTitle')`` is the character string:
    
.. code-block:: html

    <h1>pageTitle</h1>

The example below shows the initialization of SLiCAP, the checking of myCircuit and the generation of a page for the netlist. In this example we assume that a project has been created and the working directory is the project directory.

.. code-block:: matlab

    clear all
    slicap()
    makeNetlist('myCircuit')
    numberOfErrors = checkCircuit('myCircuit');
    htmlPage('Netlist');
    netlist2html('myCircuit');
    htmlPage('AlmostEmpty');
    text2html('This page is almost empty!');
    stophtml();

The ``stophtml()`` instruction closes the last active html page and the index page for this circuit with the correct html tags.

--------
Headings
--------

Sub headings (level 2 and level 3) can be placed on the active html page. 

H2
--

The function ``head2html(< level2heading >)`` places the character string ``level2heading`` in H2 format on the active html page.

.. code-block:: matlab

    head2html('Schematics of the circuit');

H3
--

The function ``head3html(< level3heading >)`` places the character string ``level3heading`` in H3 format on the active html page.

.. code-block:: matlab

    head3html('Schematics of the sub circuit myOpamp');


-----------------
List element data
-----------------

The function ``elementData2html()`` displays all the data of the elements of the expanded netlist in a table on the active html page.

.. code-block:: html

    elementData2html();

-------------------
List parameter data
-------------------

The function ``params2html()`` displays the symbolic and the numeric values of all parameters in your circuit.

.. code-block:: html

    params2html();

------------------
Include ASCII file
------------------

You can include an ASCII file with or without html tags and with or without LaTeX, literally in your active HTML page.

.. code-block:: matlab

    file2html('myTextFile.ascii');

In-line LaTeX expressions should be placed between single dollar characters: ``$ < myLaTeXexpression > $``. Displayed LaTeX expressions should be placed between double dollar characters: ``$$ < myLaTeXexpression > $$``.

---------------
Include netlist
---------------

You can include a netlist file on the active html page. Line breaks of the input file will be copied to the html file. You should not include the netlist file extension in the file name.

.. code-block:: matlab

    netlist2html('myCircuit');

---------------------
Include MATLAB script
---------------------

A MATLAB script file can be converted into a html page using the function:

.. code-block:: matlab

    script2html(< MATLABmFile >)
		
In which ``MATLABmFile`` is the name of the MATLAB script file (excluding the file extension ``.m``) that resides in the project directory. This function generates a html file with the name ``< circuitName >_< MATLABmFile >.html``, and places a link on the < ``< circuitName >_index.html`` page. It does not change the name of the active html page. LaTeX in the MATLAB script file will not be typeset. The script is displayed in the browser as in the MATLAB editor.

Assume the MATLAB script file ``hfAnalysis.m`` with the contents given below and the circuit netlist ``myCircuit.cir`` are both stored in the project directory. The script below then creates an html file ``myCircuit_hfAnalysis.m.html`` in the project directory.

.. code-block:: matlab

    clear all;
    slicap()
    numberOfErrors = checkCircuit('myCircuit');
    script2html('hfAnalysis');

------------------------
Include images and plots
------------------------

Images from files
-----------------

You can include images into your html file by using the function:

.. code-block:: matlab

    img2html( < figureFileName >, < widthInPixels >);

The width of the image is scaled to widthInPixels (the aspect ratio will be maintained). The graphic file should reside in the work/html/SLiCAP-MATLAB/figures/ directory.

MATLAB figures
--------------

Plots generated by MATLAB can be placed on the active html page by using the function:

.. code-block:: matlab

    fig2html(< MATLABfigureObject >, < fileName >, < widthInPixels >)

1. `MATLABfigureObject` is a MATLAB figure as it has been generated with one of the SLiCAP plot functions
2. `fileName` is the name of the graphic file in which the figure will be stored, including a html compatible extension. The figure file will be stored in the work/html/SLiCAP-MATLAB/figures/ directory.
3. `widthInPixels` sets the width of the figure in the html page. The aspect ratio will be maintained.

.. code-block:: matlab

    img2html('myCircuit.svg', 600);

The variable ``myFig`` in the example below is a MATLAB figure object containing the step response of a circuit. It will be displayed on an HTML page and included in the html/figures/ subdirectory of the project.

.. code-block:: matlab

    fig2html(myFig, 'stepResponse.svg', 600);

The function returns the MuPAD boolean TRUE if the file is found, else FALSE.

-----------------------------
Include tables from CSV files
-----------------------------

Comma Separated Values files can be displayed as a table on the active HTML page using the function ``csv2html.m``. The CSV file may comprise LaTeX expressions. The example below shows how a CSV file ``transimpedanceSpec.csv`` with specifications of a transimpedance amplifier is displayed on the active html page.

.. code-block:: matlab

    csv2html('transimpedanceSpec') % File extension is '.csv' and should not be included

The file ``transimpedanceSpec.csv`` has been listed below.

.. code-block:: text

    symbol,description,value,units
    $C_{s}$,Sensor capacitance,10...20,pF
    $I_{D}$,Sensor dark current,20...50,nA
    $I_{peak}$,Peak signal current of sensor,20,$\mathrm{\mu A}$
    $\left( \frac{dI}{dt} \right)_{max}$,Max rate of change sensor current,100,A/s
    $R_{\ell}$,Load resistance,1 $\cdots \infty$, $\mathrm{k \Omega}$
    $C_{\ell}$,Load capacitance,0...100,pF
    $V_{\ell}$,Peak signal voltage across load,2,V
    $V_{onoise}$,Maximum RMS noise voltage across load,100,$\mathrm{\mu V}$
    $V_{off}$,Maximum offset voltage across load,10,mV
    $B_{f}$,MFM -3dB cut-off frequency of transimpedance gain,1,MHz
    $\delta$,Maximum of absolute static (gain) inaccuracy,2,%

The displayed result (depends on the CSS file):

.. csv-table::
    :delim: ;
    :header: symbol, description, value, units

    :math:`C_{s}` ; Sensor capacitance; 10...20; pF
    :math:`I_{D}` ; Sensor dark current; 20...50; nA
    :math:`I_{peak}` ; Peak signal current of sensor; 20; :math:`\mathrm{\mu A}` 
    :math:`\left( \frac{dI}{dt} \right)_{max}` ; Max rate of change sensor current; 100; A/s
    :math:`R_{\ell}` ; Load resistance; 1 :math:`\cdots \infty` ;  :math:`\mathrm{k \Omega}` 
    :math:`C_{\ell}` ; Load capacitance; 0...100; pF
    :math:`V_{\ell}` ; Peak signal voltage across load; 2; V
    :math:`V_{onoise}` ; Maximum RMS noise voltage across load; 100; :math:`\mathrm{\mu V}` 
    :math:`V_{off}` ; Maximum offset voltage across load; 10; mV
    :math:`B_{f}` ; MFM -3dB cut-off frequency of transimpedance gain; 1; MHz
    :math:`\delta` ; Maximum of absolute static (gain) inaccuracy; 2; %

-------------------------
Include Pole-Zero results
-------------------------

The function ``pz2html.m`` accepts the result of a single (non stepped) pole-zero analysis with the data type equal to ``POLES`` or ``ZEROS`` or ``PZ``. It converts these results into html tables on the active html page. See examples for application and displayed results.

.. code-block:: matlab

    dataType('PZ');
    stepOff();
    pz2html(execute());

---------------------
Include noise results
---------------------

The function ``noise2html.m`` accepts the result of a single (non stepped) noise analysis and converts it into html tables on the active html page. See examples for application and displayed results.

.. code-block:: matlab

    dataType('noise');
    stepOff();
    noise2html(execute());

------------
Include text
------------

The function ``text2html.m`` can be used to write a text paragraph, including html tags, css code and LaTeX code to the active html page. In-line LaTeX expressions should be placed between single dollars signs ``$ < latexExpression > $``. Displayed LaTeX expressions should be placed between double dollars signs ``$$ < latexExpression > $$``.

The text is placed between html paragraph tags: ``<p> < text > </p>``. 

.. code-block:: matlab

    text2html(['The transfer $H(s)$ of a unity-gain, '...
    'second-order, low-pass Butterworth filter with '...
    'bandwidth $omega_n$, can be written as:']);
    
It writes this text to the active html page that will display:

    The transfer of a unity-gain, second-order, low-pass Butterworth filter with bandwidth :math:`\omega_{n}` can be written as:

-------------------
Include expressions
-------------------

SLiCAP incorporates functions to write expressions or equations in LaTeX format to the active html page. These LaTeX expressions can be rendered by any browser with the aid of MathJax. The MathJax configuration settings have been included in the html pages. MathJax CDN can be accessed when connected to the Internet. Local installation of MathJax is possible, but not yet documented. The functions for printing expressions to the active HTML page have been described below.


Include an in line expression in LaTeX format
---------------------------------------------

The function ``expr2html.m`` can be used for printing an expression to the active html page. The syntax is: ``expr2html(< expr >)``

In which ``expr`` is a symbolic expression. This function prints this expression in LaTeX format to the active html page.

.. code-block:: matlab

    syms('s', 'omega_n');
    text2html(['The transfer of a unity-gain, '...
    'second-order, low-pass Butterworth filter with '...
    'bandwidth $omega_n$, can be written as:']);
    expr2html(1/(1 + s*sqrt(2)/omega_n + s^2/omega_n^2));
    
The html output looks like:

    The transfer of a unity-gain, second-order, low-pass Butterworth filter with bandwidth :math:`\omega_n`, can be written as: :math:`\frac{1}{\frac{s^2}{{\mathrm{\omega}_{n}}^2} + \frac{\sqrt{2}\, s}{\mathrm{\omega}_{n}} + 1}`

Include a displayed and numbered equation in LaTeX format
---------------------------------------------------------

The function ``eqn2html.m`` prints an equation to the active html page. The syntax for this function is:

``eqn2html(< expr1, expr2 >)``

In which ``expr1`` and ``expr2`` are symbolic expressions. This function prints the equation ``expr1=expr2`` in LaTeX format to the active html page.

.. code-block:: matlab

    syms H(s) s omega_n H_s;
    H_s = 1/(1 + s*sqrt(2)/omega_n + s^2/omega_n^2);
    text2html(['The transfer $H(s)$ of a unity-gain, '...
    'second-order, low-pass Butterworth filter with '...
    'bandwidth $omega_n$, can be written as:']);
    eqn2html(H(s), H_s)

The result on the html page will look like:

    The transfer :math:`H(s)` of a unity-gain, second-order, low-pass Butterworth filter with bandwidth :math:`\omega_n`, can be written as:

      .. math::
          :label: myExpression
    
		  H\left(s\right)=\frac{1}{\frac{s^2}{{\mathrm{\omega}_{n}}^2} + \frac{\sqrt{2}\, s}{\mathrm{\omega}_{n}} + 1}

Include the MNA matrix equation in LaTeX format
-----------------------------------------------

The function ``matrices2html.m`` prints the MNA matrices with headers and comment to the active html page. It accepts the result of an ``execute()`` instruction with the data type set to ``MATRIX`` as argument. The function returns a copy of the html code written to the active html page.

The example below illustrates:

1. The initialization of SLiCAP
2. Checking of the netlist ``myCircuit.cir``
3. Printing of the matrices for the default gain type ``VI`` to an html page with the title 'Matrix equations'

.. code-block:: matlab

    clear all
    slicap
    numberOfErrors = checkCircuit('myCircuit');
    dataType('matrix');
    htmlPage('Matrix equations');
    matrices2html(execute());
