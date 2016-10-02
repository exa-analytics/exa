# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Symbolic Data Objects
###################################
This module provides a mechanism for working with symbolic data using `sympy`_.
It extens

.. _sympy: http://www.sympy.org/en/index.html
"""
import six
from exa.core.typed import TypedMeta

class SymbolicMeta(TypedMeta):
    """
    """
    pass
    

class SymbolicFunction(six.with_metaclass(TypedMeta, sy.Function)):
    """Base class for exa's symbolic function system."""
    def recompile(self):
        self._compiled =


    def compiled(self):
        """Compile the discrete function representation."""
        if not hasattr("sel")
        func = self.lambdify()
        self._compiled = self.lambdify

    def __call__(self, *args, **kwargs):
        return self.compiled(*args, **kwargs)
        f = self.compile_function
        func = self.lambdify(recompile)
        return func(*args, **kwargs)

    @classmethod
    def new_expression(cls, expression, *itypes, **kwargs):
        """
        Create a new expression instance.

        Args:
            expression: Any valid sympy expression
        """

        expression.__class__._itypes = itypes
        expression.__class__.__call__ = cls.__call__
        return expression
import sympy as sy
from numba import vectorize, jit


class SymbolicFunction(sy.Function):
    """
    Base class for symbolic functions.
    """
# This should use new compilation machinery
#    def lambdify(self, recompile=False):
#        """
#        Compile the function for discrete evaluation.
#        """
#        if self._discrete_func is None or recompile == True:
#            npfunc = sy.lambdify(sorted(self.free_symbols), self, 'numpy')
#            if self._compile_type == "jit":
#                self._discrete_func = jit(nopython=True)(npfunc)
#            elif self._compile_type == "vectorize":
#                self._discrete_func = vectorize([], nopython=True)(npfunc)
#            else:
#                raise NotImplementedError()
#        return self._discrete_func

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
        expression.__class__._compile_type = compile_type
        expression.__class__._signature = signature
        expression.__class__.__call__ = cls.__call__
        return expression
