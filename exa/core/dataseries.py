# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
DataSeries
########################
"""
import six
import pandas as pd
from pandas.core.ops import _op_descriptions
from exa.units import _Unit
from .base import ABCBaseMeta, ABCBase


class DataSeriesMeta(ABCBaseMeta):
    """
    Metaclass for the advanced series like object :class:`~exa.core.data.DataSeries`.

    The purpose of this class is to enable metadata and unit specifications for labeled
    arrays with minimal computational overhead. This means that requested mathematical
    operations take precendence over 'correct' propagation of metadata. Metadata is
    never attached to an object (after an operation is performed) unless it had metadata
    before the operation. Metadata is not propogated if objects both objects involved
    in an operation have metadata before the operation. Units are handled separately.

    See Also:
        For a description of unit propagation rules see
        :func:`~exa.core.data.DataSeriesMeta.series_op_with_units`.
    """
    unit = _Unit

    @staticmethod
    def operation_wrapper(op):
        """
        Metadata propagation on operations.

        Args:
            op (str): Private operation name (e.g. __add__)

        Returns:
            f (function): Modified operation to handle objects with units
        """
        def opwrapper(self, other, *args, **kwargs):
            """Wrapper to propagate units."""
            result = getattr(super(DataSeries, self), op)(other, *args, **kwargs)
            if (hasattr(other, "unit") and other.unit is None
                and hasattr(other, "meta") and other.meta is None):
                if isinstance(result, tuple):
                    for i in range(len(result)):
                        result[i].__finalize__(self)
                else:
                    result.__finalize__(self)
            return result
        return opwrapper

    def __new__(mcs, name, bases, clsdict):
        for opname, opdct in _op_descriptions.items():
            if opname is None:
                continue
            prvopname = "__{}__".format(opname)
            clsdict[prvopname] = mcs.operation_wrapper(prvopname)
        return super(DataSeriesMeta, mcs).__new__(mcs, name, bases, clsdict)


class DataSeries(six.with_metaclass(DataSeriesMeta, pd.Series, ABCBase)):
    """
    """
    _metadata = ["name", "uid", "unit", "meta"]

    def asunit(self, unit, copy=True, force=False):
        """
        Convert units of the series.

        Warning:
            Be very careful with the `copy` option.
        """
        if copy:
            result = self.copy()
        else:
            result = self
        if result.unit is None:
            result.unit = unit
        else:
            if not isinstance(self.unit, type(unit)) and force == False:
                raise ValueError("Unit dimensions do not match {} -> {}".format(self.unit, unit))
            result *= unit._value/self.unit._value
            result.unit = unit
        return result

    @property
    def _constructor(self):
        return DataSeries

    def __init__(self, *args, **kwargs):
        name = kwargs.pop("name", None)
        unit = kwargs.pop("unit", None)
        uid = kwargs.pop("uid", None)
        meta = kwargs.pop("meta", None)
        super(DataSeries, self).__init__(*args, **kwargs)
        self.name = name
        self.unit = unit
        self.uid = uid
        self.meta = meta
