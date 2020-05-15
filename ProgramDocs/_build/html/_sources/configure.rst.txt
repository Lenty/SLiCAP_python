====================
SLiCAP configuration
====================

Basic user configuration
========================

- Symbols for frequency, angular frequency and Laplace variable
- Number of recursive substitutions in expressions
- Number of digits for float display
- Frequency output in [Hz] or in [rad/s]
- Path settings
- Plot settings

These settings are in the file: ``SLiCAPini.py``:

.. literalinclude:: ../SLiCAPini.py
    :language: python
    :linenos:

Change or add built-in models and devices
=========================================

- DEVICES: built-in devices
- MODELS: built-in models
- HIERARCHY: Last-in first-out list for checking hierarchical loops in nested circuits

Built-in devices, models and parameters are found in the file: ``SLiCAPprotos.py``:

.. literalinclude:: ../SLiCAPprotos.py
    :language: python
    :linenos:
