# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.assets.unit`
##########################################
"""
import numpy as np
from exa.tester import UnitTester
from exa.assets.unit import Length, Mass


class TestUnit(UnitTester):
    """
    Test different types of unit conversions available in classes such as
    :class:`~exa.assets.unit.Length` and similar.
    """
    def test_length(self):
        """Test :class:`~exa.assets.unit.Length`."""
        self.assertTrue(np.isclose(Length['angstroms', 'au'], 1.88971616463)
        self.assertTrue(np.isclose(Length['km', 'm'], 1000)

    def test_mass(self):
        """Test :class:`~exa.assets.unit.Mass`."""
        self.assertTrue(np.isclose(Mass['amu', 'kg'], 1.66053892e-27)
        self.assertTrue(np.isclose(Mass['kg', 'g'], 100)
