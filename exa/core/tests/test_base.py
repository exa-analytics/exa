# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.base`
#############################################
Test a simple, concrete implementation of the core abstract base class.
"""
from unittest import TestCase
from exa.core.base import Base
from exa.typed import cta


class Concrete(Base):
    """Example concrete implementation of the abstract base class."""
    foo = cta("foo", dict)
    bar = cta("bar", list)
    baz = cta("baz", str)

    def info(self):
        """Implemented to do nothing."""
        pass


class Foo(Concrete):
    """Concrete base classes can, themselves, be subclassed."""
    def _get_foo(self):
        """Test automatic (lazy) getter with prefix _get."""
        self.foo = {'value': "foo"}

    def compute_bar(self):
        """Test automatic (lazy) getter with prefix compute."""
        self.bar = ["bar"]

    def parse_baz(self):
        """Test automatic (lazy) getter with prefix parse."""
        self.baz = "baz"


class TestBase(TestCase):
    """Test the abstract base class."""
    def test_concrete(self):
        """Test the concrete implementation."""
        c = Concrete()
        self.assertIsInstance(c, Base)
        self.assertTrue(hasattr(c, "info"))
        self.assertIsNone(c.info())
        self.assertIsNone(c.foo)

    def test_args(self):
        """Test that args get attached correctly."""
        c = Concrete(1, 2, 3, 4)
        self.assertTupleEqual(c._args, (1, 2, 3, 4))

    def test_kwargs(self):
        """Test kwargs works correctly."""
        c = Concrete(brick=0, slab=1)
        self.assertTrue(hasattr(c, "brick"))
        self.assertIsInstance(c.brick, int)

    def test_args_kwargs(self):
        """Test both args and kwargs simultaneously."""
        c = Concrete(1, 2, 3, four=4, five=5, six=6)
        self.assertTupleEqual(c._args, (1, 2, 3))
        self.assertTrue(hasattr(c, "four"))
        self.assertEqual(c.four, 4)
        self.assertTrue(hasattr(c, "five"))
        self.assertEqual(c.five, 5)
        self.assertTrue(hasattr(c, "six"))
        self.assertEqual(c.six, 6)

    def test_getters(self):
        """Test that Foo's getters work."""
        c = Foo()
        self.assertDictEqual(c.foo, {'value': "foo"})
        self.assertEquals(c.bar, ["bar"])
        self.assertEqual(c.baz, "baz")
