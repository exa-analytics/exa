# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Compilation Using `Numba`_
#############################
This module provides conversion between exa syntax and `numba`_ syntax.

.. _numba: http://numba.pydata.org/
"""
import numba as nb


def jit(func, sig=None, nopython=False, nogil=False, cache=False):
    raise NotImplementedError()


def vectorize(func, signatures=None, identity=None, nopython=True, target='cpu'):
    raise NotImplementedError()


def guvectorize(func, signatures, layout, identity=None, nopython=True, target='cpu'):
    raise NotImplementedError()


def compiler(func, *itypes, **flags):
    """Convert generic arguments to numba specific arguments."""
    raise NotImplementedError()
