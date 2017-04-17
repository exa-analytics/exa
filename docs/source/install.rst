.. Copyright (c) 2015-2016, Exa Analytics Development Team
.. Distributed under the terms of the Apache License 2.0

#####################################
Installation
#####################################
Python's external libraries are maintained as packages in repositories.
There are two main repositories, `pypi`_ and `anaconda`_ and two corresponding
Python applications that interact with them (pip and conda respectively).

This project recommends using conda because it is both a package manager and
a Python virtual environment manager. Anaconda also provides better cross
platform support especially for Python packages that require compiled external
dependences.


Anaconda
#######################
Using anaconda or miniconda...

.. code-block:: bash

    conda install numba exa


Pypi
#######################
Using pip...

.. code-block:: bash

    # sudo apt-get install llvm-3.7 or sudo yum install ... etc.
    sudo pip install numba exa


CUDA
###################
If working on a system with CUDA supported Nvidia GPUs...

.. code-block:: bash

    conda install cudatoolkit     # or via apt-get or yum etc.

Repository
#########################
Manually...

.. code-block:: bash

    # install llvm, numba, cudatoolkit, and CPython3.x
    git clone https://github.com/exa-analytics/exa
    cd exa
    pip install .


What's Next?
#####################
- Users should check out the :ref:`exa-user-overview`
- Contributors should check out the :ref:`exa-dev-overview`
- The :ref:`exa-api` contains usage and extension examples, and developer notes


.. _pypi: https://pypi.python.org/pypi
.. _anaconda: https://anaconda.org/anaconda/packages
