# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.typed`
#############################################
Test strongly typed class attributes. A usage example is provided by the
combination of :class:`~exa.tests.test_typed.DummyTyped` and
:class:`~exa.tests.test_typed.DummyClass`.
"""
import six
from exa.tester import UnitTester
from exa.typed import Typed


class DummyTyped(Typed):
    """Dummy metaclass."""
    foo = int
    bar = (str, float)
    baz = tuple
    faz = str
    jaz = object


class DummyClass(six.with_metaclass(DummyTyped, object)):
    """Dummy typed class."""
    _getter_prefix = "compute"
    def compute_foo(self):
        return True

    def compute_bar(self):
        return 42

    def compute_baz(self):
        return (42, True)

    def __init__(self, foo=None, bar=None, baz=None, faz=None):
        self.foo = foo
        self.bar = bar
        self.baz = baz
        self.faz = faz


class TestTyped(UnitTester):
    """
    Test :class:`~exa.typed` using dummy classes. Type definitions are
    given in :class:`~exa.tests.test_typed.DummyTyped` and the class
    definition is given by :class:`~exa.tests.test_typed.DummyClass`.
    """
    def test_init(self):
        """Test type enforcement on creation."""
        DummyClass()
        with self.assertRaises(TypeError):
            DummyClass(False, False)
        with self.assertRaises(TypeError):
            DummyClass(10, 10, "baz")

    def test_compute_calls(self):
        """
        Test default getters (using the _getter_prefix), for example,
        :func:`~exa.tests.test_typed.DummyClass.compute_foo`.
        """
        klass = DummyClass()
        self.assertEqual(klass.foo, True)
        self.assertEqual(klass.bar, 42)
        self.assertEqual(klass.baz, (42, True))
        self.assertTrue(klass.jaz is None)

    def test_autoconv(self):
        """
        Test automatic conversion performed by
        :func:`~exa.typed.Typed.create_property`.
        """
        klass = DummyClass(foo=0, bar=42.0, baz="stuff")
        self.assertIsInstance(klass.foo, DummyTyped.foo)
        self.assertIsInstance(klass.bar, DummyTyped.bar)
        self.assertIsInstance(klass.baz, DummyTyped.baz)
        self.assertTrue(klass.faz is None)
        with self.assertRaises(TypeError):
            klass.bar = DummyClass()
