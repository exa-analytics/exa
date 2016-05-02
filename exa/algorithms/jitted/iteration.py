# -*- coding: utf-8 -*-
'''
Just-in-Time Compiled Loop-Based Algorithms
=============================================
'''
from numba import jit
from exa.algorithms.iteration import pdist, supercell3d, meshgrid3d


nb_pdist = jit(nopython=True, cache=True)(pdist)

nb_supercell3d = jit(nopython=True, cache=True)(supercell3d)

nb_meshgrid3d = jit(nopython=True, cache=True)(meshgrid3d)
