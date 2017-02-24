# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.base`
#############################################
Tests for abstract base classes of data, editor, and container objects.
"""
from uuid import UUID
from unittest import TestCase
from exa.core.base import ABCBase, ABCContainer


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


class TestBase(TestCase):
    """
    Test the container's data identification, categorization, and other
    functionality behavior.
    """
    def setUp(self):
        self.concrete = Concrete()
        self.concrete1 = Concrete(metadata1='metadata')

    def test_raises(self):
        """Test ABC behavior of :class:`~exa.core.base.ABCBase`."""
        with self.assertRaises(TypeError):
            ABCBase()
        with self.assertRaises(TypeError):
            ABCContainer()

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

    def test_metadata_kwargs(self):
        """Test that miscellaneous kwargs become part of the metadata."""
        self.assertTrue("metadata1" in self.concrete1.meta)
