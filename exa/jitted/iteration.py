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
def periodic_supercell(x, y, z, rx, ry, rz):
    '''
    Creates a 3x3x3 (super) cell from a primitive cell.

    Args:
        x (:class:`~numpy.ndarray`): Array of x values
        y (:class:`~numpy.ndarray`): Array of y values
        z (:class:`~numpy.ndarray`): Array of z values
        rx (float): Cell magnitudes in x
        ry (float): Cell magnitudes in y
        rz (float): Cell magnitudes in z
    '''
    multipliers = [-1, 0, 1]
    n = len(x)
    periodic = np.empty((n * 27, 3), dtype=float64)
    h = 0
    for i in multipliers:
        for j in multipliers:
            for k in multipliers:
                for l in range(n):
                    periodic[h, 0] = x[l] + i * xr
                    periodic[h, 1] = y[l] + j * yr
                    periodic[h, 2] = z[l] + k * zr
                    h += 1
    return periodic


# In units of time (lower is better; i.e. want to be on the left)
# np.ravel < np.flatten < jitted
# jitted < np.repeat
# np.tile =< jitted
@jit(nopython=True, cache=True)
def repeat_int(array, n):
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
def repeat_float(array, n):
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
