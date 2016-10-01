# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.compute.compilers.wrapper`
########################################################
"""
from exa.tester import UnitTester
from exa.compute.compilers.wrapper import (compile_function, available_compilers,
                                           resources, returns)


class TestWrapper(UnitTester):
    """Tests for :mod:`~exa.compute.compilers.wrapper`."""
    def test_available_compilers(self):
        """Test :func:`~exa.compute.compilation.available_compilers`."""
        self.assertIsInstance(list(available_compilers()), list)
        self.assertTrue("none" in available_compilers())

    def test_no_compilation(self):
        """
        Test no compilation in :func:`~exa.compute.compilation.compile_function`.
        """
        func = lambda x: not x
        sig, func1 = compile_function(func, (bool, ), compiler='none')
        self.assertEqual(sig, ("cpu", "ram", "serial", bool))
        self.assertTrue(func1 is func)

    def test_mia_compiler(self):
        """
        Test raising KeyError when missing compiler selected in
        :func:`~exa.compute.compilation.available_compilers`.
        """
        with self.assertRaises(KeyError):
            compile_function(lambda x: not x, (bool, ), compiler='__mia__')

    def test_returns(self):
        """Test :func:`~exa.compute.compilers.wrapper.returns`."""
        try:
            @returns(bool)
            def fn1(arg):
                return arg

            @returns(str, int)
            def fn2(arg):
                return arg, arg
        except Exception as e:
            self.fail(str(e))
        self.assertIsInstance(fn1(0), bool)
        self.assertIsInstance(fn1(1), bool)
        self.assertEqual(fn1(0), False)
        self.assertEqual(fn1(1), True)
        values = fn2(0)
        self.assertIsInstance(values[0], str)
        self.assertIsInstance(values[1], int)
        self.assertEqual(fn2(0), ("0", 0))
        self.assertEqual(fn2(1), ("1", 1))
