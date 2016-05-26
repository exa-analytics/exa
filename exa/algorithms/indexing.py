# -*- coding: utf-8 -*-
'''
Indexing Recipes and Array Creation
=========================================
Functions related to generating indices.
'''
import numpy as np
from exa import _conf


def arange1(initials, counts):
    '''
    Generate a pseudo-sequential array from initial values and counts.

    >>> import numpy
    >>> initials = numpy.array([0, 4], dtype=numpy.int64)
    >>> counts = numpy.array([4, 5], dtype=numpy.int64)
    >>> values = arange1(initials, counts)
    >>> values[0]
    array([0, 0, 0, 0, 1, 1, 1, 1, 1])
    >>> values[1]
    array([0, 1, 2, 3, 0, 1, 2, 3, 4])
    >>> values[2]
    array([0, 1, 2, 3, 4, 5, 6, 7, 8])

    Args:
        initials (array): Starting points for array generation
        counts (array): Values by which to increment from each starting point

    Returns:
        arrays (tuple): First index, second index, and indices to select, respectively
    '''
    n = np.sum(counts)
    i_idx = np.empty((n, ), dtype=np.int64)
    j_idx = i_idx.copy()
    values = j_idx.copy()
    h = 0
    for i, start in enumerate(initials):
        stop = start + counts[i]
        for j, value in enumerate(range(start, stop)):
            i_idx[h] = i
            j_idx[h] = j
            values[h] = value
            h += 1
    return (i_idx, j_idx, values)


def arange2(initials, count):
    '''
    Generate a pseudo-sequential array from initial values and a single count.

    >>> import numpy
    >>> initials = numpy.array([0, 5], dtype=numpy.int64)
    >>> count = 5
    >>> values = arange2(initials, count)
    >>> values[0]
    array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    >>> values[1]
    array([0, 1, 2, 3, 4, 0, 1, 2, 3, 4])
    >>> values[2]
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    Args:
        initials (array): Starting points for array generation
        count (int): Value by which to increment from each starting points

    Returns:
        arrays (tuple): First index, second index, and indices to select, respectively
    '''
    n = len(initials) * count
    i_idx = np.empty((n, ), dtype=np.int64)
    j_idx = i_idx.copy()
    values = j_idx.copy()
    h = 0
    for i, start in enumerate(initials):
        stop = start + count
        for j, value in enumerate(range(start, stop)):
            i_idx[h] = i
            j_idx[h] = j
            values[h] = value
            h += 1
    return (i_idx, j_idx, values)


def indexes_sc1(starts, counts):
    '''
    Generate piecewise linear (step 1) indices from starting points and counts.

    Args:
        starts (:class:`numpy.ndarray`): Array of starting points
        counts (:class:`numpy.ndarray`): Array of counts (same length as starts)

    Returns:
        indices (tuple): Outer sequential index, inner sequential index, resulting indicies

    Note:
        Typically only the resulting indices will be of interest (third array
        of the returned tuple).
    '''
    n = np.sum(counts)
    outer = np.empty((n, ), dtype=np.int64)
    inner = outer.copy()
    index = inner.copy()
    h = 0
    for i, start in enumerate(starts):
        stop = start + counts[i]
        for j, value in enumerate(range(start, stop)):
            outer[h] = i
            inner[h] = j
            index[h] = value
            h += 1
    return (outer, inner, index)


def indexes_sc2(starts, count):
    '''
    Generate piecewise linear (step 1) indices from starting points and counts.

    Args:
        starts (:class:`numpy.ndarray`): Array of starting points
        count (int): Integer count

    Returns:
        indices (tuple): Outer sequential index, inner sequential index, resulting indicies

    Note:
        Typically only the resulting indices will be of interest (third array
        of the returned tuple).
    '''
    n = len(starts) * count
    outer = np.empty((n, ), dtype=np.int64)
    inner = outer.copy()
    index = inner.copy()
    h = 0
    for i, start in enumerate(starts):
        stop = start + count
        for j, value in enumerate(range(start, stop)):
            outer[h] = i
            inner[h] = j
            index[h] = value
            h += 1
    return (outer, inner, index)


def unordered_pairing(x, y):
    '''
    A `pairing function`_ for unordered (in magnitude) values.

    The pairing value is computed as follows:

    .. math::

        xy + \\text{trunc}\\left(\\frac{\\left(\\left|x - y\\right| -
            1\\right)^{2}}{4}\\right)

    Args:
        x (array): First value array
        y (array): Second value array

    Returns:
        p (array): Pairing function result

    Note:
        This function has a vectorized version that is imported as
        :func:`~exa.algorithms.indexing.unordered_pairing`; use that
        function when working with array data.

    .. _pairing function: http://www.mattdipasquale.com/blog/2014/03/09/unique-unordered-pairing-function/
    '''
    return np.int64(x * y + np.trunc((np.abs(x - y) - 1)**2 / 4))


if _conf['pkg_numba']:
    from numba import jit, vectorize, int32, int64, float32, float64
    arange1 = jit(nopython=True, cache=True)(arange1)
    arange2 = jit(nopython=True, cache=True)(arange2)
    indexes_sc1 = jit(nopython=True, cache=True)(indexes_sc1)
    indexes_sc2 = jit(nopython=True, cache=True)(indexes_sc2)
    unordered_pairing = vectorize([int32(int32, int32), int64(int64, int64),
                                   float32(float32, float32), float64(float64, float64)],
                                   nopython=True)(unordered_pairing)
