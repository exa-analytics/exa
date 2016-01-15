# -*- coding: utf-8 -*-
'''
Vectorized UFuncs
===============================

Warning:
    Using the vectorize option **target='parallel'** can cause instabilities
    on certain Windows systems (numba.__version__ == '0.22.1').
'''
from exa import _np as np
from exa.jitted import vectorize, float64, int32, int64, float32


@vectorize([int32(int32, int32, int32), int64(int64, int64, int64),
            float32(float32, float32, float32), float64(float64, float64, float64)])
def mag_3d(x, y, z):
    '''
    Computation of magnitude of a three dimensional vector.
    '''
    return (x**2 + y**2 + z**2)**0.5


@vectorize([int32(int32, int32), int64(int64, int64),
            float32(float32, float32), float64(float64, float64)])
def mod(x, y):
    '''
    Performs the modulo operation (remainder after division).
    '''
    return x % y
