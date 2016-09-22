# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Function Compilation
##################################

See Also:
    Often times, compiling individual functions can be sped up via the
    :mod:`~exa.compute.dispatch` module.
"""

def compile_func():
    """
    """
    pass


def compile_jit(func, sig=None, nopython=False, nogil=False, cache=False):
    """
    """
    raise NotImplementedError()


def compile_vectorize(func, signatures=None, identity=None, nopython=True, target='cpu'):
    """
    """
    raise NotImplementedError()


def compile_guvectorize(func, signatures, layout, identity=None, nopython=True,
                        target='cpu'):
    """
    """
    raise NotImplementedError()
