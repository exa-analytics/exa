# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Compilation Using `Cython`_
#############################
This module provides conversion between exa syntax and `Cython`_ syntax.

.. _cython: http://cython.org/
"""
import cython as cy


def compiler(func, *itypes, **flags):
    raise NotImplementedError()
