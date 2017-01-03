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
from sympy.core.mul import Mul
from collections import MutableMapping
from pandas.core.ops import _op_descriptions
from exa.typed import Typed
from exa.core.errors import UnitsError


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
    """Metaclass for Exa's data objects."""
    aliases = Alias
    units = (Unit, Mul, )

    @staticmethod
    def modify_op(op):
        def op_wrapper(self, other, *args, **kwargs):
            print(op)
            print(other.units)
            print(self.units)
            self.units = getattr(self.units, op)(other.units)
            return getattr(super(self.__class__, self), op)(other, *args, **kwargs).__finalize__(self)
        return op_wrapper

    def __finalize__(self, other, method=None, **kwargs):
        for name in self._metadata:
            object.__setattr__(self, name, getattr(other, name, None))
        return self

    def __new__(mcs, name, bases, clsdict):
        for op_name, info in _op_descriptions.items():
            op = "__{}__".format(op_name)
            clsdict[op] = mcs.modify_op(op)
            if info['reverse'] is not None:
                op = "__{}__".format(info['reverse'])
                clsdict[op] = mcs.modify_op(op)
        clsdict['__finalize__'] = mcs.__finalize__
        return super(Meta, mcs).__new__(mcs, name, bases, clsdict)
