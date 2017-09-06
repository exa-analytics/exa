# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.single`
#############################################
"""
from unittest import TestCase
from exa.single import Singleton


class TestSingleton(TestCase):
    """Test :class:`~exa.single.Singleton` uses."""
    def test_singleton(self):
        """Test that Singleton itself is a singleton."""
        a = Singleton()
        b = Singleton()
        self.assertEqual(a, b)
        self.assertIs(a, b)

    def test_simple_implementation(self):
        """Test a simple singleton implementation."""
        class Single(Singleton):
            pass
        a = Singleton()
        b = Single()
        c = Single()
        self.assertNotEqual(a, b)
        self.assertIsNot(a, b)
        self.assertEqual(b, c)
        self.assertIs(b, c)
