.. _exa-overview:

##################
Overview
##################
Data typically comes as labeled n-dimensional arrays (e.g. comma separated
values). This project organizes data of this type (and
higher dimension data) as parts of a "container". Containers are persistent
data stores for dataframe (spreadsheet like) and series (array like) objects.
Containers are tailored to specific data-based industries
and provide methods for high performance computing, (pre- and post-) processing,
analysis, and visualization (see :mod:`~exa.container`).

In addition to being a production ready tool for industry, this projects aims
to support academia by enabling transparent, reproducible, scientific data
exploration that can be readily shared between collaborating scientists,
professors, and students.

Scalability
##########################
This project builds a scalable data processing framework using `ipyparallel`_
and `mpi4py`_ (`MPI`_). Global interpreter lock (`GIL`_) is overcome by using `numba`_
compiled functions. This enables the use Python's standard library for
multithreaded applications.

User Interfaces
##########################
All software that is part of this project is expected to work within a
traditional Python shell, IPython interpreter, or `Jupyter notebook`_.
The notebook interface allows for interactive data exploration, processing,
and visualization. A dedicated application is currently under construction.


.. _MPI: https://computing.llnl.gov/tutorials/mpi/
.. _mpi4py: https://pythonhosted.org/mpi4py/
.. _Jupyter notebook: https://try.jupyter.org/
.. _numba: http://numba.pydata.org/
.. _ipyparallel: https://ipyparallel.readthedocs.io/en/latest/
