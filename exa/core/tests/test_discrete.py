# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.discrete`
#############################################
Tests for discrete data objects.
"""
import numpy as np
from exa.tester import UnitTester
from exa.core.discrete import Series


class CustomSeries(Series):
    """Test subclassing of :class:`~exa.core.discrete.Series`."""
    pass


class TestSeries(UnitTester):
    """Tests for :class:`~exa.core.discrete.Series`."""
    def setUp(self):
        pass
        #self.series0 = Series(np.random.rand(10), metadata={"name": "s0"})
        #self.series1 = Series(np.random.rand(10), metadata={"name": "s1"})
        #self.series2 = CustomSeries(np.random.rand(10), metadata={"name": "s2"})

    def test_copy(self):
        """
        Test that copying (:func:`~exa.core.discrete.Series.copy`) returns the
        correct type.
        """
        #obj0 = self.series0.copy()
        #obj1 = self.series2.copy()
        #self.assertFalse(obj0 is self.series0)
        #self.assertFalse(obj1 is self.series2)
        #self.assertIsInstance(obj0, Series)
        #self.assertIsInstance(obj1, CustomSeries)

    def test_combine_const(self):
        """Test metadata propagation through adding constants."""
        #obj0 = self.series0 + 1
        #obj1 = self.series1 + 1.0
        #obj2 = self.series1*2.0
        #self.assertEqual(obj0.metadata['name'], 's0')
        #self.assertEqual(obj1.metadata['name'], 's1')
        #self.assertEqual(obj2.metadata['name'], 's2')
