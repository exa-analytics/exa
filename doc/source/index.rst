.. exa documentation master file, created by
   sphinx-quickstart on Tue Jun 23 21:37:50 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

##################
`exa`_
##################
*An ecosystem for data processing, analytics, and visualization.*

This project leverages Python's open source scientific computing
environment to provide a high performance processing,
analytics, and visualization framework on which packages suited
for specific data industries can be built. This framework makes
use of the following open source projects (among others):
    - `numpy`_, `scipy`_: fundamental n-dimensional array manipulation
    - `pandas`_: expressive and labeled n-dimensional data structures (built on numpy)
    - `jupyter`_ (notebook): web-based Python interpreter
    - `ipywidgets`_: interactive widgets in browser
    - `ipyparallel`_: parallel processing
    - `sqlalchemy`_: access to SQL
    - `numba`_: just-in-time and ahead-of-time compilation, and GPU computing
    - `sympy`_: symbolic mathematics
    - `paramiko`_: ssh support
    - `mpi4py`_: MPI support

Exa provides a high performance computing environment tailored to
data specific containers (see :ref:`exa-overview`). These object
based storage devices are the foundation of a content management
system, flexible labeled data structure collection, and data
specific application framework.

.. toctree::
    :maxdepth: 2
    :caption: General Info

    overview.rst
    install.rst
    api/api.rst

.. toctree::
    :maxdepth: 2
    :caption: User Guide

    user/user.rst
..    user/started.rst
..    user/examples.rst
..    user/help.rst

.. toctree::
    :maxdepth: 2
    :caption: Contributor Guide

    dev/dev.rst
..    bugs.rst
..    proposal.rst
..    stack.rst
..    code.rst
..    contrib.rst


##################
Info
##################
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
.. _ipyparallel: https://ipyparallel.readthedocs.io/en/latest/
.. _numba: http://numba.pydata.org/
.. _sympy: http://www.sympy.org/en/index.html
.. _paramiko: http://www.paramiko.org/
.. _mpi4py: https://pythonhosted.org/mpi4py/
