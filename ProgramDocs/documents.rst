=======================
SLiCAP output documents
=======================

SLiCAP can generate latex reports, pdf files and html reports from output data. To this end, project data will be stored in a dictionary, which is an attribute of a SLiCAPproject object. The internal structure of the SLiCAP report itself is a list of keys from this dictionary. HTML web sites, LaTeX files and PDF documents can be generated from this list, simply by using buit-in methods. The contents of the dictionary and the list are generated during the execution of a SLiCAP project. The order of the items in the list can be changed with the move() method of the SLiCAPproject object.

An instance of the SLiCAPproject object is created by executing initProject(). When running it for the first time, it creates a project.ini file in the project directory. If this file exists its will not be overwritten.

HTML reports will be generated from RST reports using Python Sphinx. PDF documents are generated with pdflatex.

.. code:: python

    from datetime import datetime

    class SLiCAPproject(object):
        def __init__(self, projectName, creationDate, author):
            # attributes stored in the project.ini file:
            self.name    = projectName
            self.created = creationDate
            self.author  = author
            # attributes generated each time running initSLiCAP:
            self.updated = datetime.now() # Last updated
            self.data    = {}             # Project data dictionary with key-object pairs
            self.report  = []             # List of keys (links to the project data dictionary)

        def move(self, label, afterLabel):
            """
            moves 'label' to the next position of 'afterLabel'
            """
            self.report.insert(self.report.index(afterLabel), self.report.pop(self.report.index(label))

The project data dictionary
===========================

The projectData dictionary holds key-object pairs of data that can be put in documents. 

Keys are generated automatically:

#. text fragments:
   
   - key: tx_<i>, where i is an automatically generated number
   - object: list with text strings, SLiCAP reference objects and Sympy symbols or expressions (for in-line display).

   Text fragments will be treated as follows:
     
   - Sympy symbols or expressions will be converted into LaTex, RST or mathml format, this according to the final document format required.
   - Reference object will be converted into HTML links of LaTeX references, this according to the final document format required.
   - The total of the above will be converted into a HTML paragraph or a LaTeX paragraph.

#. headings

   - key: label, or h<n>_<i>, where n is the type of heading (h1, h2, h3 or h4) and i is an automatically generated number
   - object: SLiCAP heading object with the following attributes:

     - type: str: heading type: 'h1', 'h2', 'h3' or 'h4'
     - text: str: heading text
     - label: str: heading label

   Headings will be treated as follows:

   - h1: Chapter or new HTML page
   - h2: Section or h2 heading on HTML pages
   - h3: Subsection or h3 heading on HTML pages
   - h4: Subsubsection or h4 heading on HTML pages

#. equations

   - key: label, or eq_<i>, where i is an automatically generated number
   - object: SLiCAP equation object with the following attributes:

     - lhs: Sympy object: left hand side of the equation
     - rhs: Sympy object: left hand side of the equation
     - units: units
     - label: str: equation label

   Equations will be treated as follows:

   - Equations will be converted into displayed equations with an equation number.
   - Units will be placed between square brackets '[' ']' between the equation and the equation number

#. figures

   - key: label, or fg_<i>, where i is an automatically generated number
   - object: SLiCAP equation object with the following attributes:

     - file: str: location, relative to the path given in the SLiCAP.ini IMGPATH directive
     - width: int: figure width in pixels
     - label: str: label of the figure
     - caption: str: caption of the figure
     - figure: matplotlib figure object: if available
   
   Figures will be treated as follows:

   - image files (.svg, .png, .gif, .jpg) will be displayed in the output
   - matplotlib figure objects will be converted into .svg files and displayed in the output
   - The caption will be placed with the figure

#. tabel

   - key: label, or tb_<i>, where i is an automatically generated number
   - object: SLiCAP table object with the following attributes:

     - csvData: str: table data in csv format
     - cols: list: table formatting info: e.g. ['l', 'r', 'l']
     - widths: list: table relative column width in percentages: eg. [10, 20, 70]
     - label: str: label of the table
     - label: str: label of the table

   Tables will be treated as follows:

     - table data (see above) will be used to create the table and display it in the output
     - The caption will be placed with the table

#. reference

   - key: rf_<label>, where label is the label of the object it refers to
   - object: SLiCAP reference object with the following attributes:

     - labelName: str: name of the label of the object referred to.
   
   References will be treated as follows:

   - In HTML files it will be converted into a link to the referenced object
   - In LaTeX output it will be treated in the standard LaTeX way

#. file

   - key: label, or fi_<i>, where i is an automatically generated number
   - object: SLiCAP file object with the following attributes:

     - file: str: location, relative to the path given in the SLiCAP.ini for associated file types
     - label: str: label of the file
     - caption: str: caption for figures and tables

   Files will in documents will be treated as follows:

   - image files (.svg, .png, .gif, .jpg) will be displayed in the output
   - csv files (.csv) will be converted into tables and included in the output
   - text files (.txt) will be included in the output, latex can be included in these files
   - netlist files (.net, .cir) will be included in monospace font
   - code files (.py, .c, .m, .mu, etc.) files will be included as code
   - for other file types (.pdf, .zip, .avi, etc.) a link to these files will be placed in the final document
 
The report list
===============

The .report attribute of the SLiCAPproject object is a list of keys from the projectData dictionary. The order of items in the report can be changed with the move() method of the SLiCAPproject object.

Generating reports from the report list
=======================================

The report list is created by appending objects to it. A LaTeX file, an RST file, an HTML file or a PDF file can be generated from it with built-in methods. Other document formats can be generated from these files using pandoc.

Methods that need to be written are:

#. makeTeX(): creates a LaTeX file from the report
#. makeRST(): creates an RST file that can be compiled into a web site with Python Sphinx
#. showDocStructure(): gives a short overview of the document structure stored in the report attribute
#. showReport(): shows the report in the python editor

HTML output is generated with Python Sphinx, ReStructured text (RST) files are generated as intermediate formats. PDF files are generated with pdflatex, .tex files are generated as intermediate formats.
