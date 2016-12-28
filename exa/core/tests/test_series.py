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
        self.s0 = pd.Series([0, 1, 2])
        self.s1 = Series([1, 2, 0.2])
        self.s2 = Series([3, 4, 5], units=units.m)
        self.s3 = Series([6, 7, 8], units=units.eV)
        self.s4 = Series([9, 0, 1], units=units.km, aliases={"first": 0,
                                                                  "second": 1})

    def test_interop(self):
        """Test interoperability with standard pandas objects."""
        self.assertIsInstance(self.s0+self.s1, Series)
        self.assertIsInstance(self.s1+self.s0, Series)
        self.assertEqual((self.s0 + self.s2).units, self.s2.units)
        self.assertEqual((self.s2 + self.s0).units, self.s2.units)
