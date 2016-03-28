# -*- coding: utf-8 -*-
'''
Just-in-Time Compiled Loop-Based Algorithms
=============================================
'''
from numba import jit
from exa.algorithms.iteration import pdist, supercell3


nb_pdist = jit(nopython=True, cache=True)(pdist)

nb_supercell3 = jit(nopython=True, cache=True)(supercell3)
