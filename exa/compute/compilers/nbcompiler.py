# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Compilation Using `Numba`_
#############################
This module provides conversion between exa syntax and `Numba`_ syntax.

.. _Numba: http://numba.pydata.org/
"""
try:
    import numba as nb
except ImportError:
    pass
from exa._config import config


def signature(itypes=None, otypes=None):
    """
    Convert (Python) types to a string signature compatible with Numba types.

    Input types must map 1 to 1 to input arguments. If itypes is a given as a
    string, it will be passed through directly to Numba without processing.
    Similarly, if output types are ommitted, they will be inferred by Numba.

    Args:
        itypes: Input argument types (one type per argument)
        otypes: Return type
    """
    bit64 = False
    if config['dynamic']['64bit'] == 'true':
        bit64 = True



def jit(func, sig=None, nopython=False, nogil=False, cache=False):
    raise NotImplementedError()


def vectorize(func, signatures=None, identity=None, nopython=True, target='cpu'):
    raise NotImplementedError()


def guvectorize(func, signatures, layout, identity=None, nopython=True, target='cpu'):
    raise NotImplementedError()


def compiler(func, *itypes, **flags):
    """Convert generic arguments to numba specific arguments."""
    target = flags.pop("target", "cpu")
    core = flags.pop("core", "ram")
    mp = flags.pop("mp", "serial")
    if mp == "serial":
        func = jit(func)
    return (target, core, mp), func
