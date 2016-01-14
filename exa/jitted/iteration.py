# -*- coding: utf-8 -*-
'''
Loop Intensive Jitted Algorithms
==================================
'''
from exa import _np as np
from exa.jitted import jit, float64, int64


@jit(nopython=True, cache=True)
def periodic_supercell(ijk, ei, ej, ek):
    '''
    '''
    multipliers = [-1, 0, 1]
    n = len(ijk)
    periodic = np.empty((n * 27, 3), dtype=float64)
    h = 0
    for i in multipliers:
        for j in multipliers:
            for k in multipliers:
                for l in range(n):
                    periodic[h, 0] = ijk[l, 0] + i * ei
                    periodic[h, 1] = ijk[l, 1] + j * ej
                    periodic[h, 2] = ijk[l, 2] + k * ek
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
