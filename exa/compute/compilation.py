# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Dispatched Function Compilation
##################################
This module provides a mechanism for automatically compiling dispatched
functions for use as part of a :class:`~exa.prc.workflow.Workflow`.

See Also:
    :mod:`~exa.prc.dispatch`
"""
try:                      # If numba is not present then this module does
    import numba as nb    # not perform compilation.
except ImportError:
    nb = None


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
