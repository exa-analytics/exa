# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Abstract Base Class for Data Objects
######################################
This module provides abstract base classes for two `pandas`_ like data
objects, dataseries and dataframe objects. In the context of Exa, dataseries
objects are single valued n-dimensional arrays. Dataframes are multiply valued
n-dimensional arrays. The are called :class:`~exa.core.dataseries.DataSeries`
and :class:`~exa.core.dataframe.DataFrame`, respectively. The latter can be
thought of as collections of former having the same dimensions. Classes
provided by Exa are interoperable with pure `pandas`_ objects.

See Also:
    See :class:`~exa.core.dataseries.DataSeries` and
    :class:`~exa.core.dataframe.DataFrame` for additional features.

.. _pandas: http://pandas.pydata.org
"""
import six
import numpy as np
from pandas.core.ops import _op_descriptions
from abc import abstractproperty, abstractmethod
from exa.core.errors import MissingUnits
from exa.typed import Meta


class PandasDataObjectMeta(Meta):
    """
    Metaclass for data objects.

    Modifies all operations to ensure that metadata and types are propagated
    correctly.
    """
    @classmethod
    def _modify_op(cls, op):
        """Modifies mathematical operations to return correctly typed objects."""
        def wrapper(self, other, *args, **kwargs):
            """Ensure we return an Exa data object type."""
            return self.__finalize__(getattr(super(cls, self), op)(other, *args, **kwargs))
        return wrapper

    def __new__(mcs, name, bases, clsdict):
        for opname, info in _op_descriptions.items():
            if opname == None:
                continue
            op = "__{}__".format(opname)
            clsdict[op] = mcs._modify_op(op)
            if info['reverse'] is not None:
                op = "__{}__".format(info['reverse'])
                clsdict[op] = mcs._modify_op(op)
        return super(PandasDataObjectMeta, mcs).__new__(mcs, name, bases, clsdict)


class PandasDataObject(six.with_metaclass(PandasDataObjectMeta, object)):
    """
    """
    @abstractproperty
    def _constructor(self):
        """Required for metadata propagation."""
        pass

    def __finalize__(self, other, method=None, **kwargs):
        """Pandas metadata propatation solution."""
        for name in self._metadata:
            object.__setattr__(self, name, getattr(other, name, None))
        return self

#
#    @classmethod
#    def _init(cls):
#        """Modify class operations and update indexers."""
#        for name, info in _op_descriptions.items():
#            if name == None:
#                continue
#            op = "__{}__".format(name)
#            setattr(cls, op, cls._modify_op(op))
#            if info['reverse'] is not None:
#                op = "__{}__".format(info['reverse'])
#                setattr(cls, op, cls._modify_op(op))
