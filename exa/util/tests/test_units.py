# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.units`
#############################################
"""
from unittest import TestCase
from exa.util import units


class TestUnits(TestCase):
    """Basic checks that units have been created."""
    def test_count(self):
        """Check that all constants have been created."""
        self.assertTrue(hasattr(units, "Acceleration"))
        self.assertTrue(hasattr(units, "Energy"))

    def test_units(self):
        """Check attribute values."""
        self.assertEqual(units.Energy['J'], 1.0)
