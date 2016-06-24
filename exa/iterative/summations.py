# -*- coding: utf-8 -*-
'''
Summations
######################################
Fast algorithms for iterative summations.
'''
import numpy as np
from itertools import product
from exa import global_config


def product_add_2(a, b):
    '''
    Python "add" every pair combination of elements a and b.
    '''
    return [a + b for a, b in product(a, b)]


def product_sum_2f(a, b):
    '''
    Sum every pair combination of elements of a and b.

    >>> a = np.random.rand(3)
    >>> b = np.random.rand(3)
    >>> product_sum_2f(a, b)
    '''
    return np.array([a + b for a, b in product(a, b)], dtype=np.float64)


def _product_sum_2f(a, b):
    '''
    JIT ready version of :func:`product_sum_2f`.
    '''
    na = len(a)
    nb = len(b)
    nn = na*nb
    sums = np.empty((nn, ), dtype=np.float64)
    h = 0
    for aa in a:
        for bb in b:
            sums[h] = aa + bb
            h += 1
    return sums


if global_config['pkg_numba']:
    from numba import jit
    _product_sum_2f_py = product_sum_2f
    product_sum_2f = jit(nopython=True)(_product_sum_2f)
    product_sum_2f_ng = jit(nopython=True, nogil=True)(_product_sum_2f)
