==============
Error handling
==============

Introduction
============

For each language a dictionary with error messages will be made (key = < errorCode >, value = [< errorMessage > , (< arg1 >, < arg2 >, ...)]

The language can be set in the file ``SLiCAPini.py``:

.. literalinclude:: ../SLiCAPini.py
    :language: python
    :lines: 12

**errorCode**

Short English abbreviation of the message.

**errorMessage**

Error message

**arg1, arg2 ...**

Arguments that can be passed to the message.

During circuit checking
=======================

#. Messages, together with a cleaned-up version of the input file (built from tokens) can be printed to a log file or to Python (the notebook or editor environment). This is controlled by the option ``LOGFILE`` in the file: ``SLiCAPini.py``.

.. literalinclude:: ../SLiCAPini.py
    :language: python
    :lines: 11

#. Messages do not stop the checking. The circuit.errors attribute will be set to the number of errors.
