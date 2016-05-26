.. exa documentation master file, created by
   sphinx-quickstart on Tue Jun 23 21:37:50 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

##################
`exa`_
##################
*An ecosystem for data processing, analytics, and visualization.*

This project leverages Python's open source scientific computing
environment to provide a high performance, processing,
analytics, and visualization suite for specific data industries.
The **exa** package provides the foundation on which these data
specific applications are built. This suite makes use of the
following open source projects (among others):
    - `numpy`_, `scipy`_: fundamental n-dimensional array manipulation
    - `pandas`_: expressive and labeled n-dimensional data structures (built on numpy)
    - `jupyter`_ (notebook): web-based Python interpreter
    - `ipywidgets`_: interactive widgets in browser
    - `sqlalchemy`_: access to SQL
    - `numba`_: just-in-time and ahead-of-time compilation of Python to machine code
    - `cudatoolkit`_: Nvidia CUDA GPU computing
    - `distributed`_: distributed computing
    - `dask`_: Out-of-core computing
    - `sympy`_: symbolic mathematics

.. toctree::
    :maxdepth: 2
    :caption: User Guide

    install.rst
    started.rst
..    api.rst

.. toctree::
    :maxdepth: 2
    :caption: Developer Info

..    bugs.rst
..    proposal.rst
..    stack.rst
..    code.rst
..    contrib.rst


=============
Info
=============
:download:`License <../../LICENSE>`

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _exa: https://exa-analytics.github.io/
.. _Python: https://www.python.org/
.. _numpy: http://www.numpy.org/
.. _scipy: https://www.scipy.org/
.. _pandas: http://pandas.pydata.org/
.. _sqlalchemy: http://www.sqlalchemy.org/
.. _jupyter: http://jupyter.org/
.. _ipywidgets: https://ipywidgets.readthedocs.io/en/latest/
.. _numba: http://numba.pydata.org/
.. _cudatoolkit: https://anaconda.org/sklam/cudatoolkit
.. _distributed: http://distributed.readthedocs.io/en/latest/
.. _dask: http://dask.pydata.org/en/latest/
.. _sympy: http://www.sympy.org/en/index.html
