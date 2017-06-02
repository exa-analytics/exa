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
from exa.typed import cta, yield_typed


class Klass(object):
    """Test static :class:`~exa.typed.TypedAttribute` usage."""
    _getters = ("get", )
    typed = cta("typed", int, "an int", lambda self: setattr(self, "count", getattr(self, "count") + 1))

    def get_typed(self):
        """Automatically populate the attribute."""
        # Typically there will be some computation performed here
        # that typed's value depends on.
        self.typed = 42

    def __init__(self, typed=None):
        """
        Note that the ``count`` variable is instantiated before the ``typed``
        variable because the ``setter_finalize`` function (the lambda function
        above).
        """
        self.count = 0        # Order of assignment matters here!
        self.typed = typed


class TestSimpleTyped(TestCase):
    """
    Test the basic features of :func:`~exa.typed.cta` and
    :func:`~exa.typed.yield_typed`.
    """
    def test_typed_attr(self):
        """Test the attribute behavior."""
        klass = Klass(10)
        self.assertEqual(klass.typed, 10)
        self.assertEqual(klass.count, 1)
        klass.typed = 42
        self.assertEqual(klass.typed, 42)
        self.assertEqual(klass.count, 2)

    def test_type_conversion(self):
        """Test automatic type conversion for ``typed``."""
        klass = Klass("10")
        self.assertIsInstance(klass.typed, six.integer_types)
        klass = Klass(False)
        self.assertIsInstance(klass.typed, six.integer_types)

    def test_yielding(self):
        """Test that yielding typed attributes works."""
        yielded = list(yield_typed(Klass))
        self.assertListEqual(yielded, [("typed", Klass.typed)])
        klass = Klass(42)
        yielded = list(yield_typed(klass))
        self.assertListEqual(yielded, [("typed", Klass.typed)])

    def test_automatic_assignment(self):
        """Test that the ``typed`` attribute is automatically assigned."""
        klass = Klass()
        self.assertEqual(klass.typed, 42)

    def test_distinct(self):
        """Test that two instances do not clash."""
        klass0 = Klass(42)
        klass1 = Klass(10)
        self.assertEqual(klass0.typed, 42)
        self.assertEqual(klass1.typed, 10)
