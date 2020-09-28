# SLiCAP
SLiCAP stands for Symbolic Linear Circuit Analysis Program, and can be used for algorithm-based analog design automation.

## Setting up
To set up SLiCAP, the following components are required:
* A Python 3 install
* Maxima CAS
* A schematic capture tool, either LTspice or Gschem
Before running a program, be sure to update all the paths in the SLiCAPini.py file in the src/ folder.

Then SLiCAP can be installed by running 'python setup.py install'

## First Run
To verify setting up of SLiCAP has been done correctly, it is possible to run one of the example projects that are in the examples/ directory. 
Here either jupyter notebooks or the python file with the name of the example can be ran.

## Full Documentation
The full documentation can be found in the doc/_build/ directory, this can be rebuilt with Sphinx given that all dependencies are installed (such as the sphinx-rtd-theme).
In addition to the reference of functions, the documentation also contains elaborate information on the syntax that is to be used including examples.

## Contributing
Open-source version of SLiCAP, implemented in python.

This is currently a private repository and a work in progress
Updated
