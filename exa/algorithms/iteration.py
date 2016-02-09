# -*- coding: utf-8 -*-
'''
Loop Intensive Algorithms
==================================
'''
from exa import _np as np


def project_coordinates(xyz, rxyz):
    '''
    Generate a 3x3x3 super cell given unit coordinates.

    Args:
        xyz (array): Matrix of unit coordinates
        rxyz (array): Magnitudes by which to project
    '''
    n = xyz.shape[0]
    m = [-1, 0, 1]
    projected = np.empty((n * 27, 3), dtype='f8')
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


def pdist(array):
    '''
    '''
    n, m = array.shape
    nn = n * (n - 1) // 2
    distances = np.empty((nn, ), dtype='f8')
    index1 = np.empty((nn, ), dtype='f8')
    index2 = np.empty((nn, ), dtype='f8')
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
