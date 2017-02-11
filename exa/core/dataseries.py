# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
DataSeries
###################################
DataSeries objects can correspond to various mathematical
constructs, vectors, matrices, and higher dimensional objects.

See Also:
    http://pandas.pydata.org/
"""
import pandas as pd
from exa.core.abcdata import PandasDataObject


class DataSeries(PandasDataObject, pd.Series):
    """
    """
    def test_method(self):
        return "True!"




##from exa.core.indexing import indexers
#
#
#class DataSeries(DataObject, pd.Series):    # Note the ordering
#    """
#    A series is a single valued n dimensional array.
#
#    Single valued means that a series only carries a single type or column of
#    data (of a specific kind). Each element of the array is labeled by an index.
#    The index can be a single dimension (e.g. an array of integers) or
#    multidimensional. The dimensions of a series are determined by its index.
#    """
#    _getters = ("compute", )
#    _metadata = ['name', 'units']
#
#    @property
#    def _constructor(self):
#        return DataSeries
#
#    def asunit(self, unit):
#        """
#        Convert the physical units of the array.
#
#        .. code-block:: Python
#
#            series = exa.DataSeries([0, 1, 2], units=exa.units.km)
#            new = series.asunit(exa.units.m)
#            new.values    # prints [0.0, 1000.0, 2000.0]
#            new.units     # prints exa.units.m
#
#        Args:
#            unit (Unit): Any one of exa.units.*
#
#        Returns:
#            obj: Object of the same type with converted values and units attribute
#        """
#        if not hasattr(self.units, "as_coeff_Mul") and not isinstance(self.units, dict):
#            raise MissingUnits()
#        return self._asunit(unit)
#
#    def _asunit(self, unit):
#        """Convert units without error checking."""
#        f0, u0 = self.units.as_coeff_Mul()
#        f1, u1 = unit.as_coeff_Mul()
#        new = self.__finalize__(self*np.float64(f0/f1))
#        new.units = unit
#        return new
#
#    def __init__(self, *args, **kwargs):
#        units = kwargs.pop("units", None)
#        super(DataSeries, self).__init__(*args, **kwargs)
#        self.units = units
#
#
#DataSeries._init()
