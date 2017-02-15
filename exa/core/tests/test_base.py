# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.base`
#############################################
"""
from exa.tester import UnitTester
from exa.core.base import Base


class Concrete(Base):
    """Concrete implementation of ABC :class:`~exa.core.base.Base`."""

class TestBase(UnitTester):
    """
    Test the container's data identification, categorization, and other
    functionality behavior.
    """
    def test_raises(self):
        """Test ABC behavior of :class:`~exa.core.base.Base`."""
        with self.assertRaises(TypeError):
            Base()
