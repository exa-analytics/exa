.. Copyright (c) 2015-2017, Exa Analytics Development Team
.. Distributed under the terms of the Apache License 2.0

########################
Python API
########################
The application program interface (API) is the syntax by which a user or developer
interacts with the code. The API is presented in order of dependencies and/or
requirements. Low level functionality (objects that make up the foundation of the
framework) are presented first. High level functionality is presented later. Users
may want to start with the :ref:`examples-label` page or get additional information 
interactively.

.. code-block:: python

    help(exa)           # Package help
    help(exa.isotopes)  # Module help
    help(exa.Editor)    # Class help
    exa.Editor?         # In an IPython environment (including the notebook)

.. automodule:: exa.__init__
    :members:

.. toctree::
    :maxdepth: 2

    py/single_typed.rst
    py/base.rst
    py/editor.rst
    py/container.rst
    py/data.rst
    py/abcwidgets.rst
    py/threejs.rst
    py/physical.rst
    py/utils.rst
