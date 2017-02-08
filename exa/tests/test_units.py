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
from exa.tester import UnitTester
from exa import units


class TestUnits(UnitTester):
    """
    Test that module level imports worked and new values are leveraging Sympy
    correctly.
    """
    def test_clean_namespace(self):
        """Test that importing __all__ worked correctly."""
        self.assertFalse(hasattr(units, "sympy"))
        self.assertFalse(hasattr(units, "units"))

    def test_new_value_class(self):
        """Test that new values share types with Sympy units."""
        self.assertIsInstance(units.atomic_length, (sympy.Mul, sympy.physics.units.Unit))
