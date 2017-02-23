# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.single`
#############################################
Singletons are class objects that only ever instantiate a single object instance.
"""
import six
from unittest import TestCase
from exa.single import Singleton


class Single(six.with_metaclass(Singleton, object)):
    """Example singleton class."""
    pass


class TestSingleton(TestCase):
    """Tests behavior of :class:`~exa.single.Singleton`."""
    def setUp(self):
        self.obj0 = Single()
        self.obj1 = Single()

    def test_presence(self):
        """Test that the singleton is registered."""
        self.assertIn(Single, Singleton._singletons)

    def test_singleton(self):
        """Test that singleton character."""
        self.assertTrue(self.obj0 is self.obj1)
