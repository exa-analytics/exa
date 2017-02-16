# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.base`
#############################################
Tests for abstract base classes of core data, editor, and container objects.
"""
from uuid import UUID
from exa.tester import UnitTester
from exa.core.base import ABCBase


class Concrete(ABCBase):
    """Concrete implementation using :class:`~exa.core.base.ABCBase`."""
    _getters = ('_get', 'compute')

    def copy(self):
        """This makes the class concrete."""
        return True

    def _get_name(self):
        """Testing method only."""
        self.name = "Name"

    def compute_meta(self):
        """Testing method only."""
        self.meta = [(0, 1), (2, 3)]


class TestBase(UnitTester):
    """
    Test the container's data identification, categorization, and other
    functionality behavior.
    """
    def setUp(self):
        self.concrete = Concrete()

    def test_raises(self):
        """Test ABC behavior of :class:`~exa.core.base.ABCBase`."""
        with self.assertRaises(TypeError):
            ABCBase()

    def test_concrete(self):
        """Because we have a implemented the copy method, it works."""
        self.assertTrue(self.concrete.copy())
        self.assertIsInstance(self.concrete.uid, UUID)

    def test_getter(self):
        """Tests that the metaclass instantiated ``name`` correctly."""
        self.assertEqual(self.concrete.name, "Name")

    def test_compute(self):
        """Tests that overwriting the ``_getters`` attributed works."""
        self.assertIsInstance(self.concrete.meta, dict)
        self.assertEqual(len(self.concrete.meta), 2)
