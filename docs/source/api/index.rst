.. Copright (c) 2015-2018, Exa Analytics Development Team
.. Distributed under the terms of the Apache License 2.0

.. _api-label:

########################
User Docs
########################
The following sections describe syntax and usage of the functions and classes
provided by the Exa package. Documentation is organized for the typical use case;
a collection of structure text files need to be parsed into Pythonic data objects
and then organized into a container to facilitate visualization. Useful examples 
can be found at :ref:`examples-label` or via help::

    import exa
    help(exa)           # Package help
    help(exa.isotopes)  # Module help
    help(exa.Editor)    # Class help
    exa.Editor?         # Help in the Jupyter notebook

.. automodule:: exa.__init__
    :members:
    
.. automodule:: exa._version
    :members:

.. toctree::
    :maxdepth: 2
    :caption: Core API

    container.rst
    editor.rst
    data.rst

.. toctree::
    :maxdepth: 2
    :caption: Util

    typed.rst
    static.rst
    util/units.rst
    util/isotopes.rst
    util/constants.rst
    util/misc.rst


########################
Unittest Docs
########################
Source code of tests can sometimes provide useful information for developers
and users.

.. toctree::
    :maxdepth: 2
    :caption: Tests

    tests1.rst
    tests2.rst
    tests3.rst
