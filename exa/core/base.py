# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Base Class for Data Objects
####################################
Exa's data objects (e.g. :class:`~exa.core.dataseries.DataSeries`) have special
attributes that allow for aliasing column/row names and perform automatic unit
conversion.
"""
import numpy as np
from sympy.core.mul import Mul
from sympy.physics.units import Unit
from collections import MutableMapping
from pandas.core.ops import _op_descriptions
from exa.typed import Meta
from exa.core.errors import UnitsError, MissingUnits


class Aliases(MutableMapping):
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


class Base(Meta):
    """
    Metaclass for data objects.

    Below is an example showing the required properties of the class object:

    .. code-block:: Python

        class DataObject(six.with_metaclass(Base, pandas.SparseDataFrame)):
            @property
            def _constructor(self):
                return DataObject                # Used by __finalize__

            @property
            def _base(self):
                return pandas.SparseDataFrame    # Used by as_pandas

    See Also:
        More examples can be found in the source code:
        :class:`~exa.core.dataseries.DataSeries`,
        :class:`~exa.core.dataframe.DataFrame`
    """
    aliases = Aliases
    units = (Unit, Mul, )

    def as_pandas(self):
        """Return the corresponding pandas object."""
        return self._base(self)

    def asunit(self, unit):
        """
        Convert to new unit.

        .. code-block:: Python

            series = exa.DataSeries([0, 1, 2], units=exa.units.km)
            new = series.asunit(exa.units.m)
            new.values    # prints [0.0, 1000.0, 2000.0]
            new.units     # prints exa.units.m

        Args:
            unit (Unit): Any one of exa.units.*

        Returns:
            obj: Object of the same type with converted values and units attribute
        """
        if not hasattr(self.units, "as_coeff_Mul"):
            raise MissingUnits()
        return self._asunit(unit)

    def _asunit(self, unit):
        """Convert units without error checking."""
        f0, u0 = self.units.as_coeff_Mul()
        f1, u1 = unit.as_coeff_Mul()
        new = (self*np.float64(f0/f1)).__finalize__(self)
        new.units = unit
        return new

    @staticmethod
    def modify_op(op):
        """Modifies mathematical operations to return correctly typed objects."""
        def wrapper(self, other, *args, **kwargs):
            """Ensure we return an Exa data object type."""
            obj = getattr(super(self.__class__, self), op)(other, *args, **kwargs)
            if hasattr(obj, "__finalize__"):
                obj.__finalize__(self)
            return obj
        return wrapper

    def __finalize__(self, other, method=None, **kwargs):
        for name in self._metadata:
            object.__setattr__(self, name, getattr(other, name, None))
        return self

    def __new__(mcs, name, bases, clsdict):
        # Modify math operations
        for op_name, info in _op_descriptions.items():
            op = "__{}__".format(op_name)
            clsdict[op] = mcs.modify_op(op)
            if info['reverse'] is not None:
                op = "__{}__".format(info['reverse'])
                clsdict[op] = mcs.modify_op(op)
        # Attach methods
        clsdict['__finalize__'] = mcs.__finalize__
        clsdict['as_pandas'] = mcs.as_pandas
        clsdict['asunit'] = mcs.asunit
        clsdict['_asunit'] = mcs._asunit
        return super(Base, mcs).__new__(mcs, name, bases, clsdict)
