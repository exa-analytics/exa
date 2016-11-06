# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.discrete`
#############################################
Tests for discrete data objects.
"""
import numpy as np
from exa.tester import UnitTester
from exa.core.discrete import Series


class TestSeries(UnitTester):
    """Tests for :class:`~exa.core.discrete.Series`."""
    def setUp(self):
        self.s0 = Series([1, 2, 3], units="kJ")
        self.s1 = Series([1, 2, 3], units="J")
        self.s2 = Series([1, 2, 3], units="m")

    def test_convert_units(self):
        """Test :func:`~exa.core.discrete.Series.convert_units`."""
        self.assertEqual(self.s0.sum(), 6)
        self.s0.convert_units("J")
        #self.assertEqual(self.s0.sum(), 6000)
        self.assertEqual(self.s0.units, "J")
        self.s0.convert_units("kJ")

    def test_auto_convert_units(self):
        """
        Test automatic unit conversion features (see
        :class:`~exa.core.discrete.DiscreteMeta`).
        """
        pass



class TestDataFrame(UnitTester):
    """
    """
    pass
