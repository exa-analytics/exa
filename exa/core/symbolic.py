# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Symbolic Data Objects
###################################
This module provides a mechanism for working with symbolic data using `sympy`_.

.. _sympy: http://www.sympy.org/en/index.html
"""
import six
import types
import sympy as sy
from exa.compute.compilers.wrapper import compile_function


class Function(sy.Function):
    """Base class for exa's symbolic data objects."""
    def recompile(self):
        fn = sy.lambdify(tuple(self.free_symbols), self, "numpy")
        self._flags["nosig"] = True
        self._compiled[0] = compile_function(fn, *self._itypes, **self._flags)

    @property
    def compiled(self):
        if self._compiled[0] is None:
            self.recompile()
        return self._compiled[0]

    @classmethod
    def new_expression(cls, expression, *itypes, **flags):
        """
        Create a new expression instance.

        Args:
            expression: Any valid sympy expression
        """
        expression.__class__._itypes = itypes
        expression.__class__._flags = flags
        expression.__class__.__call__ = cls.__call__
        expression.__class__.recompile = cls.recompile
        expression.__class__.compiled = cls.compiled
        expression.__class__._compiled = [None]
        return expression

    def __call__(self, *args, **kwargs):
        return self.compiled(*args, **kwargs)
