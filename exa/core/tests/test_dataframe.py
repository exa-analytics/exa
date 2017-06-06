# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.dataframe`
#############################################
Test facilities of the dataframes with required columns. Also test that
dynamically generated information about the dataframe is populated correctly.
"""
import numpy as np
from unittest import TestCase
from exa import DataFrame, Feature
from exa.core.dataframe import SectionDataFrame, Composition


class MockDataFrame(DataFrame):
    """Test implementation of :class:`~exa.core.dataframe.DataFrame`."""
    col1 = Feature(None, True)
    col2 = Feature(str)
    col3 = Feature(float, True)
    col4 = Feature((int, float))
    col5 = Feature((float, int), True)


class TestDataFrame(TestCase):
    """Ensure behavior of DataFrame mimics pandas."""
    def test_basic(self):
        """Test that the base DataFrame can be used as is."""
        df = DataFrame()
        self.assertEqual(len(df.columns), 0)
        df['col'] = [0, 1, 2]
        self.assertEqual(len(df), 3)
        df['col'] *= 2
        self.assertTrue(np.all(df['col'] == [0, 2, 4]))

    def test_basic_meta(self):
        """Test that the additional keyword ``meta`` is handled correctly."""
        df = DataFrame(meta=[("key", True)])
        self.assertTrue(hasattr(df, "_meta"))
        self.assertDictEqual(df.meta, {'key': True})

    def test_mock_reqcols(self):
        """Test required columns work correctly."""
        dct = {'col1': [0, 1], 'col3': [0, 1], 'col5': [0, 1]}
        try:
            MockDataFrame.from_dict(dct)
        except NameError as e:
            self.fail(e)
        with self.assertRaises(NameError):
            del dct['col1']
            MockDataFrame.from_dict(dct)

    def test_mock_coltypes(self):
        """Test that column types are enforced."""
        dct = {'col1': [0, 1], 'col2': [0.0, 0.1], 'col3': [0, 1],
               'col4': [0., 1.], 'col5': [0, 1]}
        df = MockDataFrame.from_dict(dct)
        dtypes = df.dtypes
        self.assertEqual(dtypes['col2'], object)
        self.assertEqual(dtypes['col3'], float)
        self.assertEqual(dtypes['col4'], int)
        self.assertEqual(dtypes['col5'], float)
        df['col2'] = df['col2'].astype(float)
        self.assertEqual(df['col2'].dtype, object)

    def test_info(self):
        """Info is really a function of pandas."""
        try:
            dct = {'col1': [0, 1], 'col3': [0, 1], 'col5': [0, 1]}
            MockDataFrame(dct).info()
        except Exception as e:
            self.fail(str(e))


class TestSectionDataFrame(TestCase):
    """Test :class:`~exa.core.dataframe.SectionDataFrame`."""
    def test_raises(self):
        """Test raises error without required columns."""
        with self.assertRaises(NameError):
            SectionDataFrame()


class TestCompositionDataFrame(TestCase):
    """Test :class:`~exa.core.dataframe.Composition`."""
    def test_raises(self):
        """Test instantiation failure."""
        with self.assertRaises(NameError):
            Composition()
