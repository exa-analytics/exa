# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.base`
#############################################
"""
from exa.tester import UnitTester
from exa.core.base import ABCBase


class Concrete(ABCBase):
    """Concrete implementation using :class:`~exa.core.base.ABCBase`."""
    pass


class TestBase(UnitTester):
    """
    Test the container's data identification, categorization, and other
    functionality behavior.
    """
    def test_raises(self):
        """Test ABC behavior of :class:`~exa.core.base.ABCBase`."""
        with self.assertRaises(TypeError):
            ABCBase()
