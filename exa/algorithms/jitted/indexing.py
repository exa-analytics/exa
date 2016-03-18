# -*- coding: utf-8 -*-
'''
Indexing Recipes
=====================
'''
from numba import jit, vectorize, int32, int64, float32, float64
from exa.algorithms.indexing import arange1, arange2, unordered_pairing_single


nb_arange1 = jit(nopython=True, cache=True)(arange1)
nb_arange2 = jit(nopython=True, cache=True)(arange2)
nb_unordered_pairing = vectorize([int32(int32, int32),
                                  int64(int64, int64),
                                  float32(float32, float32),
                                  float64(float64, float64)])(unordered_pairing_single)
