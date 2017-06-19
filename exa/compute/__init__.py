# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Algorithm performance depends on the size of the data being processed as well
as the characteristics of the functions. This subpackage provides a mechanism
for building efficient, scalable algorithms that perform at the local machine
scale as well as distributed high performance scale. The features

- :mod:`~exa.compute.dispatch`: Dynamic algorithm selection based on data size and available resources

The technical details are as follows. `GIL`_ release is accomplished by function
and class compilation using the `numba`_ package. This is an `LLVM`_ compiler
that generates machine code specific to the resources in used. Local
parallelization and GPU/MIC card support are also accomplished using this
package. Distributed computation is done via `ipyparallel`_, `mpi4py`_, and
`dask`_ (`distributed`_).

.. _GIL: https://wiki.python.org/moin/GlobalInterpreterLock
.. _numba: http://numba.pydata.org/
.. _LLVM: http://llvm.org/
.. _ipyparallel: https://ipyparallel.readthedocs.io/en/latest/
.. _mpi4py: http://mpi4py.scipy.org/
.. _dask: http://dask.pydata.org/en/latest/
.. _distributed: https://distributed.readthedocs.io/en/latest/
"""
