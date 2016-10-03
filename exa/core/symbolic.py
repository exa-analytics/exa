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
import sympy as sy
from exa.core.typed import TypedMeta


class Meta(TypedMeta):
    """Metaclass for :class:`~exa.core.symbolic.SymbolicFunction`."""
    _getter_prefix = "compile"
    compiled = sy.Expr


class Base(six.with_metaclass(Meta, sy.Function)):
    """Base class for exa's symbolic data objects."""
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

    def __call__(self, *args, **kwargs):
        return self.compiled(*args, **kwargs)


class Function(Base):
    """Symbolic functions"""
    pass
