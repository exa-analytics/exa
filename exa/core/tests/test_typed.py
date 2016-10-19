# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.typed`
#############################################
Test strongly typed class attributes. A usage example is provided by the
combination of :class:`~exa.core.tests.test_typed.DummyTypedMeta` and
:class:`~exa.core.tests.test_typed.DummyClass`.
"""
import six
from exa.tester import UnitTester
from exa.core.typed import TypedMeta


class DummyTypedMeta(TypedMeta):
    """Dummy metaclass."""
    foo = int
    bar = (str, float)
    baz = tuple
    faz = str
    jaz = object


class DummyClass(six.with_metaclass(DummyTypedMeta, object)):
    """Dummy typed class."""
    _getter_prefix = "compute"
    def compute_foo(self):
        self._foo = True

    def compute_bar(self):
        self._bar = 42

    def compute_baz(self):
        self._baz = (42, True)

    def __init__(self, foo=None, bar=None, baz=None, faz=None):
        self.foo = foo
        self.bar = bar
        self.baz = baz
        self.faz = faz


class TestTypedMeta(UnitTester):
    """
    Test :class:`~exa.core.typed` using dummy classes. Type definitions are
    given in :class:`~exa.core.tests.test_typed.DummyTypedMeta` and the class
    definition is given by :class:`~exa.core.tests.test_typed.DummyClass`.
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
        :func:`~exa.core.tests.test_typed.DummyClass.compute_foo`.
        """
        klass = DummyClass()
        self.assertEqual(klass.foo, True)
        self.assertEqual(klass.bar, 42)
        self.assertEqual(klass.baz, (42, True))
        with self.assertRaises(AttributeError):
            klass.jaz

    def test_autoconv(self):
        """
        Test automatic conversion performed by
        :func:`~exa.core.typed.TypedMeta.create_property`.
        """
        klass = DummyClass(foo=0, bar=42.0, baz="stuff")
        self.assertIsInstance(klass.foo, DummyTypedMeta.foo)
        self.assertIsInstance(klass.bar, DummyTypedMeta.bar)
        self.assertIsInstance(klass.baz, DummyTypedMeta.baz)
        self.assertTrue(klass.faz is None)
        with self.assertRaises(TypeError):
            klass.bar = DummyClass()
