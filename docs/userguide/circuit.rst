================
Define a circuit
================

SLiCAP requires a SPICE-like netlist of a circuit as input. It converts a hierarchical netlist into matrix equations with the aid of the 'Modified Nodal Analysis' method.

You can generate a netlist from a schematic drawing program, or by entering it manually in an ASCII editor. 

Netlist generation for SLiCAP is supported for schematics created with:

1. 'gSchem' with the corresponding SLiCAP symbol library and the 'gnet-spice-noqsi' netlist plugin
2. 'LTSPICE' with the corresponding SLiCAP symbol library

------------------------
Create a circuit netlist
------------------------

Differences between SPICE and SLiCAP netlist
--------------------------------------------

The netlist syntax for SLiCAP slightly differs from the standard SPICE syntax. The differences are listed in the section `Netlist Syntax <../syntax/netlist.html>`_.


Automatic determination of the netlister
----------------------------------------

SLiCAP can create netlists from LTspice and from gSchem. 

Below the syntax for generation of the netlist file ``myCircuit.cir`` from the 'gSchem' schematic file ``myCircuit.sch`` or from the 'LTspice' schematic file ``myCircuit.asc`` in the project directory. The title of the circuit needs to be added separately. It will be used in the table of contents of html reports. If no title is provided, it will be set to the circuit file name.

.. code-block:: matlab

    makeNetlist('myCircuit', 'My Circuit Title'); % Title = 'My Circuit Title'
    makeNetlist('myCircuit');                     % Title = 'myCircuit'


Force the use of a netlister
----------------------------

If schematics are available both in **LTspice** and **gschem** formats, SLiCAP can be forced to use one of the two netlisters. 

Below the syntax for generation of the netlist file ``myCircuit.cir`` from the 'LTspice' schematic file ``myCircuit.asc`` in the project directory. 

.. code-block:: matlab

    makeNetlist('myCircuit', 'My Circuit Title', 'ltspice');

Below the syntax for generation of the netlist file ``myCircuit.cir`` from the 'gSchem' schematic file ``myCircuit.sch`` in the project directory. 

.. code-block:: matlab

    makeNetlist('myCircuit', 'My Circuit Title', 'gschem');

.. _checkCircuit:

----------------------------------------
Check the netlist and build the matrices
----------------------------------------

Below the syntax for checking the netlist file ``myCircuit.cir`` in the project directory and generating the matrices:

.. code-block:: matlab

    checkCircuit('myCircuit');

-------------
Library files
-------------

Similar as with Spice, definitions of sub circuits (**.subckt** .... **.ends**) and models (**.model** ... ) can be stored in library files. 

SLiCAP searches for library files in two directories. The search order is:

    1. Project directory
    2. < SLiCAP install path >/lib/
