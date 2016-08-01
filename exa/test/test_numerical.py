# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.numerical`
#################################
"""
import pandas as pd
import numpy as np
from exa.test import UnitTester
from exa.numerical import Numerical, Series, DataFrame


class TestingSeries(Series):
    """
    Example of subclassing the :class:`~exa.numerical.Series` object, used for
    testing.
    """
    _sname = 'testing'
    _iname = 'index'
    _stype = np.float64
    _itype = np.int64
    _precision = 2


class TestingDF0(DataFrame):
    """
    Basic example of subclassing :class:`~exa.numerical.DataFrame` with no
    traits, relationships, groups, or categories.
    """
    _index = 'index'
    _columns = ['column']


class TestingDF1(DataFrame):
    """
    Example of subclassing the :class:`~exa.numerical.DataFrame` object, used
    for testing.

    Note:
        Integer groupby.
    """
    _groupby = ('group', np.int64)
    _index = 'index'
    _columns = ['column', 'type']
    _traits = ['column']
    _categories = {'type': str}
    _precision = {'column': 2}


class TestingDF2(DataFrame):
    """
    Example of subclassing the :class:`~exa.numerical.DataFrame` object, used
    for testing.

    Note:
        String groupby.
    """
    _groupby = ('group', str)
    _index = 'index'
    _columns = ['x', 'y', 'z', 'type']
    _traits = ['x', 'y', 'z']
    _categories = {'type': np.int64}
    _precision = {'x': 2, 'y': 2, 'z': 2}


class TestNumerical(UnitTester):
    """Tests for the base numerical class, :class:`~exa.numerical.Numerical`."""
    def setUp(self):
        """Create an instance of :class:`~exa.numerical.Numerical` to test."""
        self.numerical = Numerical()

    def test_slice(self):
        """Test :func:`~exa.numerical.Numerical.slice_naive`."""
        with self.assertRaises(AttributeError):
            self.numerical.slice_naive(0)

    def test_custom_traits(self):
        """Test that :func:`~exa.numerica.Numerical._custom_traits` exists."""
        traits = self.numerical._custom_traits()
        self.assertIsInstance(traits, dict)
        self.assertTrue(len(traits) == 0)


class TestTestingSeries(UnitTester):
    """Test the :class:`~exa.test.test_numerical.TestingSeries` object."""
    def setUp(self):
        """Create instance of :class:`~exa.test.test_numerical.TestingSeries`."""
        self.series = TestingSeries(np.random.rand(10))

    def test_underattr(self):
        """
        Test to ensure the (class level) underscore attributes (of
        :class:`~exa.test.test_numerical.TestingSeries`) are respected.
        """
        self.assertTrue(self.series.name == TestingSeries._sname)
        self.assertTrue(self.series.index.name == TestingSeries._iname)

    def test_copy(self):
        """Test :func:`~exa.numerical.Series.copy`."""
        cp = self.series.copy()
        self.assertTrue(np.all(cp == self.series))
        self.assertIsInstance(cp, self.series.__class__)


class TestTestingDF0(UnitTester):
    """
    Test a basic example of an instance of :class:`~exa.numerical.DataFrame`.
    """
    def setUp(self):
        """Create instance of :class:`~exa.test.test_numerical.TestingDF0`."""
        column = np.random.rand(10)
        self.df = TestingDF0.from_dict({'column': column})

    def test_copy(self):
        """Test :func:`~exa.numerical.DataFrame.copy`."""
        cp = self.df.copy()
        self.assertTrue(np.all(cp == self.df))
        self.assertIsInstance(cp, self.df.__class__)


class TestTestingDF1(UnitTester):
    """
    Test an example instance of :class:`~exa.numerical.DataFrame` with groupby.
    """
    def setUp(self):
        """Create instance of :class:`~exa.test.test_numerical.TestingDF1`."""
        column = np.random.rand(10)
        group = [0, 0, 0, 0, 1, 1, 1, 2, 2, 3]
        typ = ['A']*5 + ['B']*5
        self.df = TestingDF1.from_dict({'column': column, 'type': typ, 'group': group})

    def test_copy(self):
        """Test :func:`~exa.numerical.DataFrame.copy`."""
        cp = self.df.copy()
        self.assertTrue(np.all(cp == self.df))
        self.assertIsInstance(cp, self.df.__class__)

    def test_categories(self):
        """Test that categoricals are being handled correctly."""
        self.assertIsInstance(self.df['type'].dtype, pd.types.dtypes.CategoricalDtype)

    def test_traits(self):
        """Test trait generation."""
        traits = self.df._update_traits()
        self.assertIsInstance(traits, dict)
        self.assertIn('testingdf1_column', traits)


class TestTestingDF2(UnitTester):
    """
    Test an example instance of :class:`~exa.numerical.DataFrame` with groupby.
    """
    def setUp(self):
        """Create instance of :class:`~exa.test.test_numerical.TestingDF2`."""
        x = np.random.rand(10)
        y = np.random.rand(10)
        z = np.random.rand(10)
        typ = [0, 0, 0, 0, 1, 1, 1, 2, 2, 3]
        group = ['A']*5 + ['B']*5
        self.df = TestingDF2.from_dict({'x': x, 'y': y, 'z': z, 'type': typ,
                                        'group': group})

    def test_copy(self):
        """Test :func:`~exa.numerical.DataFrame.copy`."""
        cp = self.df.copy()
        self.assertTrue(np.all(cp == self.df))
        self.assertIsInstance(cp, self.df.__class__)

    def test_categories(self):
        """Test that categoricals are being handled correctly."""
        self.assertIsInstance(self.df['type'].dtype, pd.types.dtypes.CategoricalDtype)
        self.assertIsInstance(self.df['group'].dtype, pd.types.dtypes.CategoricalDtype)

    def test_traits(self):
        """Test trait generation."""
        traits = self.df._update_traits()
        self.assertIsInstance(traits, dict)
        self.assertIn('testingdf2_x', traits)
        self.assertIn('testingdf2_y', traits)
        self.assertIn('testingdf2_z', traits)
