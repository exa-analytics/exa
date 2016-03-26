# -*- coding: utf-8 -*-
'''
Just-in-Time Compiled Loop-Based Algorithms
=============================================
'''
from numba import jit
from exa.algorithms.iteration import pdist


nb_pdist = jit(nopython=True, cache=True)(pdist) 
