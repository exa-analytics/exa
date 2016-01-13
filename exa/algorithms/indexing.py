# -*- coding: utf-8 -*-
'''
Indexing Recipes
=====================
Functions related to generating indexes
'''
from exa import _np as np


def idxs_from_starts_and_counts(starts, counts):
    '''
    Generates flat indexes from starting points (starts) and counts
    with incrementing by 1.
    '''
    n = np.sum(counts)
    i_idx = np.empty((n, ), dtype='i8')
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
    return (i_idx, j_idx, values)
