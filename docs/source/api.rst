.. Copyright (c) 2015-2017, Exa Analytics Development Team
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
    exa.Editor?         # In an IPython environment (including the Jupyter notebook)

.. automodule:: exa.__init__
    :members:
    
.. automodule:: exa._version
    :members:

.. toctree::
    :maxdepth: 2
    :caption: Containers and Data

    api/container.rst
    api/frame.rst

.. toctree::
    :maxdepth: 2
    :caption: Text Processing

    api/editor.rst
    api/parser.rst
    api/composer.rst

.. toctree::
    :maxdepth: 2
    :caption: Utilities

    api/util/mpl.rst
    api/util/tex.rst
    api/util/constants.rst
    api/util/units.rst
    api/util/isotopes.rst


########################
Other Docs
########################
Additional module documentation is provided here. These modules are typically
useful for extension by developers.

.. toctree::
    :maxdepth: 2
    :caption: Typing

    api/typed.rst
    api/single.rst


########################
Unittest Docs
########################
Source code of tests can sometimes provide useful information for developers
and users.

.. toctree::
    :maxdepth: 2
    :caption: Tests

.. toctree::
    :maxdepth: 2
    :caption: Util Tests 
