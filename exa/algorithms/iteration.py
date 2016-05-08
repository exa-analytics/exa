# -*- coding: utf-8 -*-
'''
Loop Intensive Algorithms
==================================
'''
import numpy as np
from exa import _conf


def pdist(array):
    '''
    Compute all pairwise distances of m-dimensional vectors in an array.

    .. math::

        d_{ij} = \\left(\\sum_{m=1}^{M}\\left(v^{i}_{m} - v^{j}_{m}\\right)^{2}\\right)^{\\frac{1}{2}}

    Args:
        array (:class:`~numpy.ndarray`): M-dimensional vectors in an array

    Returns:
        tup (tuple): Tuple of distances, first index, and second index, respectively

    '''
    n, m = array.shape
    nn = n * (n - 1) // 2
    distances = np.empty((nn, ), dtype=np.float64)
    index0 = np.empty((nn, ), dtype=np.int64)
    index1 = np.empty((nn, ), dtype=np.int64)
    h = 0
    for i in range(n):
        for j in range(i + 1, n):
            dist = 0.0
            for k in range(m):
                dist += (array[i][k] - array[j][k])**2
            distances[h] = dist**0.5
            index0[h] = i
            index1[h] = j
            h += 1
    return distances, index0, index1


def supercell3d(x, y, z, rx, ry, rz):
    '''
    Generate a 3x3x3 super cell of coordinates from given unit cell coordinates and cell dimensions.

    Args:
        x (array): First coordinate component
        y (array): Second coordinate component
        z (array): Third coordinate component
        rx (float): First cell dimension
        ry (float): Second cell dimension
        rz (float): Third cell dimension
    '''
    m = [-1, 0, 1]
    n = len(x)
    px = np.empty((n * 27, ), dtype=np.float64)
    py = np.empty((n * 27, ), dtype=np.float64)
    pz = np.empty((n * 27, ), dtype=np.float64)
    h = 0
    for i in m:
        for j in m:
            for k in m:
                for l in range(n):
                    px[h] = x[l] + i * rx
                    py[h] = y[l] + j * ry
                    pz[h] = z[l] + k * rz
                    h += 1
    return px, py, pz


def meshgrid3d(x, y, z):
    '''
    Expand x, y, and z into a volume of len(x) by len(y) by len(z) dimensions.
    '''
    n = len(x) * len(y) * len(z)
    xx = np.empty((n, ), dtype=np.float64)
    yy = np.empty((n, ), dtype=np.float64)
    zz = np.empty((n, ), dtype=np.float64)
    h = 0
    for i in x:
        for j in y:
            for k in z:
                xx[h] = i
                yy[h] = j
                zz[h] = k
                h += 1
    return xx, yy, zz


if _conf['pkg_numba']:
    from numba import jit
    pdist = jit(nopython=True, cache=True)(pdist)
    supercell3d = jit(nopython=True, cache=True)(supercell3d)
    meshgrid3d = jit(nopython=True, cache=True)(meshgrid3d)
