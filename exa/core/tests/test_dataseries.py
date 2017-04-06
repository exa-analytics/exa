# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.dataseries`
#############################################
"""
import numpy as np
from unittest import TestCase
from exa.units import km, m, eV
from exa.core.dataseries import DataSeries


class TestDataSeries(TestCase):
    """Ensure behavior of DataSeries mimics pandas."""
    def test_asunit(self):
        """Test unit conversions."""
        values = np.array([1.2, 3.4, 5.6])
        eseries = DataSeries(values, unit=km)
        eseries1 = eseries.asunit(m)
        self.assertTrue(np.all(eseries1 == values*1000))
        self.assertIsInstance(eseries1, DataSeries)
        self.assertEqual(eseries1.unit, m)
        with self.assertRaises(ValueError):
            eseries.asunit(eV)
        eseries1 = eseries.asunit(eV, force=True)
        self.assertTrue(np.all(eseries1 == values*eV._value/km._value))
        self.assertIsInstance(eseries1, DataSeries)
        self.assertEqual(eseries1.unit, eV)
