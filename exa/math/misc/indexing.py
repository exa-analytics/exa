# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Indexing
#######################
Algorithms for generating indices.
'''
import numpy as np
from exa._config import config


def starts_count(starts, count):
    '''
    Generate sequential indices (for 2 dimensions) from starting values and
    lengths (counts).

    .. math:: Python

    Args:
        starts (:class:`numpy.ndarray`): Array of starting points
        count (int): Integer count

    Returns:
        objs (tuple): Outer sequential index, inner sequential index, resulting indicies
    '''
    n = len(starts) * count
    outer = np.empty((n, ), dtype=np.int64)
    inner = outer.copy()
    index = inner.copy()
    h = 0
    for i, start in enumerate(starts):
        stop = start + count
        for j, value in enumerate(range(start, stop)):
            outer[h] = i
            inner[h] = j
            index[h] = value
            h += 1
    return (outer, inner, index)


if config['dynamic']['numba'] == 'true':
    from numba import jit
    starts_count = jit(nopython=True, cache=True, nogil=True)(starts_count)
