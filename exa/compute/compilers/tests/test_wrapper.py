# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.compute.compilers.wrapper`
########################################################
"""
from exa.tester import UnitTester
from exa.compute.compilers.wrapper import compile_function, available_compilers


class TestCompilation(UnitTester):
    """
    Tests for :mod:`~exa.compute.compilation`
    """
    def test_available_compilers(self):
        """Test :func:`~exa.compute.compilation.available_compilers`."""
        self.assertIsInstance(list(available_compilers()), list)

    def test_no_compilation(self):
        """
        Test no compilation in :func:`~exa.compute.compilation.compile_function`.
        """
        func = lambda x: not x
        sig, func1 = compile_function(func, (bool, ), compiler='none')
        self.assertEqual(sig, (0, 0, 0, bool))
        self.assertTrue(func1 is func)

    def test_mia_compiler(self):
        """
        Test raising KeyError when missing compiler selected in
        :func:`~exa.compute.compilation.available_compilers`.
        """
        with self.assertRaises(KeyError):
            compile_function(lambda x: not x, (bool, ), compiler='__mia__')
