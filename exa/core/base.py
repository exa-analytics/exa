# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Base Classes for Core Functionality
####################################
Exa's data objects (e.g. :class:`~exa.core.series.Series`, etc.) make use of
custom indexing and math operations provided by the metaclasses in this module.
"""
from sympy.physics.units import Unit
from collections import MutableMapping
from pandas.core.ops import _op_descriptions
from exa.typed import Typed


class Alias(MutableMapping):
    """Dict like object that returns non-existant keys on getitem calls."""
    def __getitem__(self, key):
        if key in self.store:
            return self.store[key]  # "store" contains the aliases
        return key                  # If the key is not found, return it

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # update is defined by MutableMapping

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, str(list(self.items())))


class Meta(Typed):
    """Metaclass for Exa's data objects supporting unit conversions."""
    aliases = Alias
    units = Unit

    @staticmethod
    def modify_op(dunder_op):
        """Modifies mathematical operations to support unit conversions."""
        def wrapper(self, other, *args, **kwargs):
            if isinstance(other, Meta) and self.units != other.units:
                pass
                #other = other.copy()*self.units/other.units
            return getattr(super(mcs, self), dunder_op)(other, *args, **kwargs).__finalize__(self)
        return wrapper

    def __finalize__(self, other, method=None, **kwargs):
        """Propagate metadata."""
        for name in self._metadata:
            object.__setattr__(self, name, getattr(other, name, None))
        return self

    def __new__(mcs, name, bases, clsdict):
        for op, info in _op_descriptions.items():
            op_name = "__{}__".format(op)
            clsdict[op_name] = mcs.modify_op(op_name)
        clsdict['__finalize__'] = mcs.__finalize__
        return super(Meta, mcs).__new__(mcs, name, bases, clsdict)
