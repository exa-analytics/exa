# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.errors`
##################################
"""
from sympy.physics import units
from exa.tester import UnitTester
from exa.core.errors import UnitsError


class TestCoreExceptions(UnitTester):
    """Tests for core exceptions and errors."""
    def setUp(self):
        pass
        #self.s0 = Series([0, 1, 2], units=units.m)
        #self.s1 = Series([3, 4, 5], units=units.eV)

    def test_raisesed(self):
        """Test the error is raised."""
        pass
        #with self.assertRaises(UnitsError):
        #    self.s0 + self.s1
