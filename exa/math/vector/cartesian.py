# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Cartesian Vector Operations
#################################
This module provides common operations for vectors in cartesian space:

.. math::

    \\vec{r} = (x, y, z)
'''
import numpy as np
from exa._config import config


def magnitude(v):
    '''
    .. math:

        \\left(x^2 + y^2 + z^2\\right)^{(1/2)}
    '''
    return vector_magnitude_c(v[:, 0], v[:, 1], v[:, 2])


def magnitude_xyz(x, y, z):
    '''
    .. math:

        \\left(x^2 + y^2 + z^2\\right)^{(1/2)}
    '''
    return (x**2 + y**2 + z**2)**0.5


def magnitude_squared(v):
    '''
    .. math:

        x^2 + y^2 + z^2
    '''
    return vector_magnitude_squared_c(v[:, 0], v[:, 1], v[:, 2])


def magnitude_squared_xyz(x, y, z):
    '''
    .. math:

        x^2 + y^2 + z^2
    '''
    return x**2 + y**2 + z**2


if config['dynamic']['numba'] == 'true':
    from numba import vectorize, jit
    types = ['int32(int32, int32, int32)', 'int64(int64, int64, int64)',
             'float32(float32, float32, float32)', 'float64(float64, float64, float64)']
    _magnitude = magnitude
    magnitude = jit(nopython=True, cache=True, nogil=True)(magnitude)
    _magnitude_xyz = magnitude_xyz
    magnitude_xyz = vectorize(types, nopython=True)(magnitude_xyz)
    _magnitude_squared = magnitude_squared
    magnitude_squared = jit(nopython=True, cache=True, nogil=True)(magnitude_squared)
    _magnitude_squared_xyz = magnitude_squared_xyz
    magnitude_squared_xyz = vectorize(types, nopython=True)(magnitude_squared_xyz)
    if config['dynamic']['cuda'] == 'true':
        magnitude_xyz_cuda = vectorize(types, target='cuda')(_magnitude_xyz)
        magnitude_squared_xyz_cuda = vectorize(types, target='cuda')(_magnitude_squared_xyz)
