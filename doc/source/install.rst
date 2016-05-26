Installation
=========================
Python's external libraries are maintained as packages in repositories.
There are two main repositories, `pypi`_ and `anaconda`_ and two corresponding
Python applications that interact with them (pip and conda respectively).

This project recommends using conda because it is both a package manager and
a Python virtual environment manager. Anaconda also provides better cross
platform support especially for Python packages that require compilation
(e.g. `llvm`_).

Using conda
-------------------
.. code-block::

    conda install exa

Manually
----------------
Install some dependencies..

.. code-block:: bash

    conda install numpy scipy pandas seaborn jupyter notebook numba dask distributed ipywidgets sympy setuptools

..then install the package.

.. code-block:: bash

    pip install .

Note that in general it is not good practice to use both conda and pip to manage the same Python
environment.


.. _pypi: https://pypi.python.org/pypi
.. _anaconda: https://anaconda.org/anaconda/packages
.. _llvm: https://anaconda.org/anaconda/llvm
