# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Summations
######################################
Fast algorithms for various types of (commonly used) summations.
'''
import numpy as np
from itertools import product
from exa._config import config


def sum_product_pair(x, y):
    '''Sum each pair of elements coming from :func:`~itertools.product`.'''
    return [xx + yy for xx, yy in product(x, y)]


def sum_product_pair_f8(x, y):
    '''
    Sum each pair of elements from two 1 dimensional arrays.

    .. code-block:: Python

        x = np.array([1., 2., 3.])
        y = np.array([4., 1., 2.])
        sum_product_pair_f8(x, y)    # array([5.0, 2.0, 3.0, 6.0, 3.0, 4.0, 7.0, 4.0, 5.0])
    '''
    m = len(x)
    n = len(y)
    values = np.empty((m*n, ), dtype=np.float64)
    i = 0
    for xx in x:
        for yy in y:
            values[i] = xx + yy
            i += 1
    return values


if config['dynamic']['numba'] == 'true':
    from numba import jit
    sum_product_pair_f8 = jit(nopython=True, nogil=True, cache=True)(sum_product_pair_f8)
