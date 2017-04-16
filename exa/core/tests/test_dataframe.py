# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.dataframe`
#############################################
"""
import numpy as np
from unittest import TestCase
from exa.core.dataframe import DataFrame
from exa.core.dataseries import DataSeries


class TestDataFrame(TestCase):
    """Ensure behavior of DataFrame mimics pandas."""
    def test_series_construction(self):
        """Test that slicing (a series) resolve to correct type."""
        df = DataFrame(np.random.rand(3, 2))
        s = df.loc[:, 0]
        self.assertIsInstance(s, DataSeries)
        s = df.loc[0:2, 0]
        self.assertIsInstance(s, DataSeries)
        s = df[1]
        self.assertIsInstance(s, DataSeries)
