=======================
SLiCAP output documents
=======================

SLiCAP can generate latex reports, pdf files and html reports from output data. To this end, project data will be stored in the data attribute of a SLiCAPproject object. The report itself consists of a list of keys from this dictionary. HTML reports, LaTeX and PDF files etc. can be generated from this list. The contents list is generated during the execution of a SLiCAP project. The order of the items in the list can be changed with the move(oldPos, newPos) method of the SLiCAP project object.

The project object is created by executing initProject. It creates a project.ini file in the project directory. If this file exists its will not be overwritten.

Methods that need to be written are:

#. makeTeX(): creates a LaTeX file from the report
#. makeRST(): creates an RST file that can be compiled into a web site with Python Sphinx
#. showDocStructure(): gives a short overview of the document structure stored in the report attribute
#. showReport(): shows the report in the python editor

HTML reports will be generated from RST reports using Python Sphinx.

.. code:: python

    from time import time

    class SLiCAPproject(object):
        def __init__(self, projectName, creationDate, author):
            # attributes stored in the project.ini file:
            self.name    = projectName
            self.created = creationDate
            self.author  = author
            # attributes not stored in the ini file:
            self.updated = time()
            self.data    = {}
            self.report  = []

        def move(self, oldPos, newPos):
            self.report.insert(newPos, self.report.pop(oldPos))

The projectData dictionary
==========================

The projectData dictionary hold key-object pairs of data that can be put in documents. 

Keys are generated automatically:

#. text fragments:
   
   - key: tx_<i>, where i is an automatically generated number
   - object: list with stext strings, SLiCAP reference objects and Sympy symbols or expressions (for in-line display)

#. headers

   - key: h<n>_<i>, where n is the type of header (h1, h2, h3 or h4) and i is an automatically generated number
   - object: SLiCAP header object with the following attributes:

     - type: str: header type: 'h1', 'h2', 'h3' or 'h4'
     - text: str: header text
     - label: str: header label

#. equations

   - key: eq_<i>, where i is an automatically generated number
   - object: SLiCAP equation object with the following attributes:

     - lhs: Sympy object: left hand side of the equation
     - rhs: Sympy object: left hand side of the equation
     - label: str: equation label

#. figures

   - key: fi_<i>, where i is an automatically generated number
   - object: SLiCAP equation object with the following attributes:

     - file: str: location, relative to the path given in the SLiCAP.ini IMGPATH directive
     - width: int: figure width in pixels
     - label: str: label of the figure
     - caption: str: caption of the figure
     - figure: matplotlib figure object: if available

#. tabel

   - tb_<i>, where i is an automatically generated number
   - object: SLiCAP table object with the following attributes:

     - csvData: str: table data in csv format
     - cols: list: table formatting info: e.g. ['l', 'r', 'l']
     - widths: list: table relative column width in percentages: eg. [10, 20, 70]

#. reference

   - rf_<i>, where i is an automatically generated number
   - object: SLiCAP reference object with the following attributes:

     - labelName: str: name of the label of the object referred to.
