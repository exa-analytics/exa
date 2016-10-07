# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.compute.compilers.cy`
########################################################
"""
from exa._config import config
from exa.tester import UnitTester


class TestCythonCompiler(UnitTester):
    def setUp(self):
        """Skip all tests if the "cython" package is not installed."""
        if config['dynamic']['cython'] == 'false':
            self.skipTest("Package 'cython' not available.")
