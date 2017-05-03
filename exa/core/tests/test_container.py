# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.container`
#############################################
"""
from unittest import TestCase
from exa.core import Container


class TestContainer(TestCase):
    """
    Test the container's data identification, categorization, and other
    functionality behavior.
    """
    def test_basic(self):
        """Test an empty container."""
        c = Container()
        self.assertIsInstance(c, Container)
        name = "name"
        meta = {"description": "description"}
        c = Container(name=name)
        self.assertEqual(c.name, name)
        c = Container(name=name, meta=meta)
        self.assertEqual(c.name, name)
        self.assertEqual(c.meta, meta)

    def test_with_generic_data(self):
        """Test a container with normal data."""
        pass
