# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
DataSeries
###################################
A `dataseries`_ is a singly valued n-dimensional array. The dimensions of the
object are defined by the shape of the indices.

See Also:
    Multiply valued n-dimensional arrays are called
    :class:`~exa.core.dataframe.DataFrame`s.

.. _dataseries: http://pandas.pydata.org/
"""
import numpy as np
import pandas as pd
from sympy.core.mul import Mul
from sympy.physics.units import Unit
from exa.core.abcdata import PandasDataObject


class DataSeries(PandasDataObject, pd.Series):
    """
    A singly valued n-dimensional array that behaves like the corresponding
    `pandas`_ object, :class:`~pandas.Series`.

    .. _dataseries: http://pandas.pydata.org/
    """
    _getters = ("compute", )
    _metadata = ['name', 'units']

    @property
    def _constructor(self):
        return DataSeries

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
        if self.units is None or not isinstance(self.units, (Mul, Unit)):
            raise MissingUnits()
        f0, u0 = self.units.as_coeff_Mul()
        f1, u1 = unit.as_coeff_Mul()
        new = self.__finalize__(self*np.float64(f0/f1))
        new.units = unit
        return new

    def __init__(self, *args, **kwargs):
        units = kwargs.pop("units", None)
        super(DataSeries, self).__init__(*args, **kwargs)
        self.units = units
