# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.container`
##################################
The :class:`~exa.container.Container` object depends in a complex manner on
much of the functionality of the framework; especially :mod:`~exa.numerical`
and :mod:`~exa.widget`.
"""
import pandas as pd
from exa.container import Container, TypedMeta
from exa.test import UnitTester
from exa.relational.base import BaseMeta
from exa.numerical import DataFrame, Series


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


class TestContainer(UnitTester):
    """
    """
    def setUp(self):
        w = [0, 1, 2, 3, 4]
        x = [0, 0, 0, 0, 0]
        y = [1.1, 2.2, 3.3, 4.4, 5.5]
        z = [0.5, 1.5, 2.5, 3.5, 4.5]
        cat = ['cube', 'sphere', 'cube', 'sphere', 'cube']
        group = [0, 0, 1, 1, 1]
        self.container = DummyContainer()
        self.container._test = False
        self.container.s0 = DummySeries(y)
        self.container.s1 = DummySeries(cat, dtype='category')
        self.container.df = pd.DataFrame.from_dict({'x': x, 'y': y, 'z': z, 'cat': cat, 'group': group})

    def test_attributes(self):
        self.assertIsInstance(self.container.s0, DummySeries)
        self.assertIsInstance(self.container.s1.dtype, pd.types.dtypes.CategoricalDtype)
        self.assertIsInstance(self.container.df, DummyDataFrame)
