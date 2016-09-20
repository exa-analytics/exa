# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.typed`
#############################################
"""
import six
from exa.tester import UnitTester
from exa.core.typed import TypedMeta


#class DummyTypedMeta(six.with_metaclass(TypedMeta, type)):
class DummyTypedMeta(TypedMeta):
    """Dummy metaclass."""
    foo = int
    bar = (str, float)
    baz = tuple


#class DummyClass(six.with_metaclass(DummyTypedMeta)):
class DummyClass(six.with_metaclass(DummyTypedMeta, object)):
    """Dummy typed class."""
    _getter_prefix = "compute"
    def compute_foo(self):
        self._foo = True

    def compute_bar(self):
        self._bar = 42

    def compute_baz(self):
        self._baz = (42, True)

    def __init__(self, foo=None, bar=None):
        self.foo = foo
        self.bar = bar


class TestTypedMeta(UnitTester):
    """
    Test :class:`~exa.core.typed` using dummy classes. Type definitions are
    given in :class:`~exa.core.tests.test_typed.DummyTypedMeta` and the class
    definition is given by :class:`~exa.core.tests.test_typed.DummyClass`.
    """
    def test_init(self):
        """Test type enforcement on creation."""
        with self.assertRaises(TypeError):
            klass = DummyClass(False, False)
