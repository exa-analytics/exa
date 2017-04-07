# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.units`
#############################################
"""
from unittest import TestCase
from exa import units


class TestUnits(TestCase):
    """Basic checks that units have been created."""
    def test_count(self):
        """Check that all constants have been created."""
        self.assertGreater(len(vars(units)), 230)

    def test_units(self):
        """Check attribute values."""
        self.assertTrue(hasattr(units, "mcd"))
        self.assertAlmostEqual(units.mcd._value, 1000.0)
