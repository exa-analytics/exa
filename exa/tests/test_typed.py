# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.typed`
#############################################
There are a large number of test implementations in the source code of these
tests, which may be helpful for developers.
"""
import six
from unittest import TestCase
from exa.typed import Typed, typed, TypedClass, TypedMeta


# The following are objects used in testing
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


class Foo4(TypedClass):
    bar = Typed(int, allow_none=False)

    def __init__(self, bar):
        self.bar = bar


class Foo5(TypedClass):
    bar = Typed(int, pre_set="pre_set")

    def pre_set(self):
        self.pre_set_called = True
        self.pre_set_bar_value = self.bar

    def __init__(self):
        self.pre_set_called = False


def external_pre_set(foo):
    """
    Test external functions (see Foo6).

    Such functions must accept an instanceo of the
    class as the first (and only) argument.
    """
    foo.pre_set_called = True
    foo.pre_set_bar_value = foo.bar


class Foo6(TypedClass):
    bar = Typed(int, pre_set=external_pre_set)

    def __init__(self):
        self.pre_set_called = False


class Foo7(TypedClass):
    bar = Typed(int, post_set="post_set")

    def post_set(self):
        self.post_set_bar_value = self.bar
        self.post_set_called = True

    def __init__(self):
        self.post_set_called = False


def external_post_set(foo):
    """See external_pre_set."""
    foo.post_set_called = True
    foo.post_set_bar_value = foo.bar


class Foo8(TypedClass):
    bar = Typed(int, post_set=external_post_set)

    def __init__(self):
        self.post_set_called = False


class Foo9(TypedClass):
    bar = Typed(int, pre_get="pre_get")

    def pre_get(self):
        self.pre_get_called = True

    def __init__(self, bar):
        self.bar = bar
        self.pre_get_called = False


def external_pre_get(foo):
    """See external_pre_set."""
    foo.pre_get_called = True


class Foo10(TypedClass):
    bar = Typed(int, pre_get=external_pre_get)

    def __init__(self, bar):
        self.bar = bar
        self.pre_get_called = False


class Foo11(TypedClass):
    """Testing auto-setting."""
    _setters = ("compute", )
    bar = Typed(int)

    def compute_bar(self):
        self.bar = 42


# Testing begins here.
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

    def test_setting_none(self):
        """Test that None is always an acceptable typed value."""
        obj = Foo3(None)
        self.assertIsNone(obj.bar)
        with self.assertRaises(TypeError):
            Foo4(None)

    def test_pre_set(self):
        """Test calling functions prior to set."""
        # Internal pre_set call
        obj = Foo5()
        self.assertFalse(obj.pre_set_called)
        self.assertFalse(hasattr(obj, "pre_set_bar_value"))
        obj.bar = 42
        self.assertTrue(obj.pre_set_called)
        self.assertIsNone(obj.pre_set_bar_value)
        self.assertEqual(obj.bar, 42)
        # External pre_set call
        obj = Foo6()
        self.assertFalse(obj.pre_set_called)
        self.assertFalse(hasattr(obj, "pre_set_bar_value"))
        obj.bar = 42
        self.assertTrue(obj.pre_set_called)
        self.assertIsNone(obj.pre_set_bar_value)
        self.assertEqual(obj.bar, 42)

    def test_post_set(self):
        """Test calling post_set functions."""
        obj = Foo7()
        self.assertFalse(obj.post_set_called)
        self.assertFalse(hasattr(obj, "post_set_bar_value"))
        obj.bar = 42
        self.assertIs(obj.post_set_bar_value, obj.bar)
        self.assertTrue(obj.post_set_called)
        obj = Foo8()
        self.assertFalse(obj.post_set_called)
        self.assertFalse(hasattr(obj, "post_set_bar_value"))
        obj.bar = 42
        self.assertIs(obj.post_set_bar_value, obj.bar)
        self.assertTrue(obj.post_set_called)

    def test_pre_get(self):
        """Test calling pre_get functions."""
        obj = Foo9(42)
        self.assertFalse(obj.pre_get_called)
        self.assertEqual(obj.bar, 42)
        self.assertTrue(obj.pre_get_called)
        obj = Foo10(42)
        self.assertFalse(obj.pre_get_called)
        self.assertEqual(obj.bar, 42)
        self.assertTrue(obj.pre_get_called)

    def test_setters(self):
        """Test _setters works correctly."""
        obj = Foo11()
        self.assertFalse(hasattr(obj, "_bar"))
        self.assertEqual(obj.bar, 42)

