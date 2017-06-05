# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.typed`
#############################################
Tests for strongly styped class attributes.
"""
import six
from unittest import TestCase
from exa.typed import TypedProperty, yield_typed, Typed


class Klass(Typed):
    """Test static :class:`~exa.typed.TypedPropertyibute` usage."""
    _getters = ("get", )
    foo = TypedProperty(int, sf=lambda self: setattr(self, "count", getattr(self, "count") + 1))
    bar = TypedProperty((str, float), sf="increment")

    def get_foo(self):
        """Automatically populate the attribute."""
        # Typically there will be some computation performed here
        # that typed's value depends on.
        self.foo = 42

    def increment(self):
        """Called by name (``sf``)."""
        self.count += 1

    def __init__(self, foo=None):
        """
        Note that the ``count`` variable is instantiated before the ``typed``
        variable because the ``sf`` function (the lambda function
        above).
        """
        self.count = 0        # Order of assignment matters here!
        self.foo = 42 if foo is None else foo
        self.bar = "42"


class TestTyped(TestCase):
    """
    Test the basic features of :func:`~exa.typed.TypedProperty` and
    :func:`~exa.typed.yield_typed`.
    """
    def test_simple(self):
        """Test the most basic usage."""
        class K(Typed):
            foo = TypedProperty(int)

        k = K()
        self.assertIsInstance(K.foo, property)
        k.foo = "1"
        self.assertEqual(k.foo, 1)
        self.assertIsInstance(k.foo, int)

    def test_automatic_assignment(self):
        """Test that the ``foo`` and ``bar`` are automatically assigned."""
        klass = Klass()
        self.assertEqual(klass.foo, 42)
        self.assertEqual(klass.bar, "42")

    def test_typed_attr(self):
        """Test the attribute behavior."""
        klass = Klass(10)
        self.assertEqual(klass.foo, 10)
        self.assertEqual(klass.count, 2)
        klass.foo = 42
        self.assertEqual(klass.foo, 42)
        self.assertEqual(klass.count, 3)
        klass.bar = "0"
        self.assertEqual(klass.bar, "0")
        self.assertEqual(klass.count, 4)

    def test_type_conversion(self):
        """Test automatic type conversion for ``typed``."""
        klass = Klass("10")
        self.assertIsInstance(klass.foo, int)
        klass = Klass(False)
        self.assertIsInstance(klass.foo, int)
        with self.assertRaises(TypeError):
            klass.foo = "cannot convert to int"

    def test_yielding(self):
        """Test that yielding typed attributes works."""
        yielded = list(yield_typed(Klass))
        self.assertEqual(len(yielded), 2)
        yielded = list(yield_typed(Klass()))
        self.assertEqual(len(yielded), 2)

    def test_distinct(self):
        """Test that two instances do not clash."""
        klass0 = Klass(42)
        klass1 = Klass(10)
        klass1.bar = 42.0
        self.assertEqual(klass0.foo, 42)
        self.assertEqual(klass1.foo, 10)
        self.assertNotEqual(id(klass0.foo), id(klass1.foo))
        self.assertIsNot(klass0.bar, klass1.bar)
        self.assertNotEqual(id(klass0.bar), id(klass1.bar))

    def test_delattr(self):
        """Test that typed attrs can be deleted."""
        klass = Klass()
        self.assertTrue(hasattr(klass, "foo"))
        self.assertEqual(klass.foo, 42)
        del klass.foo
        self.assertFalse(hasattr(klass, "_foo"))
        self.assertTrue(hasattr(klass, "foo"))
        self.assertEqual(klass.foo, 42)    # Automatic get
