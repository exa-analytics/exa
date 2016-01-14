# -*- coding: utf-8 -*-
'''
Vectorized UFuncs
===============================
'''
from exa import _np as np
from exa.jitted import vectorize, float64, int32, int64, float32


@vectorize([int32(int32, int32, int32), int64(int64, int64, int64),
            float32(float32, float32, float32), float64(float64, float64, float64)])
def mag_3d(x, y, z):
    '''
    Computation of magnitude of a three dimensional vector.
    '''
    return (x**2 + y**2 + z**2)**0.5


#
# AS OF NUMBDA 0.22 target='parallel' causes 100% CPU ON WINDOWS???
#
#@vectorize([int32(int32, int32, int32), int64(int64, int64, int64),
#            float32(float32, float32, float32), float64(float64, float64, float64)],
#            target='parallel')
#def mag_3d_p(x, y, z):
#    '''
#    Computation of magnitude of a three dimensional vector (parallelized)
#    '''
#    return (x**2 + y**2 + z**2)**0.5
