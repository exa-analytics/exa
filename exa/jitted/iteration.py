# -*- coding: utf-8 -*-
'''
Loop Intensive Jitted Algorithms
==================================


Warning:
    Not all algorithms are faster than their corresponding numpy/scipy,
    implementations! Continuous testing is required of these functions corresponding
    to improvements those libraries. For example: numpy.ravel is much faster
    than numpy.flatten or custom (jitted) code, but the a custom code
    is faster than numpy.repeat.
'''
from exa import _np as np
from exa.jitted import jit, float64, int64


@jit(nopython=True, cache=True)
def project_coordinates(xyz, rxyz):
    '''
    Generate a 3x3x3 super cell given unit coordinates.

    Args:
        xyz (array): Matrix of unit coordinates
        rxyz (array): Magnitudes by which to project
    '''
    n = xyz.shape[0]
    m = [-1, 0, 1]
    projected = np.empty((n * 27, 3), dtype=float64)
    rx = rxyz[0]
    ry = rxyz[1]
    rz = rxyz[2]
    h = 0
    for i in m:
        for j in m:
            for k in m:
                for l in range(n):
                    projected[h, 0] = xyz[l, 0] + i * rx
                    projected[h, 1] = xyz[l, 1] + j * ry
                    projected[h, 2] = xyz[l, 2] + k * rz
                    h += 1
    return projected


@jit(nopython=False, cache=True)
def pdist(array):
    '''
    '''
    n, m = array.shape
    nn = n * (n - 1) // 2
    distances = np.empty((nn, ), dtype=float64)
    index1 = np.empty((nn, ), dtype=int64)
    index2 = np.empty((nn, ), dtype=int64)
    h = 0
    for i in range(n):
        for j in range(i + 1, n):
            dist = 0.0
            for k in range(m):
                dist += (array[i][k] - array[j][k])**2
            distances[h] = dist**0.5
            index1[h] = i
            index2[h] = j
            h += 1
    return distances, index1, index2


@jit(nopython=True, cache=True)
def repeat_i8(value, n):
    '''
    '''
    values = np.empty((n, ), dtype=int64)
    h = 0
    for i in range(n):
        values[h] = value
        h += 1
    return values


@jit(nopython=True, cache=True)
def repeat_f8(value, n):
    '''
    '''
    values = np.empty((n, ), dtype=float64)
    h = 0
    for i in range(n):
        values[h] = value
        h += 1
    return values


@jit(nopython=True, cache=True)
def repeat_i8_array(array, n):
    '''
    Same operation as numpy.repeat but faster

    See Also:
        :py:func:`~numpy.repeat`
    '''
    nn = len(array)
    values = np.empty((nn * n, ), dtype=int64)
    h = 0
    for value in array:
        for i in range(n):
            values[h] = value
            h += 1
    return values


@jit(nopython=True, cache=True)
def repeat_f8_array(array, n):
    '''
    Same operation as numpy.repeat but faster

    See Also:
        :py:func:`~numpy.repeat`
    '''
    nn = len(array)
    values = np.empty((nn * n, ), dtype=float64)
    h = 0
    for value in array:
        for i in range(n):
            values[h] = value
            h += 1
    return values


#@jit(nopython=True, cache=True)
#def repeat_f8_array2d_by_counts(array, counts):
#    '''
#    '''
#    n, m = array.shape
#    nn = np.sum(counts)
#    result = np.empty((nn, m), dtype=float64)
#    h = 0
#    for i in range(n):
#        values = array[i]
#        count = counts[i]
#        for j in range(count):
#            for k in range(m):
#                result[h, k] = values[k]
#            h += 1
#    return result


@jit(nopython=True, cache=True)
def tile_i8(array, r):
    '''
    '''
    n = len(array)
    result = np.empty((n * r, ), dtype=int64)
    h = 0
    for i in range(r):
        for j in range(n):
            result[h] = array[j]
            h += 1
    return result


@jit(nopython=True, cache=True)
def tile_f8(array, r):
    '''
    '''
    n = len(array)
    result = np.empty((n * r, ), dtype=float64)
    h = 0
    for i in range(r):
        for j in range(n):
            result[h] = array[j]
            h += 1
    return result
