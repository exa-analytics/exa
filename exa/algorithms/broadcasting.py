# -*- coding: utf-8 -*-
'''
Numpy Vectorized Universal Functions
======================================
'''
import numpy as np


def vmag3(x, y, z):
    '''
    Compute squared magnitude from vector component arrays.

    Args:
        x (array): First component vector
        y (array): Second component vector
        z (array): Third component vector

    Returns:
        r2 (array): Element-wise squared magnitude (see definition)

    .. math::

        r2 = x^{2} + y^{2} + z^{2}
    '''
    return x**2 + y**2 + z**2


def vdist3(x1, y1, z1, x2, y2, z2):
    '''
    Compute squared distance between two vectors.

    Args:
        x1 (array): First component of vector 1
        y1 (array): Second component of vector 1
        z1 (array): Third component of vector 1
        x2 (array): First component of vector 2
        y2 (array): Second component of vector 2
        z2 (array): Third component of vector 2

    Returns:
        r2 (array): Element-wise squared distance (see definition)

    .. math::

        r2 = (x1 - x2)^{2} + (y1 - y2)^{2} + (z1 - z2)^{2}
    '''
    return (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2
