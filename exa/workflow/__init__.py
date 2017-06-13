# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
This subpackage provides functionality specific to high performance computing in
the context of :class:`~exa.core.container.Container` objects. This
subpackage is focused enabling seemless processing of containers with multiple
multidimensional, multifeatured, related data objects. Scaling up (utilizing
multicore/threaded processors, GPUs, compute cards) is accomplished via `numba`_
while scaling out (high performance computational cluster, i.e. a "supercomputer")
is accomplished using `ipyparallel`_ (and, where applicable, `mpi4py`_). Out
of core processing and some `distributed`_  tasks are accomplished using `dask`_.

- :mod:`~exa.core.dispatch`: Seemless management of algorithms acting on containers

.. _numba: http://numba.pydata.org/
.. _ipyparallel: https://ipyparallel.readthedocs.io/en/latest/
.. _mpi4py: http://mpi4py.scipy.org/
.. _dask: http://dask.pydata.org/en/latest/
.. _distributed: https://distributed.readthedocs.io/en/latest/
"""
