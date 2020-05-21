==============
SLiCAP Library
==============

The SLiCAP library if found in the ``lib/`` sub directory of the SLiCAP install path.

Each library will be compiled into a circuit object (as defined in ``SLiCAPprotos.py``). For this reason libraries start with a title line and end with the ``.end`` statement.

.. literalinclude:: ../SLiCAPprotos.py
    :language: python
    :linenos:
    :lines: 19-57
    :lineno-start: 29


The library file has the format of a SLiCAP netlist file and contains:

#. The first line is the ``title line``

   This line will be the ``.title`` attribute of the compiled circuit

#. Definitions of global parameters: ``.param`` lines

   Global parameters will be found in the ``.params`` attribute of the compiled circuit

#. Definitions of models: ``.model`` lines

   These model definitions will be found in the ``.modelDefs`` attribute of the compiled circuit

#. Sub circuit definitions ``.subckt ... .ends`` lines

   These subcircuit definitions will be found in the ``.circuits`` attribute of the compiled circuit

#. The last line only carries the ``.end`` command.

Compilation of standard SLiCAP libraries is performed with the ``makeLibraries function, defined in ``SLiCAPyacc.py``.

.. literalinclude:: ../SLiCAPyacc.py
    :language: python
    :linenos:
    :lines: 703 - 736
    :lineno-start: 703

After compilation, the circuit object ``LIB`` holds all the data in a way that it can be used by the SLiCAP netlist parser.

If errors are found during the compilation of the SLiCAP libraries, checking of circuits is ignored.

User libraries
==============

Compilation of user libraries is performed before the expansion of the circuit in which the library has been defined with an ``.lib`` command. The ``addUserLibs()`` function, defined in ``SLiCAPyacc.py``.

.. literalinclude:: ../SLiCAPyacc.py
    :language: python
    :linenos:
    :lines: 738 - 786
    :lineno-start: 738
