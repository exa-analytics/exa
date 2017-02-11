# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.core.errors`
##################################
"""
from exa.tester import UnitTester
from exa.core.errors import UnitsError, MissingUnits, NoParsers, NoSections


class TestCoreExceptions(UnitTester):
    """Tests for core exceptions and errors."""
    def test_raising(self):
        with self.assertRaises(UnitsError):
            raise UnitsError(None, None)
        with self.assertRaises(MissingUnits):
            raise MissingUnits()
        with self.assertRaises(NoParsers):
            raise NoParsers()
        with self.assertRaises(NoSections):
            raise NoSections()
