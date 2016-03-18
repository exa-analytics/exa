# -*- coding: utf-8 -*-
'''
Just-in-Time Compiled UFuncs
=======================================
See Also:
    :mod:`~exa.algorithms.broadcasting`
'''
import numpy as np
from numba import vectorize, float64, int32, int64, float32
from exa.algorithms.broadcasting import vmag3, vdist3


nb_vmag3 = vectorize([int32(int32, int32, int32),
                      int64(int64, int64, int64),
                      float32(float32, float32, float32),
                      float64(float64, float64, float64)])(vmag3)


nb_vdist3 = vectorize([int32(int32, int32, int32, int32, int32, int32),
                       int64(int64, int64, int64, int64, int64, int64),
                       float32(float32, float32, float32, float32, float32, float32),
                       float64(float64, float64, float64, float64, float64, float64)])(vdist3)
