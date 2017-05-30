# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.typed`
#############################################
Test Exa's abstract base class, which supports strongly typed attributes.
Note that an example of usage of this metaclass is provided by this test.
"""
#import six
#from unittest import TestCase
#from exa.special import (Typed, simple_function_factory, yield_typed, Singleton,
#                         LazyFunction)
#
#
#class MinimalTyped(Typed):
#    """Minimal working example."""
#    foo = int
#
#
#class MinimalClass(six.with_metaclass(MinimalTyped, object)):
#    """Minimal working example."""
#    def __init__(self, foo=None):
#        self.foo = foo
#
#
#class GetterClass(six.with_metaclass(MinimalTyped, MinimalClass)):
#    """Example with custom getter function(s)."""
#    _getters = ("compute", )
#
#    def compute_foo(self, ret=True):
#        """Functions must set the value of foo, but can also return it."""
#        self.foo = 20
#        if ret:
#            return self.foo
#
#
#class AdvancedTyped(MinimalTyped):
#    """Advanced modification of class objects using :mod:`~exa.typed`."""
#    foo = int
#    bar = (str, float)
#
#    def __new__(mcs, name, bases, clsdict):
#        for attr in yield_typed(mcs):
#            f = simple_function_factory("compute_all", "compute", attr[0])
#            clsdict[f.__name__] = f
#        return super(AdvancedTyped, mcs).__new__(mcs, name, bases, clsdict)
#
#
#class AdvancedClass(six.with_metaclass(AdvancedTyped, GetterClass)):
#    """Example advanced use of metaclass features."""
#    def compute_all(self):
#        """Computes both 'bar' and 'foo' attributes."""
#        self.foo = 42
#        self.bar = 42    # Type conversion will occur automatically
#
#    def __init__(self, foo=None, bar=None):
#        self.foo = foo
#        self.bar = bar
#
#
#class TestTyped(TestCase):
#    """
#    Tests the functionality provided in :mod:`~exa.typed` using the example
#    classes (and metaclasses) provided above.
#    """
#    def test_mwe(self):
#        """Test minimal working example."""
#        mwe = MinimalClass()
#        self.assertTrue(hasattr(mwe, "_foo"))
#        self.assertTrue(mwe.foo is None)
#        mwe = MinimalClass(2.1)
#        self.assertEqual(mwe.foo, 2)
#        self.assertIsInstance(mwe.foo, int)
#        with self.assertRaises(TypeError):
#            MinimalClass(type)
#
#    def test_gwe(self):
#        """Test the getter example."""
#        gwe = GetterClass()
#        self.assertTrue(gwe._foo is None)
#        gwe.foo = 30
#        self.assertEqual(gwe.foo, 30)
#        gwe = GetterClass(40)
#        self.assertEqual(gwe.foo, 40)
#        value = gwe.compute_foo()
#        self.assertEqual(value, 20)
#        value = gwe.compute_foo(False)
#        self.assertTrue(value is None)
#
#    def test_awe(self):
#        """Test the advanced example."""
#        awe = AdvancedClass()
#        self.assertTrue(hasattr(awe, "_foo"))
#        self.assertTrue(hasattr(awe, "_bar"))
#        awe.foo = 50
#        self.assertEqual(awe.foo, 50)
#        self.assertEqual(awe.bar, "42")
#        del awe.foo
#
#    def test_yield_typed(self):
#        """Test :func:`~exa.typed.yield_typed`."""
#        awe = AdvancedClass()
#        typed = list(yield_typed(awe))
#        self.assertEqual(len(typed), 2)
#        self.assertIsInstance(typed, list)
#        self.assertIsInstance(typed[0], tuple)
#
#
#
#class Single(six.with_metaclass(Singleton, object)):
#    """Example singleton class."""
#    pass
#
#
#class TestSingleton(TestCase):
#    """Tests behavior of :class:`~exa.single.Singleton`."""
#    def test_presence(self):
#        """Test that the singleton is registered."""
#        Single()    # Must create an instance of the singleton
#        self.assertIn(Single, Singleton._singletons)
#
#    def test_singleton(self):
#        """Test that singleton character."""
#        self.assertIs(Single(), Single())
#
#
#class TestLazyFunction(TestCase):
#    """Tests behavior of :class:`~exa.special.LazyFunction`."""
#    def setUp(self):
#        """Used to check for laziness."""
#        self.check = False
#
#    def test_args(self):
#        """Test evaluation of args."""
#        f = LazyFunction(lambda x: x**2, 10)
#        self.assertEqual(f(), 100)
#
#    def test_kwargs(self):
#        """Test evaluation of kwargs."""
#        f = LazyFunction(lambda x: x**2, x=2)
#        self.assertEqual(f(), 4)
#
#    def test_repr(self):
#        """Test repr."""
#        f = LazyFunction(lambda x: x**2, 10)
#        text = repr(f)
#        self.assertIsInstance(text, six.string_types)
#
#    def test_laziness(self):
#        """Test for lazy evaluation."""
#        def concrete_function(x):    # Used to check for laziness
#            self.check = True
#            return x**2
#
#        self.assertFalse(self.check)
#        f = LazyFunction(concrete_function, x=10)
#        self.assertFalse(self.check)
#        result = f()
#        self.assertTrue(self.check)
#        self.assertEqual(result, 100)
