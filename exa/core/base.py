# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Abstract Base Class for Data Objects
######################################
"""
import six
import numpy as np
from pandas.core.ops import _op_descriptions
from abc import abstractproperty, abstractmethod
from sympy.core.mul import Mul
from sympy.physics.units import Unit
from exa.typed import Meta
from exa.core.errors import UnitsError, MissingUnits
from exa.core.indexing import indexers


class DataObjectMeta(Meta):
    """Metaclass for the data objects base class."""
    units = (Unit, Mul, )


class DataObject(six.with_metaclass(DataObjectMeta)):
    """An abstract base class for Exa's data objects."""
    @abstractproperty
    def _constructor(self):
        """Required for metadata propagation."""
        pass

    def as_pandas(self):
        """Convert to a pandas object equivalent."""
        return self.__class__.__bases__[1](self)

    def asunit(self, unit):
        """
        Convert the physical units of the array.

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
        if not hasattr(self.units, "as_coeff_Mul") and not isinstance(self.units, dict):
            raise MissingUnits()
        return self._asunit(unit)

    @abstractmethod
    def _asunit(self):
        """Unit conversion function."""
        pass

    def __finalize__(self, other, method=None, **kwargs):
        """Pandas metadata propatation solution."""
        for name in self._metadata:
            object.__setattr__(self, name, getattr(other, name, None))
        return self

    @classmethod
    def _modify_op(cls, op):
        """Modifies mathematical operations to return correctly typed objects."""
        def wrapper(self, other, *args, **kwargs):
            """Ensure we return an Exa data object type."""
            return self.__finalize__(getattr(super(cls, self), op)(other, *args, **kwargs))
        return wrapper

    @classmethod
    def _init(cls):
        """Modify class operations and update indexers."""
        for name, info in _op_descriptions.items():
            if name == None:
                continue
            op = "__{}__".format(name)
            setattr(cls, op, cls._modify_op(op))
            if info['reverse'] is not None:
                op = "__{}__".format(info['reverse'])
                setattr(cls, op, cls._modify_op(op))
        for name, indexer in indexers():       # Calls pandas machinery
            setattr(cls, name, None)           # Need to unreference existing indexer
            cls._create_indexer(name, indexer) # Prior to instantiation new indexer
