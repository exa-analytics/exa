# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.errors`
##################################
"""
from exa.tester import UnitTester
from exa.errors import ExaException


class TestExceptions(UnitTester):
    """
    Test that base exceptions can be raised.
    """
    def test_generic(self):
        """
        Test for :class:`~exa.errors.ExaException`.
        """
        with self.assertRaises(ExaException):
            raise ExaException()
