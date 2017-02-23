# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.mpl`
#############################################
Tests for matplotlib wrappers.
"""
from unittest import TestCase
from exa.mpl import qualitative, sequential, diverging


class TestMPL(TestCase):
    """Test internal matplotlib configuration."""
    def test_color_palettes(self):
        """Test default color palettes."""
        self.assertTrue(len(qualitative()), 5)
        self.assertTrue(len(sequential()), 5)
        self.assertTrue(len(diverging()), 5)
