# -*- coding: utf-8 -*-
# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.container`
#######################################
"""
import sys
from unittest import TestCase
import pandas as pd
from exa import Container, TypedMeta, DataFrame, Series


class DummyDataFrame(DataFrame):
    _index = 'index'
    _categories = {'cat': str}
    _columns = ['x', 'y', 'z', 'cat']


class DummySeries(Series):
    _precision = 3
    _sname = 'field'
    _iname = 'value'


class DummyMeta(TypedMeta):
    s0 = DummySeries
    s1 = DummySeries
    df = DummyDataFrame


class DummyContainer(Container, metaclass=DummyMeta):
    pass


class TestContainer(TestCase):
    @classmethod
    def setUpClass(cls):
        x = [0, 0, 0, 0, 0]
        y = [1.1, 2.2, 3.3, 4.4, 5.5]
        z = [0.5, 1.5, 2.5, 3.5, 4.5]
        cat = ['cube', 'sphere', 'cube', 'sphere', 'cube']
        group = [0, 0, 1, 1, 1]
        cls.container = DummyContainer()
        cls.container._test = False
        cls.container.s0 = DummySeries(y)
        cls.container.s1 = DummySeries(cat, dtype='category')
        cls.container.df = pd.DataFrame.from_dict({'x': x, 'y': y, 'z': z, 'cat': cat, 'group': group})
        cls.container._cardinal = "df"

    def test_attributes(self):
        self.assertIsInstance(self.container.s0, DummySeries)
        self.assertIsInstance(self.container.s1.dtype, pd.api.types.CategoricalDtype)
        self.assertIsInstance(self.container.df, DummyDataFrame)

    def test_copy(self):
        cp = self.container.copy()
        self.assertIsNot(self.container, cp)

    def test_concat(self):
        with self.assertRaises(NotImplementedError):
            self.container.concat()

    def test_slice_naive(self):
        c = self.container[[0]].copy()
        self.assertEquals(c.df.shape, (1, 5))

    def test_getsizeof(self):
        size_bytes = sys.getsizeof(self.container)
        self.assertIsInstance(size_bytes, int)
        self.assertTrue(size_bytes > 100)
