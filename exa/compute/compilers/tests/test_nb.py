# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.compute.compilers.nb`
########################################################
"""
from exa._config import config
from exa.tester import UnitTester


class TestNumbaCompiler(UnitTester):
    def setUp(self):
        """Skip all tests if the "numba" package is not installed."""
        if config['dynamic']['numba'] == 'false':
            self.skipTest("Package 'numba' not available.")
