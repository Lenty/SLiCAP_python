# SLiCAP

## What it is
- SLiCAP is an acronym for: **S** ymbolic **Li** near **C** ircuit **A** nalysis **P** rogram
- SliCAP is a tool for **algorithm-based analog design automation**
- SLiCAP is intended for setting up and solving **design equations** of electronic circuits
- SLiCAP is a an **open source** application written in Python and maxima CAS
- SLiCAP is part of the tool set for teaching 'Structured Electronic Design' at the Delft University of Technology

## Why you should use it
- SLiCAP facilitates analog design automation
- SLiCAP speeds up the circuit engineering process
- SLiCAP makes complex symbolic math doable
- SLiCAP integrates documentation and design
- SLiCAP facilitates design education and knowledge building

## Features
- Accepts SPICE-like netlists as input
- Concurrent design and documentation
- Supports and facilitates structured analog design

## Capabilities
- Conversion of hierarchically structured SPICE netlist into mixed symbolic/numeric matrix equation
- Symbolic and numeric noise analysis
- Symbolic and numeric noise integration over frequency
- Symbolic and numeric determination of transfer functions and polynomial coefficients of transfer functions
- Symbolic and numeric inverse Laplace Transform
- Symbolic and numeric determination of network solutions
- Accurate numeric pole-zero analysis
- Root-locus analysis with a arbitrarily selected circuit parameters as root locus variable(s)
- Symbolic and numeric DC and DC variance analysis for determination of budgets for resistor tolerances and offset and bias quantities
- Symbolic and numeric derivation and solution of design equations for bandwidh, frequency response, noise performance, dc variance and temperature stability

## Technology
- Python, Maxima CAS, HTML, CSS, LaTeX, MathJax, Jupyther Lab


## Setting up SLiCAP
To set up SLiCAP, the following components are required:
- A Python 3 install -  Dependencies of packages is found in requirements.txt
- Maxima CAS
- SLiCAP can generate netlists from schematics made with:
  - LTspice
  - gschem
  - lepton-eda

SLiCAP can be installed by running 'python setup.py install' or 'python setup.py install --user'. 

## First Run
To verify setting up of SLiCAP has been done correctly, it is possible to run one of the example projects that are in the examples/ directory. 
Here either jupyter notebooks or the python file with the name of the example can be ran.
Please take care to verify that the paths in the SLiCAPconfig.py of the example project are set correctly.

## Full Documentation
The full documentation can be found in the doc/_build/ directory, this can be rebuilt with Sphinx given that all dependencies are installed (such as the sphinx-rtd-theme).
In addition to the reference of functions, the documentation also contains elaborate information on the syntax that is to be used including examples.

## Contributing
This github page is to be used for contributing to SLiCAP.

### Adding features
Features should be added through pull requests and pass all checks that have been set up on the github page.
These tests include:
* Functional python tests
* Style tests verified using a linter

### Bugs
In case bugs are found, please report them to the 'Issues' page where we can resolve the issues and keep track of any possible bugs.

[![Build Status](https://travis-ci.com/Lenty/SLiCAP_python.svg?token=v99xpEdEDxCGytNHxFu2&branch=master)](https://travis-ci.com/Lenty/SLiCAP_python)
