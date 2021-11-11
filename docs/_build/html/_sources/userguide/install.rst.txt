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

SLiCAP is licensed under a `Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License <http://creativecommons.org/licenses/by-nc-nd/4.0/>`_. Based on a work at: `http://www.analog-electronics.eu/slicap/slicap.html <http://www.analog-electronics.eu/slicap/slicap.html>`_

Requirements
------------

Before installing SLiCAP you need to install `maxima CAS <http://maxima.sourceforge.net/download.html>`_ and Python 3 packages listed in `https://github.com/Lenty/SLiCAP_python/requirements.txt <https://github.com/Lenty/SLiCAP_python/blob/master/requirements.txt>`_.

MacOS installation of maxima
````````````````````````````
#. Install maxima on macOs using the *homebrew* package manager (see `brew.sh <https://brew.sh/>`_ for installation instructions)
#. Install maxima with homebrew: open a terminal and enter: *brew install maxima*. 

Download SLiCAP
---------------

- Open a command window or terminal in a folder where you want to store the downloaded files and clone `https://github.com/Lenty/SLiCAP_python <https://github.com/Lenty/SLiCAP_python>`_ into that folder:

.. code-block:: bash

   git clone https://github.com/Lenty/SLiCAP_python

or 

- Download the zip file from: `https://github.com/Lenty/SLiCAP_python <https://github.com/Lenty/SLiCAP_python>`_ and extract it in some folder.


Install SLiCAP
--------------

- If you work with Anaconca open the *Anaconda Prompt* 

  - You need to have the module `in_place <https://anaconda.org/conda-forge/in_place>`_ installed.

- If you have python installed under Windows, open a terminal by running the command *cmd*
- If you have python installed under Linux or mac Open a *terminal*

#. Go to the folder with the file *setup.py* (usually: *<where_you_downloaded_or_cloned>/SLiCAP_python-master/)* and enter the command:

.. code-block:: python

   python setup.py install --user

#. Enter the requested directory paths or accept the defaults.

------------------------
Configure SLiCAP options
------------------------

You can configure SLiCAP options after you have created a project. To this end you create a python file 
in some project directory. The minimum content of this (python) file is:

.. code-block:: python

   # import the SLiCAP modules
   from SLiCAP import *
   # Create a SLiCAP project, this creates the folder structure
   # and compiles the libraries.
   my_project = initProject('my_firstSLiCAP_project')

You can modify the directory structure and update the paths for circuit files, library files, etc in the
``SLiCAPconfig.py`` file, which is created in the project directory.

MathJax
-------

SLiCAP uses MathJax to render LaTeX embedded in html. LaTeX is used for expressions. MathJax rendering of equations requires an Internet connection. The scripts of the `MathJax CDN`_ will then be used for this purpose. For proper rendering of equations you need to have JavaScript enabled in your browser.

.. _MathJax CDN: https://www.mathjax.org/

Global parameters
-----------------

SLiCAP has a number of built-in parameters. These parameters are defined in the ``SLiCAPmodels.lib`` library file in the ``lib/`` folder
You can define other global parameters by adding SPICE .param declarations in this file.

.. literalinclude:: ../../files/lib/SLiCAPmodels.lib
    :language: text
    :linenos: 
    :lines: 1-54
    :lineno-start: 1

Path settings
-------------

The project path settings are defined in **SLiCAPconflig.py**. This file is created in the project directory the by **initProject()**. Once created, it can be edited to modify the path settings. **initProject()** will not overwrite the existing **SLiCAPconflig.py**. If you want it to be regenerated, simply delete it before running **initProject()**. 

The default values are:

.. literalinclude:: ../../SLiCAP/SLiCAPconfig/SLiCAPconfig.py
    :language: python
    :linenos:
    
SLiCAP configuration parameters
-------------------------------

The configuration parameters for SLiCAP are defined in `SLiCAP.SLiCAPini.py <../reference/SLiCAPini.html#module-SLiCAPini>`_.

To list the values of the SLiCAP configuration parameters enter:

.. code:: python

   >>> ini.dump()

------------
Getting Help
------------

For help open the ``index.html`` in the ``doc/`` folder in the SLiCAP main library path that you have selected during installation. 

If you are working in a python IDE or in a jupyter notebook, use the *Help()* function (with capital **H**).

.. code:: python

   >>> Help() # This will open the HTML documentation in your default web browser.

-----------------
Schematic capture
-----------------

SLiCAP accepts SPICE-like netlists. Many schematic capture programs can be configured to generate such netlists. SLiCAP comes with symbol libraries for *LTspice*, *gSchem* and its fork *lepton-eda*.

The syntax that should be used for composing SLiCAP netlists is described in the `Device Models <../syntax/netlist.html#devices-and-built-in-models>`__ section. 

LTspice
-------

**LTspice** can be used for netlist generation. LTspice works with Windows and Linux (under Wine). A version for MAC is also available. Go to `LTspice <http://www.linear.com/designtools/software>`_ for the latest version.

For an overview of SLiCAP symbols for LTspice, please view the `LTSpice <../syntax/schematics.html#LTSpice>`__ section. 

**Configure LTspice for use with SLiCAP**

SLiCAP circuits should be made with SLiCAP symbols (and not with the default LTspice symbols). LTspice symbols for SLiCAP are placed in the ``LTspice/`` folder in the SLiCAP main library path that you have selected during installation. 

#. Start LTspice
#. On the menu bar click ``Tools > Control Panel``. This will bring up the LTspice control panel:

   .. image:: ../img/LTspiceControlPanel.png

#. On this control panel select the ``Netlist Options`` tab and select the options as shown below:

   .. image:: ../img/LTspiceControlPanelNetlistOptions.png

#. Then select the ``Sym. & Lib. Search Paths`` tab and enter the full path to the ``LTspice/`` folder of your SLiCAP install path. This directory contains all the SLiCAP symbol definitions ('.asy' files) for LTspice:

   .. image:: ../img/LTspiceControlPanelSymbolPath.png

#. Then select the ``Drafting Options`` tab and change the font size and deselect the "Bold" checkbox as shown below. If you want, you can also select different colors for your schematics.

   .. image:: ../img/LTspiceControlPanelFontSettings.png


Gschem
------

The open source **gschem** package can also be used in conjunction with SLiCAP. SLiCAP symbols for gschem are included in the ``gSchem/symbol/`` folder in the SLiCAP main library path that you have selected during installation.

For an overview of SLiCAP symbols for gSchem, please view the `gSchem <../syntax/schematics.html#gSchem>`__ section. 

The **gnet-spice-noqsi** spice netlister should be used for netlist generation. SLiCAP has a built-in instruction for netlist generation with gschem and this netlister. 

The use of gschem as front-end for SLiCAP has been tested under Linux and under Windows. 

**Linux installation**

Under Linux you can install it with the package manager. Please visit `gEDA <http://www.geda-project.org>`_ for more information. In some Linux distributions gschem may be replaced with lepton-eda.

The spice netlister for gschem can be found in the ``gSchem/gnet-spice-noqsi-master/`` folder in the SLiCAP main library path that you have selected during installation.

Linux installation of gschem and the gnet-spice-noqsi is well documented and straightforward. 

After installation of gschem you need to create or modify the file: ``.gEDA/gafrc`` in your home directory with the contents:

.. code-block:: python

    (reset-component-library)
    (component-library "<path to SLiCAP symbol Library>" "SLiCAP")

If you wish to have a light background you can create or modify the file ``.gEDA/gschemrc`` in your home directory with the contents:

.. code-block:: python

    (load (build-path geda-rc-path "gschem-colormap-lightbg")) ; light background

**Windows installation**

A windows installer for gschem can be downloaded from: `gEDA-20130122.zip <http://bibo.iqo.uni-hannover.de/dokuwiki/doku.php?id=english:geda_for_ms-windows>`_.

Windows installation of gschem is straightforward: simply extract the ``gEDA-20130122.zip`` file and run the Windows installer. In the drop down menu of the "Select Components" dialog box select "Program only", for the rest accept default settings.

The spice netlister for gschem can be found in the ``gSchem/gnet-spice-noqsi-master/`` folder in the SLiCAP main library path that you have selected during installation.

The netlister is installed by copying the file ``gnet-spice-noqsi.scm`` from the extracted ``gnet-spice-noqsi.zip`` to: ``C:\Program Files (x86)\gEDA\gEDA\share\gEDA\scheme\gnet-spice-noqsi``.

You need to create or modify the file ``gafrc`` in the ``C:\Users\<userName>\.gEDA\`` directory. It should have the following content:

.. code-block:: python

    (reset-component-library)
    (component-library "C:/Program Files (x86)/gEDA/gEDA/share/gEDA/sym/slicap")
    
The component library is found in the in the ``gschem/symbols/`` folder in the SLiCAP install path. Create a directory ``C:\Program Files (x86)\gEDA\gEDA\share\gEDA\sym\slicap`` and copy the component library to this directory.
    
If you wish to have a light background you can create or modify the file ``gschemrc`` in the ``C:\Users\<userName>\.gEDA\`` directory. Its contents must be:

.. code-block:: python

    (load (build-path geda-rc-path "gschem-colormap-lightbg")) ; light background

Be sure you save these two files ``gafrc`` and ``gschemrc`` without any file extension.

Lepton-eda
----------

Lepton-eda is a fork of geda-gaf. Please visit `https://github.com/lepton-eda/lepton-eda <https://github.com/lepton-eda/lepton-eda>`_ for more information.

SLiCAP symbols for lepton-eda are included in the ``lepton-eda/`` folder in the SLiCAP main library path that you have selected during installation.

For an overview of SLiCAP symbols for lepton-eda, please view the `gSchem <../syntax/schematics.html#gSchem>`__ section in the help file. 

After installation of lepton-eda you need to create or modify the file: ``.config/lepton-eda/gafrc`` in your home directory with the contents:

.. code-block:: python

    (reset-component-library)
    (component-library "<path to SLiCAP symbol Library>" "SLiCAP")

If you wish to have a light background, you can create or modify the file ``.config/lepton-eda/gschemrc`` in your home directory with the contents:

.. code-block:: python

    (load (build-path geda-rc-path "gschem-colormap-lightbg")) ; light background

Be sure you save these two files ``gafrc`` and ``gschemrc`` without any file extension.

The **gnet-spice-noqsi** spice netlister should be used for netlist generation. SLiCAP has a built-in instruction for netlist generation with lepton-eda and this netlister. 

The spice netlister for lepton-eda can be found in the ``lepton-eda/gnet-spice-noqsi-master/`` folder in the SLiCAP main library path that you have selected during installation.

For compact node names (important for use in symbolic expressions) you need to reconfigure the default *net name prefix*.

This is how it should be done under Ubuntu-based Linux systems:

.. code:: bash

    sudo lepton-cli config --system "netlist" "default-net-name" ""

Display schematics on html pages
--------------------------------

With **LTspice** you can print schematics to a .PDF file using a PDF printer.

With **gschem** running under **MSwindows** you can write your schematic file to a .PDF file.

For proper display of schematics on html pages these .PDF files need to be be converted to .SVG files, you can use `pdf2svg <https://github.com/jalios/pdf2svg-windows>`_ for this purpose. Under Linux and Mac OS you need to install 'psd2svg' to make this work.

With **gschem** running under **Linux** or **Mac OS** you can write your schematic file to a .EPS file.

.EPS files can be converted into .PDF files using the `epstopdf <https://www.systutorials.com/docs/linux/man/1-epstopdf/>`_ command. 

Ghostscript is often available in the package manager of Linux distributions. Otherwise Ghostscript versions can be downloaded from: `Ghostscript <https://ghostscript.com/download>`_. 

With **lepton-eda** running under **Linux** you can print to pdf or svg.

Inkscape .svg editor
--------------------

When printing a schematic from LTspice with a PDF printer, the full path of the file will be listed at the bottom of the page. After the .PDF file has been converted into a .SVG file (see above), you can use **inkscape** to edit this SVG file and delete the footer.

Inkscape runs under Windows, Linux and Mac OS. Inkscape versions can be downloaded from: `inkscape.org <https://inkscape.org/release/inkscape-1.0.1/>`_.

