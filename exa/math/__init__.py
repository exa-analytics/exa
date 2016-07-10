# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Math
###################
Discrete and symbolic mathematical functions and algorithms. Many of the modules
in this sub-package attempt to compile Python source code down to machine code
(for CPU and GPU instruction as available).

Note:
    If a module compiles its functions to machine code, access to original
    (typically `numpy`_ supporting) functions is done via the same function
    name with a leading underscore. CUDA compiled functions have a trailing
    "_cuda".

See Also:
    :mod:`~exa.distributed.__init__`

Warning:
    Performance is guarenteed if `numba`_ is installed. If it is missing,
    performance will be affected and distributed/parallel computing features
    will not be available.

.. _numba: http://numba.pydata.org/numba-doc/latest/index.html
.. _numpy: http://www.numpy.org/
'''
from exa.math import misc, vector
