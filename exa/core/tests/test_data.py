# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.data`
#############################################
Test data objects' behavior.
"""
import os
import numpy as np
import pandas as pd
from uuid import uuid4
from tempfile import mkdtemp
from unittest import TestCase
from exa.core.data import (DataSeries, DataFrame, SparseDataSeries,
                           SparseDataFrame, Index, Column, _Param)


# Some simple Param tests
class FooSeries(DataSeries):
    idx = Index()


class FooMSeries(DataSeries):
    idx0 = Index(level=0)
    idx1 = Index(level=1)


class FooFrame(DataFrame):
    idx = Index()
    a0 = Column(int, required=True)
    b1 = Column((float, str))


class FooFrame(DataFrame):
    idx0 = Index(int, level=0)
    idx1 = Index(str, level=1)
    a0 = Column(int, required=True)
    b1 = Column((float, str))


# Testers (_Tester is a mixin with some 'universal' tests)
class _Tester(TestCase):
    """This is a mixin tester - see below for usage."""
    def test_meta(self):
        """Check that meta exists."""
        self.assertIsInstance(self.d1.meta, dict)
        self.assertDictEqual(self.d1.meta, {'uni': 42})
        with self.assertRaises(TypeError):
            self.d0.meta = ["universe", 42]

    def test_pdcons(self):
        """Test that the pandas constructor is correct."""
        self.assertIsInstance(self.d0, self.d0._constructor_pandas)

    def test_hdf(self):
        """Test custom writing to hdf (including meta)."""
        path = os.path.join(mkdtemp(), uuid4().hex)
        self.d1.to_hdf(path, "test")
        self.assertTrue(os.path.exists(path))
        df1 = self.d1.__class__.from_hdf(path, "test")
        self.assertDictEqual(df1.meta, self.d1.meta)
        self.assertTrue(np.all(df1.values == self.d1.values))
        os.remove(path)


class TestDataSeries(_Tester):
    """Tests for :class:`~exa.data.DataSeries`."""
    def setUp(self):
        self.d0 = DataSeries(np.random.rand(10))
        self.d1 = DataSeries(self.d0, meta={'uni': 42})

    def test_constructors(self):
        """Test constructor types."""
        self.assertIs(self.d0._constructor, DataSeries)
        self.assertIs(self.d0._constructor_expanddim, DataFrame)

    def test_hdf_append(self):
        """Test appending data."""
        path = os.path.join(mkdtemp(), uuid4().hex)
        self.d1.to_hdf(path, "test", append=True)
        self.d1.to_hdf(path, "test", append=True)
        self.assertTrue(os.path.exists(path))
        df1 = self.d1.__class__.from_hdf(path, "test")
        self.assertEqual(len(df1), 2*len(self.d1))
        self.assertTrue(np.all(df1.values == np.concatenate((self.d1.values, self.d1.values))))
        os.remove(path)

    def test_params(self):
        """Test the params machinery."""
        # Confirm _Param raises (instead of abstract class)
        with self.assertRaises(NotImplementedError):
            _Param().check_type(None)
        s = FooSeries()
        self.assertEqual(s.index.name, "idx")
        index = pd.MultiIndex.from_product([[0, 1, 2], ["green", "purple"]])
        s = FooMSeries(index=index)
        self.assertListEqual(list(s.index.names), ["idx0", "idx1"])

    def test_index_name(self):
        class Foo_(DataSeries):
            idx = Index(auto=False)
        with self.assertRaises(NameError):
            Foo_(index=pd.Index([0, 1, 2], name="things"))


class TestDataFrame(_Tester):
    """Tests for :class:`~exa.data.DataFrame`."""
    def setUp(self):
        self.d0 = DataFrame(np.random.rand(10, 3))
        self.d1 = DataFrame(self.d0, meta={'uni': 42})

    def test_constructors(self):
        """Test constructor types."""
        self.assertIs(self.d0._constructor, DataFrame)
        self.assertIs(self.d0._constructor_sliced, DataSeries)

    def test_hdf_append(self):
        """Test appending data."""
        path = os.path.join(mkdtemp(), uuid4().hex)
        self.d1.to_hdf(path, "test", append=True)
        self.d1.to_hdf(path, "test", append=True)
        self.assertTrue(os.path.exists(path))
        df1 = self.d1.__class__.from_hdf(path, "test")
        self.assertEqual(len(df1), 2*len(self.d1))
        self.assertTrue(np.all(df1.values == np.concatenate((self.d1.values, self.d1.values))))
        os.remove(path)

    def test_params(self):
        """Test params machinery."""
        index = pd.MultiIndex.from_product([[0, 1], ["green", "purple"]])
        s = FooFrame([0, 1, 2, 3], columns=("a0", ), index=index)
        self.assertListEqual(list(s.index.names), ["idx0", "idx1"])
        with self.assertRaises(NameError):
            s = FooFrame(index=index)


class TestSparseDataSeries(_Tester):
    """Tests for :class:`~exa.data.SparseDataSeries`."""
    def setUp(self):
        self.d0 = SparseDataSeries(np.random.rand(10))
        self.d1 = SparseDataSeries(self.d0, meta={'uni': 42})

    def test_constructors(self):
        """Test constructor types."""
        self.assertIs(self.d0._constructor, SparseDataSeries)
        self.assertIs(self.d0._constructor_expanddim, SparseDataFrame)


class TestSparseDataFrame(_Tester):
    """Tests for :class:`~exa.data.SparseDataFrame`."""
    def setUp(self):
        self.d0 = SparseDataFrame(np.random.rand(10, 3))
        self.d1 = SparseDataFrame(self.d0, meta={'uni': 42})

    def test_constructors(self):
        """Test constructor types."""
        self.assertIs(self.d0._constructor, SparseDataFrame)
        self.assertIs(self.d0._constructor_sliced, SparseDataSeries)
