# -*- coding: utf-8 -*-
'''
Just-in-time Compiled Operations
======================================
Just-in-time comilation is the process of translation of source code immediately
prior to execution. This module provides a large number of basic operations (
such as addition, division, etc.) that can be applied to dataframes. This can
dramatically speed up these operations compared to typical pandas/numpy
performance.
'''
from exa import _conf
if not _conf['pkg_numba']:
    raise ImportError('JIT compilation requires numba!')
