# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Additional Itertools
#########################
Specialized, compiled itertools functions.
"""
import numpy as np
from numba import jit


@jit(nopython=True, nogil=True)
def ncr2(values):
    """
    Pairwise combination (nCr(values, 2)).

    .. math::

        \\begin{bmatrix}
            n \\
            2
        \\end{bmatrix}
    """
    m = len(values)
    n = m*(m - 1)//2
    pairs = np.empty((n, 2), dtype=np.int64)
    k = 0
    for i, value in enumerate(values):
        for j in range(i+1, m):
            pairs[k, 0] = value
            pairs[k, 1] = values[j]
            k += 1
    return pairs
