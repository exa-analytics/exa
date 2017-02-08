# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.typed`
#############################################
Test Exa's abstract base class, which supports strongly typed attributes.
Note that an example of usage of this metaclass is provided by this test.
"""
import six
from exa.tester import UnitTester
from exa.typed import Meta


class MinimalMeta(Meta):
    """Minimal working example."""
    foo = int


class MinimalClass(six.with_metaclass(MinimalMeta, object)):
    """Minimal working example."""
    def __init__(self, foo=None):
        self.foo = foo


class GetterMeta(MinimalMeta):
    """Example with getters."""
    _getters = ("compute", )


class GetterClass(six.with_metaclass(GetterMeta, MinimalClass)):
    """Example with custom getter function(s)."""
    def compute_foo(self, ret=True):
        """
        Functions of this type may return or set the value of foo.
        """
        if ret:
            return 10
        self.foo = 20


class TestTyped(UnitTester):
    """
    Tests the functionality provided in :mod:`~exa.typed` using the example
    classes (and metaclasses) provided above.
    """
    def test_mwe(self):
        """Test minimal working example."""
        mwe = MinimalClass()
        self.assertTrue(hasattr(mwe, "_foo"))
        self.assertTrue(mwe.foo is None)
        mwe = MinimalClass(2.1)
        self.assertEqual(mwe.foo, 2)
        self.assertIsInstance(mwe.foo, int)
        with self.assertRaises(TypeError):
            MinimalClass(type)

    def test_gwe(self):
        """Test the getter example."""
        gwe = GetterClass()
        self.assertTrue(gwe._foo is None)
        gwe.foo = 30
        self.assertEqual(gwe.foo, 30)
        gwe = GetterClass(40)
        self.assertEqual(gwe.foo, 40)
        value = gwe.compute_foo()
        self.assertEqual(value, 10)
        gwe = GetterClass()
        self.assertEqual(gwe.foo, 10)
        gwe.compute_foo(False)
        self.assertEqual(gwe.foo, 20)
