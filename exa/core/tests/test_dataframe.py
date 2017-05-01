# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.dataframe`
#############################################
"""
import numpy as np
import pandas as pd
from unittest import TestCase
from exa.core.dataframe import DataFrame, ColumnError


class MockDataFrame(DataFrame):
    """Test implementation of :class:`~exa.core.dataframe.DataFrame`."""
    _required_columns = ("col1", )


class TestDataFrame(TestCase):
    """Ensure behavior of DataFrame mimics pandas."""
    def test_series_construction(self):
        """Test that slicing (a series) resolve to correct type."""
        df = DataFrame(np.random.rand(3, 2))
        s = df.loc[:, 0]
        self.assertIsInstance(s, pd.Series)
        s = df.loc[0:2, 0]
        self.assertIsInstance(s, pd.Series)
        s = df[1]
        self.assertIsInstance(s, pd.Series)

    def test_required_columns(self):
        """Test instantiation with/without required columns."""
        df = MockDataFrame.from_dict({'col1': [0, 1], 'col2': [0, 1]})
        self.assertIsInstance(df, DataFrame)
        self.assertIn("col1", df)
        with self.assertRaises(ColumnError):
            MockDataFrame.from_dict({'col2': [0, 1], 'col3': [0, 1]})
