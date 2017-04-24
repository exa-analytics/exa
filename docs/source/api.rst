.. Copyright (c) 2015-2017, Exa Analytics Development Team
.. Distributed under the terms of the Apache License 2.0

########################
User Docs
########################
The following sections describe syntax and usage of the functions and classes
provided by the Exa package. Documentation is organized for the typical use case;
a collection of structure text files need to be parsed into Pythonic data objects
and then organized into a container to facilitate visualization. Useful examples 
can be found at :ref:`examples-label`.

.. code-block:: python

    import exa
    help(exa)           # Package help
    help(exa.isotopes)  # Module help
    help(exa.Editor)    # Class help
    exa.Editor?         # In an IPython environment (including the notebook)

.. automodule:: exa.__init__
    :members:
    
.. automodule:: exa._version
    :members:

.. toctree::
    :maxdepth: 2
    :caption: Editors

    api/editors/editor.rst
    api/editors/sections.rst
    api/editors/parser.rst
    api/editors/tests.rst

.. toctree::
    :maxdepth: 2
    :caption: Data Objects

    api/data/dataseries.rst
    api/data/dataframe.rst
    api/data/container.rst

.. toctree::
    :maxdepth: 2
    :caption: Utilities

    api/mpl.rst
    api/tex.rst
    api/constants.rst
    api/units.rst
    api/isotopes.rst


########################
Dev Docs
########################

.. toctree::
    :maxdepth: 2
    :caption: Miscellanous

    api/special.rst
    api/base.rst
