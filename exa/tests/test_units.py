# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.units`
#############################################
Most of the features in :mod:`~exa.units` should be covered by Sympy's unit
tests: this module focuses on new features and functionality provided by
the Exa package.
"""
import sympy
import sympy.physics
from unittest import TestCase
from exa import units


class TestUnits(TestCase):
    """
    Test that module level imports worked and new values are leveraging Sympy
    correctly.
    """
    def test_exists(self):
        """Test that units were created."""
        self.assertTrue(hasattr(units, "m"))
        self.assertTrue(hasattr(units, "Time"))
        self.assertAlmostEqual(units.m._value, 1.0)
        self.assertAlmostEqual(units.s._value, 1.0)
        self.assertIsInstance(units.m, units.Length)
        self.assertIsInstance(units.s, units.Time)

    def test_can_create(self):
        new = units.Time("new", (), {'_value': 2.0, '_name': "new"})
        self.assertAlmostEqual(new._value, 2.0)
        self.assertEqual(new._name, "new")
        self.assertIsInstance(new, units.Time)
