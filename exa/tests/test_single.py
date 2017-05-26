# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.single`
#############################################
Test that singleton and related classes work as expected.
"""
import six
from unittest import TestCase
from exa.single import Singleton, SharedState


class TestSharedState(TestCase):
    """Test that the shared state paradigm works."""
    def test_sharedness(self):
        """Test that the state is indeed shared."""
        class Shared(SharedState):
            def __init__(self, value=None):
                self.value = value

        obj0 = Shared(1)
        self.assertEqual(obj0.value, 1)
        obj1 = Shared()
        self.assertEqual(obj0.value, None)
        self.assertEqual(obj1.value, None)
        obj1.value = 42
        self.assertEqual(obj0.value, 42)
        self.assertEqual(obj1.value, 42)
        self.assertFalse(obj0 is obj1)
        self.assertIs(obj0.value, obj1.value)
        self.assertNotEqual(id(obj0), id(obj1))
        self.assertEqual(id(obj0.value), id(obj1.value))


class TestSingleton(TestCase):
    """Test that the singleton metaclass behaves correctly."""
    def test_as_type(self):
        """The Singleton class can be used inline like `type`."""
        Klass = Singleton("Klass", (), {})
        instance0 = Klass()
        instance1 = Klass()
        self.assertIsInstance(instance0, Klass)
        self.assertIs(instance0, instance1)
        self.assertEqual(id(instance0), id(instance1))
        self.assertEqual(hash(instance0), hash(instance1))

    def test_as_metaclass(self):
        """Test the singleton metaclass works as a metaclass."""
        class Klass(six.with_metaclass(Singleton, object)):
            pass
        instance0 = Klass()
        instance1 = Klass()
        self.assertIsInstance(Klass, Singleton)
        self.assertIsInstance(instance0, Klass)
        self.assertIs(instance0, instance1)
        self.assertEqual(id(instance0), id(instance1))
        self.assertEqual(hash(instance0), hash(instance1))
