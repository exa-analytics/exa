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



class TestSeries(Series):
    """Tests for :class:`~exa.core.discrete.Series`."""
    def setUp(self):
        self.series0 = Series(np.random.rand(10))
        self.series1 = Series(np.random.rand(10))
        self.series2 = CustomSeries(np.random(10))
