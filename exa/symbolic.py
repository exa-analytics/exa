# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Symbolic Data Objects
###################################
Often it is convenient to work with an analytical form of a function prior to
discretizing and computing an approximate solution. This can be particularly
useful where the analytical form of a :class:`~exa.numerical.Field` is known,
but visualization requires evaluation of the field on a discrete grid. This
module provides functionality to support such situations.
"""
import numpy as np
import sympy as sy
from numba import vectorize, jit


class SymbolicFunction(sy.Function):
    """
    Base class for symbolic functions.
    """
    def lambdify(self, recompile=False):
        """
        Compile the function for discrete evaluation.
        """
        if self._discrete_func is None or recompile == True:
            npfunc = sy.lambdify(sorted(self.free_symbols), self, 'numpy')
            if self.compile_type == "jit":
                self._discrete_func = jit(nopython=True)(npfunc)
            elif self.compile_type == "vectorize":
                self._discrete_func = vectorize(nopython=True)(npfunc)
            else:
                raise NotImplementedError()
        return self._discrete_func

    def __call__(self, *args, recompile=False, **kwargs):
        func = self.lambdify(recompile)
        return func(*args, **kwargs)

    @classmethod
    def new_expression(cls, expression, compile_type="jit", signature=None):
        """
        Create a new expression instance.

        Args:
            expression: Any valid sympy expression
            compile_type (str): One of "jit" or "vectorize" corresponding to numba compile type
        """
        expression.__class__.compile_type = compile_type
        expression.__class__.signature = signature
        expression.__class__.__call__ = cls.__call__
        return expression
