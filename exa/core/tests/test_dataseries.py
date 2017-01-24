# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.dataseries`
#############################################
"""
import numpy as np
import pandas as pd
from pandas.core.ops import _op_descriptions
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

    def test_conversion(self):
        """Test conversion to the correct pandas object equivalent."""
        s = self.s1.as_pandas()
        self.assertIsInstance(s, pd.Series)

    def test_asunit(self):
        """Tests for unit conversions."""
        with self.assertRaises(MissingUnits):
            self.s1.asunit(units.m)


# We add test functions dynamically, we could have dynamically created test cases
def create_op_finalize_test(op):
    """This function creates the test below for every operation."""
    def test_op_finalize(self):
        """Test that finalize converts objects correctly on operations."""
        self.assertIsInstance(getattr(self.s1, op)(1), DataSeries)  # constant
        self.assertIsInstance(getattr(self.s1, op)(self.s0), DataSeries)  # pandas
        self.assertIsInstance(getattr(self.s1, op)(self.s2), DataSeries)  # DataSeris
    return test_op_finalize


for name, info in _op_descriptions.items():
    if name == None:
        continue
    op = "__{}__".format(name)
    setattr(TestDataSeries, "test_op_finalize" + op, create_op_finalize_test(op))
    if info['reverse'] is not None:
        op = "__{}__".format(info['reverse'])
        setattr(TestDataSeries, "test_op_finalize" + op, create_op_finalize_test(op))

#    def test_interop(self):
#        """Test interoperability with standard pandas objects."""
#        s = self.s0 + self.s1    # __add__
#        self.assertIsInstance(s, DataSeries)
#        s = self.s1 + self.s0    # __radd__
#        self.assertIsInstance(s, DataSeries)
#        s = self.s2.as_pandas()
#        self.assertIsInstance(s, pd.Series)
#        self.assertFalse(hasattr(s, "units"))
#        self.assertFalse(s is self.s2)

#
#    def test_no_units(self):
#        """See also :mod:`~exa.core.base`."""
#        s = self.s0 + self.s1
#        self.assertEqual(s.units, self.s1.units)
#        self.assertTrue(s.units is None)
#        s = self.s1 + self.s0
#        self.assertEqual(s.units, self.s1.units)
#        self.assertTrue(s.units is None)
#        with self.assertRaises(MissingUnits):
#            self.s1.asunit(units.m)
#
#    def test_unit_conversion(self):
#        """Test unit conversion: :func:`~exa.core.base.Meta.asunit`."""
#        s = self.s3.asunit(units.m)
#        self.assertTrue(np.allclose(s, [0, 1000, 2000]))
#
#    def test_operations(self):
#        """Test that normal operations work even if units don't match."""
#        s = self.s0 + self.s2
#        self.assertEqual(s.units, self.s2.units)
#        s = self.s2 + self.s0
#        self.assertEqual(s.units, self.s2.units)
#        s = self.s2.asunit(units.km) + self.s3
#        self.assertEqual(s.units, units.km)
#
