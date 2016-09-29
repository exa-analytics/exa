# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.cms.base`
#############################################
"""
from exa.tester import UnitTester
from exa.cms.base import generate_hexuid


class TestBaseModel(UnitTester):
    """Test the base model for database tables."""
    def test_generate_hexuid(self):
        """Test :func:`~exa.cms.base.generate_hexuid`."""
        hexuid = generate_hexuid()
        self.assertEqual(len(hexuid), 32)
