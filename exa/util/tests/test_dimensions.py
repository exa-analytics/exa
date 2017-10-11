# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
from unittest import TestCase


class TestDimensions(TestCase):
    def test_null_ops(self):
        """Test that operations on zero dimensions do nothing."""
        null = u"\u2205"
        self.assertEqual(str(angle), null)
        self.assertEqual(str(angle**2), null)
        self.assertEqual(str(1/angle), null)
        self.assertEqual(angle+angle, angle)
        self.assertEqual(angle-angle, angle)

    def test_basic_error(self):
        """Test basic ops raise errors"""
        with self.assertRaises(DimensionsError):
            angle +1

    def test_add(self):
        """Test addition operations."""
        self.assertEqual(str(length+length), "L^1")
        self.assertEqual(time+time, time)
        with self.assertRaises(DimensionsError):
            time + length

    def test_sub(self):
        """Test subtraction."""
        self.assertEqual(str(mass-mass), "M^1")
        self.assertEqual(luminosity-luminosity, luminosity)
        with self.assertRaises(DimensionsError):
            temperature - current

    def test_mul(self):
        """Test multiplication."""
        self.assertEqual(str(amount*amount), "N^2")
        self.assertEqual(str(time*mass*length), "L^1 M^1 T^1")
        self.assertEqual(str(luminosity*current*temperature), "I^1 J^1 Θ^1")

    def test_div(self):
        """Test division."""
        self.assertEqual(str(amount/amount), u"\u2205")
        self.assertEqual(str(time/mass/length), "L^-1 M^-1 T^1")
        self.assertEqual(str(luminosity/current/temperature), "I^-1 J^1 Θ^-1")

    def test_pow(self):
        """Test exponentiation."""
        self.assertEqual(str(amount**2), "N^2")
        self.assertEqual(str(time**-2), "T^-1")
