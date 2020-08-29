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


Requirements
------------

Before installing SLiCAP you need to install `maxima CAS <http://maxima.sourceforge.net/download.html>`_.

Install SLiCAP
--------------

.. code-block:: python

   pip install slicap

------------------------
Configure SLiCAP options
------------------------

You can configure SLiCAP options after you have created a project. To this end you create a python file 
in a project directory. The minimum content of this file is:

.. code python::

   # import the SLiCAP modules
   from SLiCAP import *
   # Create a SLiCAP project, this creates the driectory structure
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

SLiCAP has a number of built-in parameters. These parameters are defined in the ``SLiCAPmodels.lib`` library file.
You can define other global parameters by adding SPICE .param declarations.

.. literalinclude:: ../../lib/SLiCAPmodels.lib
    :language: text
    :linenos: 
    :lines: 1-54
    :lineno-start: 1

Path settings
-------------

The project path setting are defined in the file **SLiCAPconflig.py**. This file is created in the project directory the by **initProject()**. Once created, it can be edited to modify the path settings. The default values are:

.. literalinclude:: ../../SLiCAPconfig.py
    :language: python
    :linenos:
    
SLiCAP configuration parameters
-------------------------------

The configuration parameters for SLiCAP are described in `SLiCAPini.py <../reference/SLiCAPini.html#module-SLiCAPini>`_.

To list the values of the SLiCAP configuration parameters enter:

.. code:: python

   >>> ini.dump()

------------
Getting Help
------------

For help open the ``doc/index.html`` file in the SLiCAP install path. 
