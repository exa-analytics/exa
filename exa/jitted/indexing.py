# -*- coding: utf-8 -*-
'''
Indexing Recipes
=====================
Jitted functions related to generating indexes
'''
from exa import _np as np
from exa.jitted import jit, int64


@jit(nopython=True, cache=True)
def idxs_from_starts_and_counts(starts, counts):
    '''
    Numba'd version of :func:`~exa.jitted
    '''
    n = np.sum(counts)
    i_idx = np.empty((n, ), dtype=int64)
    j_idx = i_idx.copy()
    values = j_idx.copy()
    h = 0
    for i, start in enumerate(starts):
        stop = start + counts[i]
        for j, value in enumerate(range(start, stop)):
            i_idx[h] = i
            j_idx[h] = j
            values[h] = value
            h += 1
    return i_idx, j_idx, values
