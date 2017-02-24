.. Copyright (c) 2015-2017, Exa Analytics Development Team
.. Distributed under the terms of the Apache License 2.0

########################
JavaScript API
########################
Visualization is accomplished with in the `Jupyter notebook`_ environment
using the `ipywidgets`_ machinery. Widgets are written in JavaScript and
follow the model, view, controller programming paradigm (see `backbone.js`_
which is leveraged by `ipywidgets`_). JavaScript features do not have the 
same interactivity as the Python API; they are used within the aforementioned
constraints of the `Jupyter notebook`_ `ipywidgets`_ framework. The JavaScript 
API is targeted toward developers; see also :ref:`extensions-label`.

.. note::

    JavaScript documentation is generated using `jsdoc`_ directly
    from the source code in ``js/src/`` via the jsdoc to 
    reStructuredText template available on the `web`_.

.. toctree::
    :maxdepth: 2

    js/abcwidgets.rst

.. _Jupyter notebook: https://jupyter.org
.. _ipywidgets: https://github.com/ipython/ipywidgets
.. _backbone.js: http://backbonejs.org/
.. _jsdoc: http://usejsdoc.org/
.. _web: https://github.com/HumanBrainProject/jsdoc-sphinx 

