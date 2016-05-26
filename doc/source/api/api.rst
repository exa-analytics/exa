.. _exa-api:

#####################################
API
#####################################
The application programming interface (API) is generated automatically.
All docs are pulled directly from the source code and may contain extension
examples, usage, and/or developer notes. The API documentation is organized
alphabetically with sub-packages appearing last.

.. toctree::
    :maxdepth: 3

    root.rst




HTML/JavaScript/CSS
############################



..
    Logical ordering of every function and class that is publicly exposed. In-line
    examples and warnings are also provided. This documentation can be obtained
    inside a Python environment in a variety of ways:

    .. code-block:: python

        help(exa.container)
        c = exa.Container()
        dir(c)
        #c.save?    # works in IPython/Jupyter notebook

    Python
    -------------------
    .. toctree::
        :maxdepth: 3

        modules/editor_an.rst
        modules/container_widget.rst
        modules/web_main.rst
        modules/config_install.rst
        modules/error_log_utility.rst
        relational.rst
        algorithms.rst
        distributed.rst
        tests.rst

    JavaScript
    -------------------
    .. toctree::
        :maxdepth: 2

        js/exa.rst
