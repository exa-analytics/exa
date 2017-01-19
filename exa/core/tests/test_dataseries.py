# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.dataseries`
#############################################
"""
import numpy as np
import pandas as pd
from exa import units
from exa.tester import UnitTester
from exa.core.dataseries import DataSeries
from exa.core.errors import MissingUnits


class TestDataSeries(UnitTester):
    """Tests :class:`~exa.core.dataseries.DataSeries`."""
    def setUp(self):
        self.s0 = pd.Series([0, 1, 2])
        self.s1 = DataSeries([0.0, 1.0, 2.0])
        self.s2 = DataSeries([0, 1, 2], units=units.m)
        self.s3 = DataSeries([0, 1, 2], units=units.km)
        self.s4 = DataSeries([0, 1, 2], units=units.eV)
        self.s5 = DataSeries([9, 0, 1], units=units.km,
                             aliases={"first": 0, "second": 1})

    def test_interop(self):
        """Test interoperability with standard pandas objects."""
        s = self.s0 + self.s1    # __add__
        self.assertIsInstance(s, DataSeries)
        s = self.s1 + self.s0    # __radd__
        self.assertIsInstance(s, DataSeries)
        s = self.s2.as_pandas()
        self.assertIsInstance(s, pd.Series)
        self.assertFalse(hasattr(s, "units"))
        self.assertFalse(s is self.s2)

    def test_no_units(self):
        """See also :mod:`~exa.core.base`."""
        s = self.s0 + self.s1
        self.assertEqual(s.units, self.s1.units)
        self.assertTrue(s.units is None)
        s = self.s1 + self.s0
        self.assertEqual(s.units, self.s1.units)
        self.assertTrue(s.units is None)
        with self.assertRaises(MissingUnits):
            self.s1.asunit(units.m)

    def test_unit_conversion(self):
        """Test unit conversion: :func:`~exa.core.base.Meta.asunit`."""
        s = self.s3.asunit(units.m)
        self.assertTrue(np.allclose(s, [0, 1000, 2000]))

    def test_operations(self):
        """Test that normal operations work even if units don't match."""
        s = self.s0 + self.s2
        self.assertEqual(s.units, self.s2.units)
        s = self.s2 + self.s0
        self.assertEqual(s.units, self.s2.units)
        s = self.s2.asunit(units.km) + self.s3
        self.assertEqual(s.units, units.km)
