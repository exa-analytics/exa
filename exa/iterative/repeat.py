# -*- coding: utf-8 -*-
'''
Repeat
############################
Functions for repeating arrays of varying dimensions.
'''
import numpy as np
from exa import global_config


def _repeat(array, counts):
    '''
    Repeat a 1D array.
    '''
    n = len(array)
    nn = np.sum(counts)
    repeated = np.empty((nn, ), dtype=np.float64)
    h = 0
    for i in range(n):
        count = counts[i]
        record = array[i]
        for j in range(count):
            repeated[h] = record
            h += 1
    return repeated


def _repeat_2d(array, counts):
    n, m = array.shape
    nn = np.sum(counts)
    repeated = np.empty((nn, m), dtype=np.float64)
    h = 0
    for i in range(n):
        count = counts[i]
        record = array[i]
        for j in range(count):
            repeated[h] = record
            h += 1
    return repeated


if global_config['pkg_numba']:
    repeat = jit(nopython=True, nogil=True, cache=True)(_repeat)
    repeat_2d = jit(nopython=True, nogil=True, cache=True)(_repeat_2d)
else:
    repeat = np.repeat
    repeat_2d = np.repeat
