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


def projected_unitcell(px, py, pz, rx, ry, rz):
    '''
    Create a 3x3x3 supercell from the coordinates of a unit cell.
    '''
    n = len(px)
    m = [-1, 0, 1]
    xyz = np.empty((n * 27, 3), dtype='f8')
    h = 0
    for i in m:
        for j in m:
            for k in m:
                for l in range(n):
                    xyz[h, 0] = px[l] + i * rx
                    xyz[h, 1] = py[l] + j * ry
                    xyz[h, 2] = pz[l] + k * rz
                    h += 1
    return xyz


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
