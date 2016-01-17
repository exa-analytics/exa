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


@vectorize([float64(float64, float64, float64, float64, float64, float64)])
def dist3d(x1, y1, z1, x2, y2, z2):
    '''
    '''
    return ((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)**0.5
