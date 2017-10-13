# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Cartesian Vector Operations
#################################
This module provides common operations for vectors in cartesian space:

.. math::

    \\vec{r} = (x, y, z)
"""
import numpy as np
from numba import jit, vectorize


types3 = ['int32(int32, int32, int32)', 'int64(int64, int64, int64)',
          'float32(float32, float32, float32)', 'float64(float64, float64, float64)']


@jit(nopython=True, nogil=True, cache=True)
def magnitude(v):
    """
    .. math:

        \\left(x^2 + y^2 + z^2\\right)^{(1/2)}
    """
    return vector_magnitude_c(v[:, 0], v[:, 1], v[:, 2])

@vectorize(types3, nopython=True)
def magnitude_xyz(x, y, z):
    """
    .. math:

        \\left(x^2 + y^2 + z^2\\right)^{(1/2)}
    """
    return (x**2 + y**2 + z**2)**0.5


@jit(nopython=True, nogil=True, cache=True)
def magnitude_squared(v):
    """
    .. math:

        x^2 + y^2 + z^2
    """
    return vector_magnitude_squared_c(v[:, 0], v[:, 1], v[:, 2])


@vectorize(types3, nopython=True)
def magnitude_squared_xyz(x, y, z):
    """
    .. math:

        x^2 + y^2 + z^2
    """
    return x**2 + y**2 + z**2


@jit(nopython=True, nogil=True, cache=True)
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


@jit(nopython=True, nogil=True, cache=True)
def pdist_euclidean_dr(x, y, z):
    """
    Pairwise Euclidean distance computation returning distance vectors as well
    as magnitudes (distances).
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


@jit(nopython=True, nogil=True, cache=True)
def pdist_euc_dxyz_idx(x, y, z, indexes):
    """
    Pairwise Euclidean distance computation returning distance vectors as well
    as pair indexes.
    """
    m = len(x)
    n = m*(m - 1)//2
    dx = np.empty((n, ), dtype=np.float64)
    dy = np.empty((n, ), dtype=np.float64)
    dz = np.empty((n, ), dtype=np.float64)
    dr = np.empty((n, ), dtype=np.float64)
    idxi = np.empty((n, ), dtype=np.int64)
    idxj = np.empty((n, ), dtype=np.int64)
    h = 0
    for i in range(m):
        xi = x[i]
        yi = y[i]
        zi = z[i]
        indexi = indexes[i]
        for j in range(i + 1, m):
            xx = xi - x[j]
            yy = yi - y[j]
            zz = zi - z[j]
            dx[h] = xx
            dy[h] = yy
            dz[h] = zz
            dr[h] = np.sqrt(xx**2 + yy**2 + zz**2)
            idxi[h] = indexi
            idxj[h] = indexes[j]
            h += 1
    return dx, dy, dz, dr, idxi, idxj


@jit(nopython=True, nogil=True, cache=True)
def periodic_pdist_euc_dxyz_idx(ux, uy, uz, rx, ry, rz, indexes):
    """
    Pairwise Euclidean distance computation for periodic systems returning
    distance vectors, pair indices, and projected coordinates.
    """
    m = [-1, 0, 1]
    n = len(ux)
    nn = 27*n*(n - 1)//2
    dx = np.empty((nn, ), dtype=np.float64)    # Two body distance component x
    dy = np.empty((nn, ), dtype=np.float64)    # within corresponding periodic
    dz = np.empty((nn, ), dtype=np.float64)    # unit cell
    dr = np.empty((nn, ), dtype=np.float64)
    px = np.empty((nn, ), dtype=np.float64)    # Projected j coordinate x
    py = np.empty((nn, ), dtype=np.float64)    # Projected j coordinate y
    pz = np.empty((nn, ), dtype=np.float64)    # Projected j coordinate z
    idxi = np.empty((nn, ), dtype=np.int64)    # index of i
    idxj = np.empty((nn, ), dtype=np.int64)    # index of j
    h = 0
    for i in range(n):
        xi = ux[i]
        yi = uy[i]
        zi = uz[i]
        indexi = indexes[i]
        for j in range(i + 1, n):
            xj = ux[j]
            yj = uy[j]
            zj = uz[j]
            indexj = indexes[j]
            for ii in m:
                for jj in m:
                    for kk in m:
                        pxj = xj + ii*rx
                        pyj = yj + jj*ry
                        pzj = zj + kk*rz
                        dxx = xi - pxj
                        dyy = yi - pyj
                        dzz = zi - pzj
                        dx[h] = dxx
                        dy[h] = dyy
                        dz[h] = dzz
                        px[h] = pxj
                        py[h] = pyj
                        pz[h] = pzj
                        dr[h] = np.sqrt(dxx**2 + dyy**2 + dzz**2)
                        idxi[h] = indexi
                        idxj[h] = indexj
                        h += 1
    return dx, dy, dz, dr, idxi, idxj, px, py, pz
