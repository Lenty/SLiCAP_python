=====================
Generate HTML reports
=====================

Writing design documentation is often something that needs to be done after the design work has been finished. By then, all kinds of information needs to be collected and structured in a document, while in many cases new projects are already taking most of the time. This undesirable but almost always inevitable practice can be prevented if the design work goes hand in hand with generation of the design documents. SLiCAP supports this with the generation of web-based design documentation in which figures, tables, expressions and ASCII files can be updated while running SLiCAP-MATLAB scripts. In this way, presentations and documentation can be kept up-to-date with the actual state of the design.

SLiCAP distinguishes two types of html pages:

- index pages: used for displaying tables of contents with links to other pages

  The attribute *ini.htmlIndex* is the name of the active index page

- data pages: used for displaying all kinds of design data, such as, tables, equations, text, graphs, images, etc.

  The attribute *ini.htmlPage* is the name of the active data page. 

- A list with the names of all the html pages is stored in *ini.htmlPages*

Detailed information about all html functions can be found in the module reference `SLiCAPhtml.py <../reference/SLiCAPhtml.html>`_.

.. _html:

-------------------
HTML site structure
-------------------

The structure of the project web site that can be generated with SLiCAP will be discussed below.

Main Index.html
---------------

Initialization of a project generates an *index.html* file in the *html/* project subdirectory. This file will hold the main table of contents of your project. Each time you check a circuit netlist that resides in the project directory, a list entry will be generated in this index file. 

.. code-block:: python

    >>> from SLiCAP import *
    >>> prj = initProject('My first RC network') # Initialize a SLiCAP project
    >>>                                          # and create main index page
    >>> print(ini.htmlIndex)                     # print the active index page
    index.html

Circuit index file
------------------

With the checking of a circuit, a circuit index page is generated:

.. code-block:: python

    >>> from SLiCAP import *
    >>> prj = initProject('My first RC network') # Initialize a SLiCAP project
    >>>                                          # and create main index page
    >>> instr = instruction()                    # Create an instance of an instruction object
    >>> instr.setCircuit('myFirstRCnetwork.cir') # Create a circuit from 'myFirstRCnetwork.cir'
                                                 # and create circuit index page
    No errors found for circuit: 'My first RC network' from file: 'myFirstRCnetwork.cir'.
    >>> print(ini.htmlIndex)                     # print the active index page
    My-first-RC-network_index.html

---------------------
Start a new html page
---------------------

It is a good practice to start a new html (data) page after checking the circuit, this prevents output to be writen to index files which would mess up the table of contents.

A new html data page can be created by evoking the command *htmlPage(< pageTitle >)*, in which *pageTitle* is the title of the new page (without .html file extension). After creation this new page is automatically assigned as active html data page. With the creation of a data page, a link to this data page is placed on the active index page.

.. code-block:: python

    >>> from SLiCAP import *
    >>> prj = initProject('My first RC network') # Initialize a SLiCAP project
    >>>                                          # and create main index page
    >>> instr = instruction()                    # Create an instance of an instruction object
    >>> instr.setCircuit('myFirstRCnetwork.cir') # Create a circuit from 'myFirstRCnetwork.cir'
                                                 # and create circuit index page
    No errors found for circuit: 'My first RC network' from file: 'myFirstRCnetwork.cir'.
    >>> htmlPage('Circuit data')                 # Create a new html data page and make it the 
                                                 # active data page
    >>> print(ini.htmlPage)
    My-first-RC-network_Circuit-data.html
    >>> print(ini.htmlPages)
    ['My-first-RC-network_index.html', 'index.html', 'My-first-RC-network_Circuit-data.html']

A new html index page can be created by evoking the command *htmlPage(< pageTitle >, index=True)*, in which *pageTitle* is the title of the new index page (without .html file extension).

After the creation this new index page, a link to this page is placed on the active index page. Subsequently, the new index page is assigned as new index page.
