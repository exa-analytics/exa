# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.base`
#############################################
Test Exa's data object metaclass (:class:`~exa.core.base.Meta`) and the indexer
aliasing class (:class:`~exa.core.base.Alias`).
"""
import six
from exa.tester import UnitTester
from exa.core.base import Alias, Meta


class TestAlias(UnitTester):
    """Tests for :class:`~exa.core.base.Alias`."""
    def setUp(self):
        self.alias = Alias(dict([("key0", "alias0"), ("key1", "alias1")]))

    def test_getter(self):
        """Test dictionary getter."""
        self.assertEqual(self.alias['key0'], "alias0")
        self.assertEqual(self.alias['key_'], "key_")

    def test_setter(self):
        """Test dictionary setter."""
        self.alias['key_'] = "alias_"
        self.assertEqual(self.alias['key_'], "alias_")

    def test_del(self):
        """Test dictionary deleter and faux getter."""
        self.alias["del"] = "me"
        self.assertEqual(self.alias["del"], "me")
        del self.alias["del"]
        self.assertEqual(self.alias["del"], "del")

    def test_iter_len(self):
        """Test dictionary iterator."""
        n = len(self.alias)
        for key in self.alias:
            self.assertEqual(len(self.alias), n)


class TestMeta(UnitTester):
    """Tests for :class:`~exa.core.base.Meta`."""
    def setUp(self):
        """Dummy class to test the metaclass."""
        class Klass(six.with_metaclass(Meta)):
            _getter_prefix = "default"
        self.klass = Klass()

    def test_hasattr(self):
        """Test that the aliases attribute is created."""
        self.assertIsNone(self.klass.aliases)
