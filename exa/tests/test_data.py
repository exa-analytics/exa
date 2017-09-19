# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.data`
#############################################
Test data objects' behavior.
"""
import os
import numpy as np
import pandas as pd
from uuid import uuid4
from tempfile import mkdtemp
from unittest import TestCase
from exa.data import DataSeries, DataFrame
from exa.util.hdf import _spec_name


class _Tester(TestCase):
    """This is a mixin tester - see below for usage."""
    def test_metadata(self):
        """Check that metadata exists."""
        self.assertIsInstance(self.d1.metadata, dict)
        self.assertDictEqual(self.d1.metadata, {'uni': 42})
        with self.assertRaises(TypeError):
            self.d0.metadata = ["universe", 42]

    def test_hdf(self):
        """Test custom writing to hdf (including metadata)."""
        path = os.path.join((mkdtemp(), uuid4().hex))
        self.d1.to_hdf(path, "test")
        self.assertTrue(os.path.exists(path))
        store = pd.HDFStore(path)
        self.assertIn(_spec_name, store)
        df1 = self.d1.__class__.from_hdf(path, "test")
        self.assertDictEqual(df1.metadata, df.metadata)
        self.assertTrue(np.all(df.values == df1.values))


class TestDataSeries(_Tester):
    """Tests for :class:`~exa.data.DataSeries`."""
    def setUp(self):
        self.d0 = DataSeries(np.random.rand(10))
        self.d1 = DataSeries(self.d0, metadata={'uni': 42})

    def test_constructors(self):
        """Test constructor types."""
        self.assertIsInstance(self.d0, DataSeries)
        self.assertIs(type(self.d0), DataSeries)
        self.assertIs(self.d0._constructor, DataSeries)
        self.assertIs(self.d0._constructor_expanddim, DataFrame)
        self.assertIs(self.d0._constructor_pandas, pd.Series)


class TestDataFrame(_Tester):
    """Tests for :class:`~exa.data.DataFrame`."""
    def setUp(self):
        self.d0 = DataFrame(np.random.rand(10, 3))
        self.d1 = DataFrame(self.d0, metadata={'uni': 42})

    def test_constructors(self):
        """Test constructor types."""
        self.assertIsInstance(self.d0, DataFrame)
        self.assertIs(type(self.d0), DataFrame)
        self.assertIs(self.d0._constructor, DataFrame)
        self.assertIs(self.d0._constructor_sliced, DataSeries)
        self.assertIs(self.d0._constructor_pandas, pd.DataFrame)
