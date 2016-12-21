# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.series`
#############################################
Test the custom Exa series objects.
"""
import pandas as pd
from sympy.physics import units
from exa.tester import UnitTester
from exa.core.series import Series


class TestSeries(UnitTester):
    """Tests :class:`~exa.core.series.Series`."""
    def setUp(self):
        self.series0 = pd.Series([0, 1, 2])
        self.series1 = Series([0, 1, 2])
        self.series2 = Series([3, 4, 5], units=units.m)
        self.series2 = Series([6, 7, 8], units=units.eV)
        self.series3 = Series([9, 0, 1], units=units.km, aliases={"first": 0,
                                                                  "second": 1,
                                                                  "third": 2})

    def test_interop(self):
        """
        """
        pass
