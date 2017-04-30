# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.base`
#############################################
Tests for abstract base classes of data, editor, and container objects. Note
that the source code of this module provides minimal working examples for
implementations of the aforementioned objects.
"""
from uuid import UUID
from unittest import TestCase
from exa.core.base import ABCBase, ABCContainer


class ConcreteBase(ABCBase):
    """Concrete implementation using :class:`~exa.core.base.ABCBase`."""
    _getters = ("_get", "compute")

    def info(self):
        """Make this class concrete."""
        pass

    def _get_name(self):
        """Testing method only."""
        self.name = "Name"

    def compute_meta(self):
        """Testing method only."""
        self.meta = [(0, 1), (2, 3)]


class TestBase(TestCase):
    """Test the abstract base class."""
    def setUp(self):
        """Errors if the concrete implementation is incorrect."""
        try:
            self.concrete = ConcreteBase()
        except TypeError:
            self.fail("Abstract method not implemented in ConcreteBase")

    def test_raises(self):
        """Test ABC behavior of :class:`~exa.core.base.ABCBase`."""
        with self.assertRaises(TypeError):
            ABCBase()
        with self.assertRaises(TypeError):
            ABCContainer()

    def test_concrete(self):
        """Because we have a implemented the info method, this works."""
        self.assertIsInstance(self.concrete.uid, UUID)

    def test_getter(self):
        """Tests that the metaclass instantiated ``name`` correctly."""
        self.assertEqual(self.concrete.name, "Name")

    def test_compute(self):
        """Tests that overwriting the ``_getters`` attributed works."""
        self.assertIsInstance(self.concrete.meta, dict)
        self.assertEqual(len(self.concrete.meta), 2)


class ConcreteContainer(ABCContainer):
    """Concrete implementation of the container object for testing."""
    def info(self):
        """Dummy method implementation."""
        pass

    def describe(self):
        """Dummy method implementation."""
        pass

    def _html_repr_(self):
        """Dummy method implementation."""


class TestBaseContainer(TestCase):
    """Test the abstract base container object."""
    def setUp(self):
        """Errors if the concrete implementation is incorrect."""
        try:
            self.concrete = ConcreteContainer()
        except TypeError:
            self.fail("Abstract method not implemented in ConcreteContainer")

    def test_concrete(self):
        """Works because all abstract methods have concrete implementations."""
        self.assertIsInstance(self.concrete.uid, UUID)

    def test_data_properties(self):
        """Test :func:`~exa.core.base.Container._data_properties."""
        dct = self.concrete._data_properties()
        self.assertIsInstance(dct, dict)
