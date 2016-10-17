# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
This sub-package provides function compilers using various tools available in
the Python ecosystem. For an introduction see :mod:`~exa.compute.__init__`.

- `Numba`_: :mod:`~exa.compute.compilers.nb`
- `Cython`_: :mod:`~exa.compute.compilers.cy`

.. _Numba: http://numba.pydata.org/
.. _Cython: http://cython.org/
"""
# Import modules
from exa.compute.compilers import nbcompiler

# Import sub-packages
from exa.compute.compilers import tests

# Import user/dev API
