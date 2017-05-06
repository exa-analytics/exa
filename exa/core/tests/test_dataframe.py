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


class TestColumnError(TestCase):
    """Test :class:`~exa.core.dataframe.ColumnError`."""
    def test_working(self):
        """Test that the basic arg passing works."""
        self.assertEqual(str(ColumnError("column")), "Missing required column(s): column")

    def test_custom(self):
        """Test that custom messages work."""
        self.assertEqual(str(ColumnError(msg="You forgot column")), "You forgot column")


class MockDataFrame(DataFrame):
    """Test implementation of :class:`~exa.core.dataframe.DataFrame`."""
    _required_columns = ("col1", )
    _col_descriptions = {'col1': "First column"}
    _aliases = {'col1': r"$\frac{col}{1}$"}


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

    def test_info(self):
        """Test that info works."""
        df = MockDataFrame.from_dict({'col1': [0, 1], 'col2': [0, 1]})
        inf = df.info()
        self.assertIsInstance(inf, pd.DataFrame)
        self.assertEqual(len(inf), 2)
        self.assertEqual(inf.iloc[0, 0], "First column")
        self.assertEqual(inf.iloc[0, 1], r"$\frac{col}{1}$")
