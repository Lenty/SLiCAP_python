=====================
SLiCAP netlist parser
=====================

Converts a SLiCAP (Spice compatible) netlist into:

- A circuit structure for Maxima
- A circuit object for MATLAB
- A circuit object for Python

Input file
==========

The input file consists of a title line, a collection of netlist lines and instructions. **SLiCAP netlist input is case sensitive!**

- The first line of the input file is the title_ of the circuit.
- The first non-whitespace character of an `element definition`_ line. 
- The last line is the line with the '.end' instruction.

Type and order of file lines
----------------------------

#. The first line is a the title_ of the circuit.
#. A line starting with a dot '.' is an instruction line.
#. A '.end'. instruction line ends the circuit definition. Lines followinh this line will be ignored.
#. Lines between a line that starts with the '.subckt' instruction and a line that starts with '.ends' instruction, describe a sub circuit within the circuit or a sub circuit. Such lines can be of any type except '.end' '.inc...' and '.lib ...'.
#. Lines starting with '*' are comment lines.
#. Parts of a line that follow ';' are considered comment.
#. Lines starting with '+' are extensions of the previous line (without the '+"' itself).
#. Lines of which the first non-whitespace charachter is not '*', ';', '.' or '+' are `element definition`_ lines

Description syntax
------------------

The following syntax is used in the description of netlist lines:

- < placeHolder >
- ( contents should be enclosed in brackets )
- { contents should be enclosed in curly brackets }
- [ optional ]
- ... more of the preceeding

.. _title:

Circuit title
-------------

The first line is a the title_ of the circuit.

.. code::

    This is a valid circuit title

.. _element definition:
  
Element definition lines
------------------------

Lines of which the first non-whitespace charachter is not '*', ';', '.' or '+' are `element definition`_ lines

< elementName > [ < node1 > < node2 > [ < node3 > ...] ] | [ < ref1 > [ < ref2 > ... ] ] < value > | { < expr > } | modelName [ < param1 > = < value1 > | { < expr1 > } [ < param2 > = < value2 > | { < expr2 > } ... ] ]

.. code::

    C_1 in out 1p                                       ; capacitor C_1 with a capacitance of 1pF between
                                                        ; node in and out
    Ra out 0 r value={R_ell} dcvar={(sigma_R*R_ell)^2}  ; resistor Ra, model r with value = 1R_ell Ohm,
                                                        ; and an absolute variance of (sigma_R*R_ell)^2 Ohm^2
    R1 1 2 {1/2/pi/C_i/f_max}                           ; resistor R1, with a value of 1/2/pi/C_i/f_max Ohm
    Kc L1 Lout 0.95                                     ; coupling Kc between two inductors L1 and Lout with
                                                        ; a coupling factor of 0.95
    Na outP 0 in1 in2                                   ; nullor: nulator between nodes in1 and in2,
                                                        ; norator between nodes outP and 0
    Q1 c b e s BC547                                    ; bipolar transistor Q1, model BC547 with default
                                                        ; parameters
    Q1 c b e s Q2N3904 gm = 40m rpi = 2.5k              ; bipolar transistor Q1, model Q2N3904 with default
                                                        ; parameters except for gm and rpi, these are 40m 
                                                        ; and 2.5k, respectively

- **elementName**

  The first character is the element identifier (ID, see below), following characters constitute the instance identifier (alphanumeric and '_' used for subscripts) 
  
  A table with `element identifiers`_ is found below.

- **node1 ...**

  Alphanumeric characters

- **value ...**

  Numeric including scientific notation and postfixes (+, -, a, f, p, n, m, k, M, G, T, P)

  Only real numbers are accepted as input. Examples:

  - -12345
  - 12345
  - +12345
  - +123450e-1
  - 1.2345e4
  - 1.2345E+4
  - 12.345k
  - 0.012345M

  Both 'e' and 'E' can be used for the exponent in scientific notations.
  
- **expr ...**

  An expression including functions, normal brackets (), real numbers in scientific notation or with postfixes (see above)

- **modelName**

  Possible models for the element. The model name starts with a letter, following characters can be alphanumeric. Tables with built-in models_ for elements are given below.


- **ref1 ...**

  Reference to another element. It must be the *elementName* of an element of the circuit and not one of its parent circuit or one of its child circuits.

- **param1 ...**

  Parameter name, starts with a letter, following characters can be alphanumeric  and '_' used for subscripts.

Sub circuit definition
----------------------

.subckt < subcktName > < node1 > < node2 > [ < node3 > ... ]  [ params ]  [ < param1 > = < value1 > | {< expr1 >} [ < param2 > = < value2 > | { < expr2 > } ... ] ]

- **subcktName**

  Starts with a letter, following characters can be alphanumeric

.ends

 End of a sub circuit definition

Include a file
--------------

.include  < FileName1 > [ < FileName2 > ... ]

.inc < FileName1 >  [ < FileName2 > ... ]

- **fileName1 ...**

  Name of the file to be included, absolute or relative path. If there are spaces in the name, it should be placed within double quotes.

.. code::

    .inc "my include file.txt" anotherIncludeFile.txt

Library definition line
------------------------

.lib < fileName1 > [ < fileName2 > ... ]

.. code::

    .lib "/home/me/my library file.lib" anotherLibFile.txt

Model definition line
---------------------

.model < modelName > < modelType > ( < param1 > = < value1 > | {< expr1 >} [ < param2 > = < value2 > | {< expr2 >} ... ] )

.. code::

    .model OPA211 OV ; model with numeric model parameters
    + cd = 8p  ; differential-mode input capacitance 
    + gd = 50u ; differential-mode input conductance 
    + cc = 2p  ; common-mode input capacitance 
    + av = {0.67M*(1+s/2/pi/40M)/(1+s/2/pi/120)/(1+s/2/pi/20M)} ; voltage gain 
    + zo = {3.6k/(1+s*3.6k*8u) + 0.7 + s*900n*60/(60+s*900n)}   ; output impedance

    .model OPA211_A0 OV model with numeric model parameters except for the DC voltage gain
    + cd = 8p  ; differential-mode input capacitance 
    + gd = 50u ; differential-mode input conductance 
    + cc = 2p  ; common-mode input capacitance 
    + av = {A_0*(1+s/2/pi/40M)/(1+s/2/pi/120)/(1+s/2/pi/20M)}   ; voltage gain 
    + zo = {3.6k/(1+s*3.6k*8u) + 0.7 + s*900n*60/(60+s*900n)}   ; output impedance

parameter definition line
-------------------------

.param < param1 > = < value1 > | { <expr1 >}  [ < param2 > = < value2 > | { < expr2 > } ... ] ]

.. code::

    .param A_0 = 1M tau_p = {GB/2/pi/A_0} GB = 50M

end of the netlist
------------------

.. code::

    .end

.. _element identifiers:

Element identifiers
-------------------

**See SLiCAPprotos.py**

If an element can have more models, the **first** one is the default model.

+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| ID  | Description        | Nnodes |  Nrefs  |  Nval/expr  |  Models     |  Note                                          |
+=====+====================+========+=========+=============+=============+================================================+
| C   | Capacitor          | 2      |  0      |  1          |  C          |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| D   | Diode              | 2      |  0      |  0          |  D          |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| E   | VCVS               | 4      |  0      |  1          |  **E**      |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
|     |                    |        |         |             |  EZ         |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| F   | CCCS               | 2      |  1      |  1          |  F          | Spice compatible, differs from current SLiCAP  |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| G   | VCCS               | 4      |  0      |  1          |  **G**      |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
|     |                    |        |         |             |  g          |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| H   | CCVS               | 2      |  1      |  1          |  **H**      | Spice compatible, differs from current SLiCAP  |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
|     |                    |        |         |             |  HZ         |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| I   | Current source     | 2      |  0      |  1          |  I          |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| J   | JFET               | 3      |  0      |  0          |  J          |                                                | 
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| K   | Coupling factor    | 0      |  2      |  1          |  K          |                                                | 
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| L   | Inductor           | 2      |  0      |  1          |  L          |                                                | 
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| M   | MOSFET             | 4      |  0      |  0          |  **M**      |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
|     |                    |        |         |             |  MD         |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| N   | Nullor             | 4      |  0      |  0          |  N          |                                                | 
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| O   | OpAmp              | 4      |  0      |  0          |  **OV**     |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
|     |                    |        |         |             |  OC         |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| Q   | BJT                | 4      |  0      |  0          |  **QV**     |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
|     |                    |        |         |             |  QL         |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
|     |                    |        |         |             |  QD         |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| R   | Resistor           | 2      |  0      |  1          |  **R**      |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
|     |                    |        |         |             |  r          |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| T   | Transformer        | 4      |  0      |  1          |  T          |                                                | 
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| V   | Voltage source     | 2      |  0      |  1          |  **V**      |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
|     |                    |        |         |             |  VZ         |                                                |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| W   | Gyrator            | 4      |  0      |  1          |  G          |                                                | 
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| X   | Subcircuit         | x      |  0      |  0          |  < name >   | x: arbitrary number of nodes                   |
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+
| Z   | Impedance          | 2      |  0      |  1          |  Z          |                                                | 
+-----+--------------------+--------+---------+-------------+-------------+------------------------------------------------+

.. _models:

Models
------

SLiCAP has two different types of models: `stamp models`_ and `expansion models`_. Stamp models have an associated matrix stamp for building the MNA matrix equiation. Expansion models are expanded into stamp models during the checking of the circuit. 

**See SLiCAPprotos.py**

.. _stamp models:

Stamp models
~~~~~~~~~~~~

The table below gives an overview of the built-in stamp models.

**Nomenclature**

- ID

  Model identifier

- description

  Description of the model

- params

  Names of model parameters

- Laplace:    

  y: The LAPLACE variable is allowed in the expression of this parameter
  
  n: The LAPLACE variable 's' is not allowed in the expression of this parameter

+-----+---------------------------------+---------+---------+
| ID  | description                     | params  | Laplace | 
+=====+=================================+=========+=========+
| C   | Capacitor                       | value   | n       | 
+-----+---------------------------------+---------+---------+      
| E   | VCVS                            | value   | y       | 
+-----+---------------------------------+---------+---------+           
| EZ  | VCVS with series impedance      | value   | y       | 
+-----+---------------------------------+---------+---------+      
|     |                                 | zs      | y       | 
+-----+---------------------------------+---------+---------+      
| F   | CCCS                            | value   | y       | 
+-----+---------------------------------+---------+---------+     
| G   | VCCS                            | value   | y       |
+-----+---------------------------------+---------+---------+
| g   | VCCS (dc only)                  | value   | n       |
+-----+---------------------------------+---------+---------+
| H   | CCVS                            | value   | y       |
+-----+---------------------------------+---------+---------+
| HZ  | CCVS with series impedance      | value   | y       |
+-----+---------------------------------+---------+---------+  
|     |                                 | zs      | y       | 
+-----+---------------------------------+---------+---------+      
| I   | Current source                  | value   | y       | 
+-----+---------------------------------+---------+---------+
|     |                                 | dc      | n       | 
+-----+---------------------------------+---------+---------+
|     |                                 | dcvar   | n       | 
+-----+---------------------------------+---------+---------+
|     |                                 | noise   | n       | 
+-----+---------------------------------+---------+---------+
| K   | Coupling factor                 | value   | n       |
+-----+---------------------------------+---------+---------+
| L   | Inductor                        | value   | n       |
+-----+---------------------------------+---------+---------+
| N   | Nullor                          |         |         |
+-----+---------------------------------+---------+---------+
| R   | Resistor ( resistance != 0)     | value   | n       |  
+-----+---------------------------------+---------+---------+ 
| r   | Resistor ( resistance != inf)   | value   | n       |
+-----+---------------------------------+---------+---------+
|     |                                 | dcvar   | n       | 
+-----+---------------------------------+---------+---------+
| T   | Transformer                     | value   | n       | 
+-----+---------------------------------+---------+---------+
| V   | Voltage source                  | value   | y       | 
+-----+---------------------------------+---------+---------+
|     |                                 | dc      | n       | 
+-----+---------------------------------+---------+---------+
|     |                                 | dcvar   | n       | 
+-----+---------------------------------+---------+---------+
|     |                                 | noise   | n       | 
+-----+---------------------------------+---------+---------+
| VZ  | V source with series impedance  | value   | y       |
+-----+---------------------------------+---------+---------+  
|     |                                 | dc      | n       | 
+-----+---------------------------------+---------+---------+
|     |                                 | dcvar   | n       | 
+-----+---------------------------------+---------+---------+
|     |                                 | noise   | n       | 
+-----+---------------------------------+---------+---------+
|     |                                 | zs      | y       | 
+-----+---------------------------------+---------+---------+
| W   | Gyrator                         | value   | n       |  
+-----+---------------------------------+---------+---------+
| Z   | Impedance                       | value   | y       |
+-----+---------------------------------+---------+---------+


.. _expansion models:

Expansion models
~~~~~~~~~~~~~~~~

**Nomenclature**

- ID

  Model identifier

- description

  Description of the model

- params

  Names of model parameters

- Laplace:    

  y: Laplace variable 's' is allowed in the expression of this parameter
  
  n: Laplace variable 's' is not allowed in the expression of this parameter

- defValue

  default parameter value

+----+---------------------------------+---------+-----------------------------------------+---------+----------+
| ID | description                     | params  | Description                             | Laplace | defValue |
+====+=================================+=========+=========================================+=========+==========+
| D  | Diode                           | gd      | Conductance                             | n       | 1        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cd      | Capacitance                             | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | rs      | Series resistance                       | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
| J  | Junction FET                    | gm      | Transconductance                        | n       | 1m       |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | go      | Output conductance                      | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cgs     | Gate-source capacitance                 | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cdg     | Drain-gate capacitance                  | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
| M  | MOSFET                          | gm      | Transconductance                        | n       | 1m       |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | gb      | Bulk transconductance                   | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | go      | Output conductance                      | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cgs     | Gate-source capacitance                 | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cgb     | Gate-bulk overlap capacitance           | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cdg     | Drain-gate capacitance                  | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cdb     | Drain-bulk capacitance                  | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | csb     | Source-bulk capacitance                 | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
| MD | Differential-pair MOS           | gm      | Transconductance                        | n       | 1m       |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | go      | Output conductance                      | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cgg     | Input capacitance                       | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cdd     | Output capacitance                      | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cdg     | Drain-gate capacitance                  | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
| OC | Current feedback OpAmp          | gp      | pos input to supply (ground) resistance | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | gm      | Input stage transconductance            | n       | 20m      |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | gpn     | Differential input conductance          | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cp      | pos input to supply (ground) capacitance| n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cpn     | Differential input capacitance          | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | zt      | Output stage transimpedance             | y       | 1M       |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | Zo      | Output impedance                        | Y       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
| OV | Voltage feedback OpAmp          | gd      | Differential input conductance          | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | gc      | Common-mode input conductance           | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cd      | Differential-mode input capacitance     | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cc      | Common-mode input capacitance           | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | av      | Volatge gain factor                     | y       | 1M       |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | zo      | Output impedance                        | y       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
| QD | Differential-pair BJT           | gbb     | Input conductance                       | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | rb      | Base resistance                         | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | gm      | Transconductance                        | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | gcc     | Output conductance                      | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | gbc     | Collector-base conductance              | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cbb     | Input capacitance                       | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cbc     | Collector-base (internal) capacitance   | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cbx     | Collector-base (external) capacitance   | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
| QL | Lateral BJT                     | gpi     | Input conductance                       | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | rb      | Base resistance                         | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | gm      | Transconductance                        | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | go      | Output conductance                      | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | gbc     | Collector-base conductance              | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cbe     | Input capacitance                       | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cbc     | Collector-base (internal) capacitance   | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cbx     | Collector-base (external) capacitance   | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cs      | Substrate capacitance                   | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
| QV | Vertical BJT                    | gpi     | Input conductance                       | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | rb      | Base resistance                         | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | gm      | Transconductance                        | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | go      | Output conductance                      | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | gbc     | Collector-base conductance              | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cbe     | Input capacitance                       | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cbc     | Collector-base (internal) capacitance   | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cbx     | Collector-base (external) capacitance   | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+
|    |                                 | cs      | Substrate capacitance                   | n       | 0        |
+----+---------------------------------+---------+-----------------------------------------+---------+----------+

Parser output
=============

The output of the parser is a circuit object of which all expansion models and sub circuits have been expanded into elements with stamp models.

