# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.util.nbvars`
##################################
"""
import numpy as np
import sympy as sy
import symengine as sge
from numba.errors import TypingError
from unittest import TestCase
from exa.util.nbvars import numbafy


class TestNumbafy(TestCase):
    """
    Test that :func:`~exa.util.nbvars.numbafy` supports strings, and sympy
    and symengine expressions.
    """
    def setUp(self):
        self.sca = 0.1
        self.arr = np.random.rand(10)

    def test_simple_strings(self):
        """Test string functions."""
        fn = "sin(x)/x"
        func = numbafy(fn, "x", compiler="vectorize")
        self.assertTrue(np.allclose(func(self.arr),
                                    np.sin(self.arr)/self.arr))
        func = numbafy(fn, "x", compiler="jit")
        self.assertTrue(np.isclose(func(self.sca),
                                   np.sin(self.sca)/self.sca))

    def test_fail_string(self):
        """Test failure on untyped name."""
        fn = "Sin(x)/x"
        func = numbafy(fn, "x")
        with self.assertRaises(TypingError):
            func(self.sca)

    def test_complex_strings(self):
        """Test more complicated string functions."""
        fn = "arccos(x)/y + exp(-y) + mod(z, 2)"
        func = numbafy(fn, ("x", "y", "z"), compiler="vectorize")
        result = func(self.arr, self.arr, self.arr)
        check = np.arccos(self.arr)/self.arr + np.exp(-self.arr) + np.mod(self.arr, 2)
        self.assertTrue(np.allclose(result, check))
        func = numbafy(fn, ("x", "y", "z"))
        result = func(self.sca, self.sca, self.sca)
        check = np.arccos(self.sca)/self.sca + np.exp(-self.sca) + np.mod(self.sca, 2)
        self.assertTrue(np.isclose(result, check))

    def test_sympy(self):
        """Test sympy expressions."""
        x, y, z = sy.symbols("x y z")
        fn = sy.acos(x)/y + sy.exp(-y) + sy.Mod(z, 2)
        func = numbafy(fn, (x, y, z), compiler="vectorize")
        result = func(self.arr, self.arr, self.arr)
        check = np.arccos(self.arr)/self.arr + np.exp(-self.arr) + np.mod(self.arr, 2)
        self.assertTrue(np.allclose(result, check))

    def test_symengine(self):
        """Test symengine."""
        x, y, z = sge.var("x y z")
        fn = sge.acos(x)/y + sge.exp(-z)
        func = numbafy(fn, (x, y, z), compiler="vectorize")
        result = func(self.arr, self.arr, self.arr)
        check = np.arccos(self.arr)/self.arr + np.exp(-self.arr)
        self.assertTrue(np.allclose(result, check))
