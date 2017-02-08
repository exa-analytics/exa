.. Copyright (c) 2015-2017, Exa Analytics Development Team
.. Distributed under the terms of the Apache License 2.0

########################
Introduction
########################
The application program interface (API) is the syntax by which a user or developer
interacts with the code. A full listing of source code documentation is given in
the following pages. Additional ways of getting this information interactively are
as follows.

.. code-block:: python

    help(exa.Editor)
    exa.Editor?      # In Jupyter notebook

Users may want to consult the :ref:`examples-label` page for most common usage.
The API is organized in (pseudo) dependency order: objects that are used by 
higher level functionality in the package are presented first. More complex
functionality (i.e. API used by users) is presented later.

.. automodule:: exa.__init__
    :members:

.. toctree::
    :maxdepth: 1

    root/01_init.rst
    root/02_err.rst
    root/03_mcs.rst
    root/04_util.rst
    root/05_tests.rst
