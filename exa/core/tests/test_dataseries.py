# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.dataseries`
#############################################
"""
import numpy as np
from unittest import TestCase
from exa.units import km, m, eV, Ha
from exa.core.dataseries import DataSeries


class TestDataSeries(TestCase):
    """Ensure behavior of DataSeries mimics pandas."""
    def setUp(self):
        """Used by multiple tests."""
        self.values = np.array([1.2, 3.4, 5.6])
        self.eseries = DataSeries(self.values, unit=km)
        self.eseries1 = self.eseries.asunit(m)
        self.eseries2 = DataSeries(self.values, unit=eV)

    def test_asunit(self):
        """Test unit conversions."""
        eseries1 = self.eseries.asunit(eV, force=True)
        self.assertTrue(np.all(eseries1 == self.values*eV._value/km._value))
        self.assertIsInstance(eseries1, DataSeries)
        self.assertEqual(eseries1.unit, eV)

    def test_basic(self):
        """Test some basic operations."""
        self.assertTrue(np.all(self.eseries1 == self.values*1000))
        self.assertIsInstance(self.eseries1, DataSeries)
        with self.assertRaises(ValueError):
            self.eseries.asunit(eV)

    def test_divmod(self):
        """This operation returns two objects instead of one."""
        tup = self.eseries.__divmod__(42)
        self.assertEqual(len(tup), 2)
        self.assertIsInstance(tup[0], DataSeries)
        self.assertIsInstance(tup[1], DataSeries)

    def test_not_copy(self):
        """Test modification of units inplace."""
        eseries2 = self.eseries2.copy()
        self.assertEqual(eseries2.unit, eV)
        eseries3 = eseries2.asunit(Ha)
#        self.assertIs(eseries2.values, eseries3.values)
#        self.assertTrue(np.all(eseries2 == eseries3))
        self.assertEqual(eseries3.unit, Ha)
