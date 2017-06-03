# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for Special Functions
#####################################
Test the behavior of lazily evaluated functions.
"""
import six
from unittest import TestCase
from exa.functions import LazyFunction, simple_fn_builder


class TestLazyFunction(TestCase):
    """Tests behavior of :class:`~exa.functions.LazyFunction`."""
    def setUp(self):
        """Used to check for laziness."""
        self.check = False

    def test_args(self):
        """Test evaluation of args."""
        f = LazyFunction(lambda x: x**2, 10)
        self.assertEqual(f(), 100)

    def test_kwargs(self):
        """Test evaluation of kwargs."""
        f = LazyFunction(lambda x: x**2, x=2)
        self.assertEqual(f(), 4)

    def test_repr(self):
        """Test repr."""
        f = LazyFunction(lambda x: x**2, 10)
        text = repr(f)
        self.assertIsInstance(text, six.string_types)

    def test_laziness(self):
        """Test for lazy evaluation."""
        def concrete_function(x):    # Used to check for laziness
            self.check = True
            return x**2

        self.assertFalse(self.check)
        f = LazyFunction(concrete_function, x=10)
        self.assertFalse(self.check)
        result = f()
        self.assertTrue(self.check)
        self.assertEqual(result, 100)


class TestSimpleFunctionFactory(TestCase):
    """Test simple function generation."""
    def test_func_gen(self):
        """Test that the simple factory generates a function."""
        class Klass(object):
            # The fn builder allows us to define newfunc before
            # old func is defined.
            newfunc = simple_fn_builder("newfunc", "oldfunc")

            def oldfunc(self, *args, **kwargs):
                self.oldcalled = True

            def __init__(self):
                self.oldcalled = False

        obj = Klass()
        self.assertFalse(obj.oldcalled)
        obj.oldfunc()
        self.assertTrue(obj.oldcalled)
        obj = Klass()
        self.assertFalse(obj.oldcalled)
        obj.newfunc()
        self.assertTrue(obj.oldcalled)
