==============
What is SLiCAP
==============

- SLiCAP is an acronym for: **S** ymbolic **Li** near **C** ircuit **A** nalysis **P** rogram
- SliCAP is a tool for **algorithm-based analog design automation**
- SLiCAP is intended for setting up and solving **design equations** of electronic circuits
- SLiCAP is a an **open source** application written in Python and maxima CAS
- SLiCAP is part of the tool set for teaching 'Structured Electronic Design' at the Delft University of Technology

=========================
Why should you use SLiCAP
=========================

- SLiCAP facilitates analog design automation
- SLiCAP speeds up the circuit engineering process
- SLiCAP makes complex symbolic math doable
- SLiCAP integrates documentation and design
- SLiCAP facilitates design education and knowledge building

Features
--------

- Accepts SPICE-like netlists as input
- Concurrent design and documentation
- Supports and facilitates structured analog design

Capabilities
------------

- Conversion of hierarchically structured SPICE netlist into mixed symbolic/numeric matrix equation
- Symbolic and numeric noise analysis
- Symbolic and numeric noise integration over frequency
- Symbolic and numeric determination of transfer functions and polynomial coefficients of transfer functions
- Symbolic and numeric inverse Laplace Transform
- Symbolic and numeric determination of network solutions
- Accuate numeric pole-zero analysis
- Root-locus analysis with a arbitrarily selected circuit parameters as root locus variable(s)
- Symbolic and numeric DC and DC variance analysis for determination of budgets for resistor tolerances and offset and bias quantities
- Symbolic and numeric derivation and solution of design equations for bandwidh, frequency response, noise performance, dc variance and temperature stability

Technology
----------

- Python, Maxima CAS, HTML, CSS, LaTeX, MathJax, Python, Jupyther Lab

=================
How to use SLiCAP
=================

Way of working
--------------

Working with SLiCAP usually requires the following steps:

#. Initialize a SLiCAP project; this will

   #. Create the directory structure for your project
   #. Create a configuration file for your project 
   #. Create the main html index page for this project

#. Create a circuit netlist and check the circuit

   SLiCAP supports netlist generation with gSchem and LTspice
    
#. Modify, add or delete circuit parameter definitions

#. Define an instruction

   You can change all the aspects of the instruction. If the instruction data is complete and consistent (this will be checked by SLiCAP), it can be executed. Definition of an instruction usually involves the following steps:

   #. Define the symbolic or numerical calculation mode: SLiCAP uses symbolic calculation methods, even if the data is numeric. If the simulation type is set to *numeric*, parameter values will recursively be substituted into the expressions for the circuit element values.
    
   #. Define the gain type: SLiCAP can provide expression for:

      - Nodal voltages or currents through voltage sources (or other elements that have been defined in current-controlled notation)
        
      - Transfer functions of the asymptotic-gain model:
            
        - the gain (source to detector transfer)    
        - the asymptotic-gain           
        - the loop gain           
        - the direct transfer           
        - the servo function
    
   #. Define the signal source, the detector and the loop gain reference variable according to the asymptotic-gain feedback model.
        
   #. Define the data type: 
        
      SLiCAP can provide many types of data:
    
      - Matrix equations for the circuit, with the matrices adapted to the gaintype       
      - Laplace transform of voltages, currents or transfer functions
      - Numerator or denominator of the above Laplace transform       
      - Time functions, unit impulse and unit step functions; calculated from the inverse Laplace transform        
      - Contributions to spectral densities of source-referred or detector-referred noise or integrated noise        
      - Poles, zeros and DC gain of a transfer function, with and without cancellation of coinciding poles and zeros        
      - DC voltage and current and their variance due to offset and bias currents and resistor tolerances
        
   #. Enable or disable parameter stepping for the instruction and define the step parameters.

#. Execute the instruction
    
#. Work with the results
    
   - SLiCAP has predefined functions for plotting, displaying tables and generation of web pages with beautifully typeset expressions, tables, figures and files. 
   - SLiCAP has a lot of postprocessing functions available for finding budgets for all kinds of performance parameters of electronic devices. 
   - There are many examples available for the design of the dynamic behavior and the noise behavior of amplifiers. 
   - It will be clear that once you have the (symbolic) matrix equation of a circuit, you have sufficient knowledge of Structured Analog Design, SLiCAP can help you with setting up and solving design equations for almost any design problem and, ultimately, with the automation of design engineering.
   - While doing your design work with SLiCAP, you concurrently generate a collection of linked html pages that document your work and help you to discuss your work with colleagues and present it to others on any platform with a web browser.

