==============
Parsing method
==============

The tokenizer
=============

Tokenizing of the input file with `Python Lex <https://www.dabeaz.com/ply/>`_.

   .. literalinclude:: ../SLiCAPlex.py
       :language: python
       :linenos:
       :lines: 1-191

Creation of a nested circuit object from the tokens
===================================================

Conversion of the tokenized input into a circuit object. Sub circuit definitions are stored as circuit object in their parent circuit. The procedure is found in ``SLiCAPyacc.py``:

   .. literalinclude:: ../SLiCAPyacc.py
       :language: python
       :linenos:
       :lines: 1-411

Expansion of the models and the sub circuits
============================================

This is the 'flattening' of the main circuit object


#. Models of elements that have not been defined in the netlist file are imported from libraries and added to the circuit's .modelDefs attribute. 

#. Model type elements will be expanded into a number of stamp-type elements. Built-in expansion models are defined as (sub) circuit objects and will be treated as such. This makes it possible for the user to add other models to SLiCAP, without having to dive into the hard coded scripts. Model parameters defined with an element will be passed to the sub circuit. Other elements will be given the value of their .model definition. If no definition is given they will receive the default value from the prototype model. Since elements with expansion models can be part of a sub circuit, such elements will be expanded before the sub circuit elements are passed to the parent circuit. The suffix '_< elementID > will be added to the name of the elements of the expanded model, where **elementID**  is the name of the (parent) element to be expanded.

   .. code::

       M1 d g s b MyMOS                  ; This is a MOSFET with gm=5m cgs=0.5p cdg=10f
                                         ; other parameters have their default value

       M2 d g s b MyMOS gm=10m cgs=1p    ; This is a MOSFET with gm=10m cgs=1p cdg=10f
                                         ; other parameters have their default value

       M3 d g s b M gm=1m cgs=0.05p      ; This is a MOSFET with gm=1m cgs=0.05p
                                         ; other parameters have their default value

       .model MyMOS M gm=5m cgs=0.5p cdg=10f


   Below the built-in sub circuit object of expansion model 'M' (four-terminal MOSFET). Definitions of these circuits are found in the library ``SLiCAPmodels.lib``.

   .. literalinclude:: ../lib/SLiCAPmodels.lib
       :linenos:
       :lineno-start: 37
       :lines: 37-47

   This is how the expansion of M2 would look in a netlist of the final circuit:

   .. code::

       Gm_M2  d s g s g value=10m
       Cgs_M2 g s     C value=1p
       Cdg_M2 d g     C value=10f

#. Nested inclusion of (child) sub circuits into their parent (sub) circuit

#. Parameters used in expressions of the elements of the sub circuit that have no associated definition in the .parDefs field of the sub circuit are added to this .parDefs field with: .parDefs[< parName >] = False

#. The entries in the .parDefs dictionary of the sub circuit are added to the .parDef attribute of the parent circuit, after all the parameter names in the keys and in the values of the sub circuit .parDefs attribute obtain the extension _Xnnn, except for the parameters that are passed from the parent circuit to the sub circuit. The latter ones obtain their definition given in the parent circuit.

#. Before the elements of the sub circuit are added to the list of elements of the parent circuit, their element identifiers will obtain a suffix _< elementID >, in which **elementID** is the ID of the sub circuit.

#. All parameters used in expression of elements of the sub circuit, except those that should be passed from the parent circuit will also have this suffix added to their name.

   .. code::
 
       "Voltage divider"

       X1 in out 0 vDivider A = {alpha}          ; Sub circuit element X1
                                                 ; parameter A is passed to the sub circuit
       .subckt vDivider inp outp GND A={A} R={R} ; Sub circuit definition parameters A and R
                                                 ; can be passed from the parent circuit
       R1 input  output {R*(1-A)}
       R2 output GND    {R*A}
       .param A=0.1 R=10k                        ; .param A=0.1 is overruled by A={alpha}
       .ends

       .param alpha=0.5
       .end
       
   The above circuit will expand to:

   .. code::
 
       "Voltage divider"

       R1_X1 in  out {R_X1*(1-alpha)}
       R2_X1 out 0   {R_X1*alpha}

       .param R_X1=10k alpha = 0.5
       .end

#. Parameters used in expressions of the elements of the main circuit that have no associated definition in the .parDefs field of the main circuit are added to this .parDefs field with: .parDefs[< parName >] = False

The procedure for flattening the circuit is found in ``SLiCAPyacc.py``:

   .. literalinclude:: ../SLiCAPyacc.py
       :language: python
       :linenos:
       :lineno-start: 413
       :lines: 413-629

Updating of circuit data
========================

This comprises:

#. Creation of the circuit object attributes for:

   #. Independent sources (can be assigned as signal source)

      This will be a list with IDs of voltage and current sources

   #. Dependent variables (can be assigned as detector)

      This wil be a list with nodal voltages and branch currents of current-controlled elements.

      - The voltage at node <Nnnn> with be named V_<Nnnn>
      - A current through a branch of a current-controlled element with element ID <elID> will be named  I_<elID> for two-terminal elements, Ii_<elID> for controlled sources that have a current-controlled input port and Io_<elID> for controlled sources that have a current-controlled output port.

   #. Controlled sources (can be assigned as loop gain reference) 


The procedure for updating the circuit data is found in ``SLiCAPyacc.py``:

.. literalinclude:: ../SLiCAPyacc.py
    :language: python
    :linenos:
    :lineno-start: 631
    :lines: 631-702

Recursive substitution
======================

Recursive substitution is performed by the function ``fullSubs``. It is located in ``SLiCAPhtml.py``. It is used during the flattening of the circuit and in some HTML functions. 

.. literalinclude:: ../SLiCAPhtml.py
    :language: python
    :linenos:
    :lineno-start: 372
    :lines: 372-398
