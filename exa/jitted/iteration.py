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
def periodic_supercell(xyz, rx, ry, rz):
    '''
    Creates a 3x3x3 (super) cell from a primitive cell.

    Args:
        xyz (:class:`~numpy.ndarray`): Array of xyz values
        rx (float): Cell magnitude in x
        ry (float): Cell magnitude in y
        rz (float): Cell magnitude in z
    '''
    multipliers = [-1, 0, 1]
    n = len(xyz)
    periodic = np.empty((n * 27, 3), dtype=float64)
    h = 0
    for i in multipliers:
        for j in multipliers:
            for k in multipliers:
                for l in range(n):
                    periodic[h, 0] = xyz[l, 0] + i * rx
                    periodic[h, 1] = xyz[l, 1] + j * ry
                    periodic[h, 2] = xyz[l, 2] + k * rz
                    h += 1
    return periodic


@jit(nopython=True, cache=True)
def pdist2d(xyz):
    '''
    '''
    n, m = xyz.shape
    nn = n * (n - 1) // 2
    distances = np.empty((nn, ), dtype=float64)
    h = 0
    for i in range(n):
        for j in range(i + 1, n):
            csum = 0.0
            for k in range(m):
                csum += (xyz[i, k] - xyz[j, k])**2
            distances[h] = csum**0.5
            h += 1
    return distances



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


@jit(nopython=True, cache=True)
def repeat_f8_array2d_by_counts(array, counts):
    '''
    '''
    n, m = array.shape
    nn = np.sum(counts)
    result = np.empty((nn, m), dtype=float64)
    h = 0
    for i in range(n):
        values = array[i]
        count = counts[i]
        for j in range(count):
            for k in range(m):
                result[h, k] = values[k]
            h += 1
    return result
