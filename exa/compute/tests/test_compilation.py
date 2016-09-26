# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.compute.compilation`
########################################################
"""
from exa.tester import UnitTester
from exa.compute.compilation import compile_function, available_compilers


class TestCompilation(UnitTester):
    """
    """
    def test_available_compilers(self):
        """Test :func:`~exa.compute.compilation.available_compilers`."""
        self.assertIsInstance(list(available_compilers()), list)

    def test_no_compilation(self):
        """Test """
        pass
