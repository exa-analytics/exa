# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.typed`
#############################################
"""
import six
from unittest import TestCase
from exa.typed import Typed, typed, TypedClass, TypedMeta


@typed
class Foo0(object):
    """Test for decoration implementation."""
    bar = Typed(int)

    def __init__(self, bar):
        self.bar = bar


class Foo1(six.with_metaclass(TypedMeta, object)):
    """Test metaclass use."""
    bar = Typed(int)

    def __init__(self, bar):
        self.bar = bar


class Foo2(TypedClass):
    """Test base class use."""
    bar = Typed(int)

    def __init__(self, bar):
        self.bar = bar


@typed
class Foo3(object):
    bar = Typed(int, autoconv=False)

    def __init__(self, bar):
        self.bar = bar


class TestTyped(TestCase):
    """
    Test the strongly typed infrastructure provided by :mod:`~exa.typed`.
    """
    def test_basic(self):
        """
        Test that the three methods of typed class creation work.
        """
        obj = Foo0(42)
        self.assertIsInstance(obj.bar, int)
        self.assertEqual(obj.bar, 42)
        obj = Foo1(42)
        self.assertIsInstance(obj.bar, int)
        self.assertEqual(obj.bar, 42)
        obj = Foo2(42)
        self.assertIsInstance(obj.bar, int)
        self.assertEqual(obj.bar, 42)

    def test_autoconv(self):
        """Test auto type conversion."""
        obj = Foo0(42.0)
        self.assertIsInstance(obj.bar, int)
        self.assertEqual(obj.bar, 42)
        with self.assertRaises(TypeError):
            Foo0("failure")
        with self.assertRaises(TypeError):
            Foo3("failure")
