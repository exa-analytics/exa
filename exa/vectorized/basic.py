# -*- coding: utf-8 -*-
'''
Vectorized Basic Operations
###########################################
Numba vectorized operations for addition, subtraction, multiplication, and
division typically used in place to numpy/pandas built-ins.

Note:
    Numpy's automatic broadcasting is usually more efficient than calling
    numpy.vectorize.
'''
from exa import global_config


def mul_2(a, b):
    return a*b


if global_config['pkg_numba']:
    from numba import vectorize
    mul_2 = vectorize(nopython=True)(mul_2)
