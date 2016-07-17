# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Repeat
############################
Functions for repeating arrays of varying dimensions.
"""
import numpy as np
from exa._config import config


def repeat_count(array, n):
    """
    Repeat each element of an array n times.
    """
    pass


def repeat_counts_f8_1d(array, counts):
    """
    Repeat each element of an array n times (with variable n).
    """
    m = len(array)
    nn = np.sum(counts)
    repeated = np.empty((nn, ), dtype=np.float64)
    h = 0
    for i in range(m):
        count = counts[i]
        record = array[i]
        for j in range(count):
            repeated[h] = record
            h += 1
    return repeated


def repeat_counts_f8_2d(array, counts):
    """
    Repeat each element of an array n times (with variable n).
    """
    m, n = array.shape
    nn = np.sum(counts)
    repeated = np.empty((nn, n), dtype=np.float64)
    h = 0
    for i in range(m):
        count = counts[i]
        record = array[i]
        for j in range(count):
            repeated[h] = record
            h += 1
    return repeated


if config['dynamic']['numba'] == 'true':
    from numba import jit
    repeat_counts_f8_1d = jit(nopython=True, cache=True, nogil=True)(repeat_counts_f8_1d)
    repeat_counts_f8_2d = jit(nopython=True, cache=True, nogil=True)(repeat_counts_f8_2d)
