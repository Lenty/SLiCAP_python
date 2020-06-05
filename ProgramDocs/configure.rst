====================
SLiCAP configuration
====================

SLiCAP uses several configuration files. 

Basic user configuration
========================

A user configuration file will be created in the project directory by initPtoject(). 
Once created it can be modified and modifications will not be overwritten by initProject().

- Symbols for frequency, angular frequency and Laplace variable
- Number of recursive substitutions in expressions
- Number of digits for float display
- Frequency output in [Hz] or in [rad/s]
- Path settings
- Plot settings

These settings are in the file: ``SLiCAPconfig.py``:

.. literalinclude:: ../SLiCAPconfig.py
    :language: python
    :linenos:

Basic SLiCAP configuration
==========================

- Import of python modules
- Detection of install path
- Detection of project path
- Some type conversions for user-defined constants

These settings are in the file: ``SLiCAPini.py``:

.. literalinclude:: ../SLiCAPini.py
    :language: python
    :linenos:

After this file has been copied to the project directory, product data will be added.
An example of product data is shown below. The variable LASTUPDATE will be updated by initProject().

.. code:: python

    # Project information
    PROJECT    = 'My first SLiCAP project'
    AUTHOR     = 'anton'
    CREATED    = '2020-06-04 16:17:06.407070'
    LASTUPDATE = '2020-06-04 17:02:35.948693'

Change or add built-in models and devices
=========================================

- DEVICES: built-in devices
- MODELS: built-in models
- HIERARCHY: Last-in first-out list for checking hierarchical loops in nested circuits

Built-in devices, models and parameters are found in the file: ``SLiCAPprotos.py``:

.. literalinclude:: ../SLiCAPprotos.py
    :language: python
    :linenos:
