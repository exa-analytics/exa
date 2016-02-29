# -*- coding: utf-8 -*-
'''
Indexing Recipes
=====================
Jitted functions related to generating indexes
'''
from exa import _np as np
from exa.jitted import jit, int64, vectorize


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


@jit(nopython=True, cache=True)
def idxs_from_starts_and_count(starts, count):
    '''
    '''
    n = len(starts)
    i_idx = np.empty((n * count, ), dtype=int64)
    j_idx = i_idx.copy()
    values = j_idx.copy()
    h = 0
    for i, start in enumerate(starts):
        stop = start + count
        for j, value in enumerate(range(start, stop)):
            i_idx[h] = i
            j_idx[h] = j
            values[h] = value
            h += 1
    return i_idx, j_idx, values
    

@vectorize([int64(int64, int64)])
def unordered_pairing_function(x, y):
    '''
    http://www.mattdipasquale.com/blog/2014/03/09/unique-unordered-pairing-function/
    '''
    return np.int64(x * y + np.trunc((np.abs(x - y) - 1)**2 / 4))
