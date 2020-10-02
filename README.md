# SLiCAP
SLiCAP stands for Symbolic Linear Circuit Analysis Program, and can be used for algorithm-based analog design automation which is to be used for algorithm-based analog circuit design automation.
SLiCAP is intended for creating and solving design equations of electronic circuits. The application is open source and primarily utilizes python and maxima CAS.


## Setting up
To set up SLiCAP, the following components are required:
* A Python 3 install -  Dependencies of packages is found in requirements.txt
* Maxima CAS
* A schematic capture tool, either LTspice or Gschem

Before running a program, be sure to update all the paths in the SLiCAP/SLiCAPconfig/SLiCAPconfig.py file.

Then SLiCAP can be installed by running 'python setup.py install' or 'python setup.py install --user'

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
