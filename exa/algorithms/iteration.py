# -*- coding: utf-8 -*-
'''
Loop Intensive Algorithms
==================================
'''
from exa import _np as np


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
    periodic = np.empty((n * 27, 3), dtype='f8')
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


def repeat_f8_array2d_by_counts(array, counts):
    '''
    '''
    n, m = array.shape
    nn = np.sum(counts)
    result = np.empty((nn, m), dtype='f8')
    h = 0
    for i in range(n):
        values = array[i]
        count = counts[i]
        for j in range(count):
            for k in range(m):
                result[h, k] = values[k]
            h += 1
    return result
