# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.errors`
##################################
"""
from exa.tester import UnitTester
from exa.cms.errors import FileCreationError


class TestExceptions(UnitTester):
    """Test that base exceptions can be raised."""
    def test_raised(self):
        """Test errors in :mod:`~exa.cms.errors` can be raised."""
        with self.assertRaises(FileCreationError):
            raise FileCreationError("null", "null")
