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
from abc import abstractmethod
from exa.tester import UnitTester
from exa.typed import Meta


class MockMeta(Meta):
    """An exmaple usage of :class:`~exa.typed.Typed`."""
    _getters = ("parse", "compute")
    foo = int
    bar = (str, float)
    baz = tuple
    faz = (str, object)


class MockBaseClass(six.with_metaclass(MockMeta)):
    """An example of an abstract base class using :class:`~exa.typed.Meta`."""
    @abstractmethod
    def parse_all(self):
        """Example of an abstract method that requires implementation."""
        pass

    def compute_foo(self):
        self.foo = 42

    def compute_bar(self):
        self.bar = 42.0

    def parse_baz(self):
        self.baz = ("42", 42)

    def parse_faz(self):
        self.faz = "42"

    def __init__(self, foo=None, bar=None, baz=None, faz=None):
        self.foo = foo
        self.bar = bar
        self.baz = baz
        self.faz = faz


class MockSubClass1(MockBaseClass):
    """This class correctly implements the "parse_all" method."""
    def compute_foo(self):
        self.foo = 0

    def compute_bar(self):
        self.bar = "0.0"

    def parse_all(self):
        """
        Example implementation of a subclass that correctly implements the
        required :func:`~exa.tests.test_typed.MockBaseClass.parse_all`.
        """
        return True


class MockSubClass2(MockBaseClass):
    """
    This class does not implement the "parse_all" method. Instantiating this
    class throws a TypeError.
    """
    pass


class TestTyped(UnitTester):
    """
    Tests for :mod:`~exa.typed` via :class:`~exa.tests.test_typed.MockMeta`,
    :class:`~exa.tests.test_typed.MockBaseClass`, and
    :class:`~exa.tests.test_typed.MockSubClass`.
    """
    def setUp(self):
        """Create instances of the mock classes."""
        self.klass = MockSubClass1()

    def test_instance(self):
        """Ensure that TypeError is raised."""
        with self.assertRaises(TypeError):
            MockBaseClass()
        with self.assertRaises(TypeError):
            MockSubClass2()

#    def test_init(self):
##        """Test type enforcement on creation."""
##        DummyClass()
##        with self.assertRaises(TypeError):
##            DummyClass(False, False)
##        with self.assertRaises(TypeError):
##            DummyClass(10, 10, "baz")
##
##    def test_compute_calls(self):
##        """
##        Test default getters (using the _getter_prefix), for example,
##        :func:`~exa.tests.test_typed.DummyClass.compute_foo`.
##        """
##        klass = DummyClass()
##        self.assertEqual(klass.foo, True)
##        self.assertEqual(klass.bar, 42)
##        self.assertEqual(klass.baz, (42, True))
##        self.assertTrue(klass.jaz is None)
##
##    def test_autoconv(self):
##        """
##        Test automatic conversion performed by
##        :func:`~exa.typed.Typed.create_property`.
##        """
##        klass = DummyClass(foo=0, bar=42.0, baz="stuff")
##        self.assertIsInstance(klass.foo, DummyTyped.foo)
##        self.assertIsInstance(klass.bar, DummyTyped.bar)
##        self.assertIsInstance(klass.baz, DummyTyped.baz)
##        self.assertTrue(klass.faz is None)
##        with self.assertRaises(TypeError):
##            klass.bar = DummyClass()
##
