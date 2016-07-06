# -*- coding: utf-8 -*-
'''
Summations
######################################
Fast algorithms for various types of (commonly used) summations.
'''
import numpy as np
from numba import jit
from itertools import product


def sum_product_pair(x, y):
    '''Sum each pair of elements coming from :func:`~itertools.product`.'''
    return [xx + yy for xx, yy in product(x, y)]


@jit(nopython=True, nogil=True)
def sum_product_pair_f8(x, y):
    '''
    Sum each pair of elements from two 1 dimensional arrays.
    '''
    m = len(x)
    n = len(y)
    values = np.empty((m*n, ), dtype=np.float64)
    i = 0
    for xx in x:
        for yy in y:
            values[i] = xx + yy
    return values
