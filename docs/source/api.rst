.. Copyright (c) 2015-2017, Exa Analytics Development Team
.. Distributed under the terms of the Apache License 2.0

########################
Introduction
########################
The application program interface (API) is the syntax by which a user or developer
interacts with the code. The API is presented in order of dependencies and/or
requirements. Low level functionality (objects that make up the foundation of the
framework) are presented first. High level functionality is presented later. Users
may want to start with the :ref:`examples-label` page or get additional information 
interactively.

.. code-block:: python

    help(exa.Editor)
    exa.Editor?      # In Jupyter notebook

Visualization is accomplished with in the `Jupyter notebook`_ environment
using the `ipywidgets`_ machinery. Widgets are written in JavaScript and
follow the model, view, controller programming paradigm (see `backbone.js`_
which is leveraged by `ipywidgets`_). JavaScript features do not have the 
same interactivity as the Python API; they are used within the aforementioned
constraints of the `Jupyter notebook`_ `ipywidgets`_ framework. The JavaScript 
API is targeted toward developers; see also :ref:`extensions-label`.

.. note::

    JavaScript documentation is generated using `jsdoc`_ directly
    from the source code in js/src/ via the jsdoc to reStructuredText
    template available on the `web`_.

########################
Python API
########################
.. toctree::
    :maxdepth: 2

    py/01.rst
    py/02.rst
    py/03.rst
    py/04.rst
    py/05.rst
    py/06.rst

########################
JavaScript API
########################
.. toctree::
    :maxdepth: 2

    js/01.rst


.. _Jupyter notebook: https://jupyter.org
.. _ipywidgets: https://github.com/ipython/ipywidgets
.. _backbone.js: http://backbonejs.org/
.. _jsdoc: http://usejsdoc.org/
.. _web: https://github.com/HumanBrainProject/jsdoc-sphinx 
