# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
This sub-package provides functionality for automatic compilation and
parallelization of functions and class methods. For high performance computing,
including parallel and distributed computing, functions need to operate with the
`GIL`_ removed. A natural method for releasing the GIL is through compilation
(see :mod:`~exa.compute.wrapper`). Because compilation (almost always)
requires statically typed arguments, this package provides a simple `multiple
dispatch`_ system for easy generation of function signatures for algorithms
dependent on specific input argument types.

Related to the issues of parallel and distributed computing are distributed
communication (see :mod:`~exa.compute.connects`) and resource management (see
:mod:`~exa.compute.resources`)

.. _GIL: https://wiki.python.org/moin/GlobalInterpreterLock
.. _multiple dispatch: https://en.wikipedia.org/wiki/Multiple_dispatch
"""
# Import modules
from exa.compute import connects, resources

# Import sub-packages
from exa.compute import tests

# Import user/dev API

# Import modules
#from exa.compute import connects, resources, compiler, dispatch, workflow

# Import sub-packages
#from exa.compute import algorithms, compilers, queue, tests

# Import user/dev API
#from exa.compute.compiler import compiler_function, available_compilers
#from exa.compute.dispatch import dispatch
