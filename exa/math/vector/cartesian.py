# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Cartesian Vector Operations
#################################
This module provides common operations for vectors in cartesian space:

.. math::

    \\vec{r} = (x, y, z)
"""
import numpy as np
from exa._config import config


def magnitude(v):
    """
    .. math:

        \\left(x^2 + y^2 + z^2\\right)^{(1/2)}
    """
    return vector_magnitude_c(v[:, 0], v[:, 1], v[:, 2])


def magnitude_xyz(x, y, z):
    """
    .. math:

        \\left(x^2 + y^2 + z^2\\right)^{(1/2)}
    """
    return (x**2 + y**2 + z**2)**0.5


def magnitude_squared(v):
    """
    .. math:

        x^2 + y^2 + z^2
    """
    return vector_magnitude_squared_c(v[:, 0], v[:, 1], v[:, 2])


def magnitude_squared_xyz(x, y, z):
    """
    .. math:

        x^2 + y^2 + z^2
    """
    return x**2 + y**2 + z**2


def pdist_euclidean(x, y, z):
    """
    Pairwise Euclidean distance computation
    """
    m = len(x)
    n = m*(m - 1)//2
    r = np.empty((n, ), dtype=np.float64)
    h = 0
    for i in range(m):
        xi = x[i]
        yi = y[i]
        zi = z[i]
        for j in range(i + 1, m):
            r[h] = np.sqrt((xi - x[j])**2 + (yi - y[j])**2 + (zi - z[j])**2)
            h += 1
    return r


def pdist_euclidean_dr(x, y, z):
    """
    Pairwise Euclidean distance computation returning distance vectors
    """
    m = len(x)
    n = m*(m - 1)//2
    dx = np.empty((n, ), dtype=np.float64)
    dy = np.empty((n, ), dtype=np.float64)
    dz = np.empty((n, ), dtype=np.float64)
    r = np.empty((n, ), dtype=np.float64)
    h = 0
    for i in range(m):
        xi = x[i]
        yi = y[i]
        zi = z[i]
        for j in range(i + 1, m):
            xx = xi - x[j]
            yy = yi - y[j]
            zz = zi - z[j]
            dx[h] = xx
            dy[h] = yy
            dz[h] = zz
            r[h] = np.sqrt(xx**2 + yy**2 + zz**2)
            h += 1
    return dx, dy, dz, r


if config['dynamic']['numba'] == 'true':
    from numba import vectorize, jit
    types3 = ['int32(int32, int32, int32)', 'int64(int64, int64, int64)',
             'float32(float32, float32, float32)', 'float64(float64, float64, float64)']
    _magnitude = magnitude
    magnitude = jit(nopython=True, cache=True, nogil=True)(magnitude)
    _magnitude_xyz = magnitude_xyz
    magnitude_xyz = vectorize(types3, nopython=True)(magnitude_xyz)
    _magnitude_squared = magnitude_squared
    magnitude_squared = jit(nopython=True, cache=True, nogil=True)(magnitude_squared)
    _magnitude_squared_xyz = magnitude_squared_xyz
    magnitude_squared_xyz = vectorize(types3, nopython=True)(magnitude_squared_xyz)
    _pdist_euclidean = pdist_euclidean
    pdist_euclidean = jit(nopython=True, cache=True, nogil=True)(pdist_euclidean)
    _pdist_euclidean_dr = pdist_euclidean_dr
    pdist_euclidean_dr = jit(nopython=True, cache=True, nogil=True)(pdist_euclidean_dr)
    if config['dynamic']['cuda'] == 'true':
        magnitude_xyz_cuda = vectorize(types3, target='cuda')(_magnitude_xyz)
        magnitude_squared_xyz_cuda = vectorize(types3, target='cuda')(_magnitude_squared_xyz)
