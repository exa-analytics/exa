# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
from unittest import TestCase
from exa.util.dimensions import (angle, mass, length, time, current, amount,
                                 temperature, luminosity, DimensionsError)
from exa.util.dimensions import empty_set_array as esa



class TestDimensions(TestCase):
    def test_angle_ops(self):
        """Test that operations on zero dimensions do nothing."""
        self.assertEqual(angle, esa)
        self.assertEqual(angle**2, esa)
        self.assertEqual(angle/2, esa)
        self.assertEqual(1/angle, esa)
        self.assertEqual(angle*-5, esa)

    def test_raises(self):
        """Test invalid operations."""
        with self.assertRaises(DimensionsError):
            angle + 1
        with self.assertRaises(DimensionsError):
            angle - 1
