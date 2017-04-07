# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.constants`
#############################################
"""
from unittest import TestCase
from exa import constants


class TestConstants(TestCase):
    """Basic checks that constants have been created."""
    def test_count(self):
        """Check that all constants have been created."""
        self.assertGreater(len(vars(constants)), 320)

    def test_constants(self):
        """Check attribute values."""
        self.assertTrue(hasattr(constants, "a220_lattice_spacing_of_silicon"))
        self.assertAlmostEqual(constants.standard_state_pressure.value, 100000.0)
