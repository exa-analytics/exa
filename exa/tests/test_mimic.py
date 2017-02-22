# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Tests for :mod:`~exa.mimic`
##################################
Tests for mimicked classes
"""
from pandas import DataFrame
from exa.tester import UnitTester
from exa.mimic import Mimic


class TestMimic(UnitTester):
    """Test a small sammpling of mimicked objects."""
    def setUp(self):
        """Sample objects to test."""
        self.sca = 1
        self.lst = ['a', 'b', 3]
        self.tup = ('a', 'b', 3)
        self.dct = {'a': 0, 'b': 1, 3: 2}
        self.cpx = DataFrame()
        self.mc_sca = Mimic(self.sca)
        self.mc_lst = Mimic(self.lst)
        self.mc_tup = Mimic(self.tup)
        self.mc_dct = Mimic(self.dct)
        self.mc_cpx = Mimic(self.cpx)

    def test_sca(self):
        """Test int."""
        self.assertTrue(type(self.mc_sca) == Mimic)
        self.assertIsInstance(self.mc_sca, int)
        self.assertEqual(self.mc_sca.bit_length(), 1)
        self.assertEqual(self.mc_sca, 1)
        self.assertLess(0, self.mc_sca)
        self.assertGreater(2, self.mc_sca)
        self.assertGreaterEqual(1, self.mc_sca)
        self.assertLessEqual(1, self.mc_sca)
        self.assertNotEqual(0, self.mc_sca)
        self.assertEqual(hash(self.mc_sca), hash(self.sca))
        with self.assertRaises(TypeError):
            self.mc_sca.__reduce__()
        with self.assertRaises(TypeError):
            self.mc_sca.__reduce_ex__()
        self.assertEqual(str(self.mc_sca), "1")
        self.assertIsInstance(self.mc_sca.__sizeof__(), int)
        self.assertEqual(repr(self.mc_sca), "1")

    def test_lst(self):
        """Test lists."""
        self.assertTrue(type(self.mc_lst) == Mimic)
        self.assertIsInstance(self.mc_lst, list)
        self.assertTrue(self.mc_lst._obj is self.lst)
        self.mc_lst.append("c")
        self.assertEqual(self.lst[-1], "c")
        self.assertEqual(self.mc_lst[-1], "c")

    def test_tup(self):
        """Test tuples."""
        self.assertTrue(type(self.mc_tup) == Mimic)
        self.assertIsInstance(self.mc_tup, tuple)
        self.assertTrue(self.mc_tup._obj is self.tup)
        count = self.mc_tup.count("a")
        self.assertEqual(count, 1)

    def test_dct(self):
        """Test dictionaries."""
        self.assertTrue(type(self.mc_dct) == Mimic)
        self.assertIsInstance(self.mc_dct, dict)
        self.assertTrue(self.mc_dct._obj is self.dct)
        self.mc_dct[4] = 'd'
        self.assertEqual(self.dct[4], 'd')

    def test_cpx(self):
        """Test complex class."""
        self.assertTrue(type(self.mc_cpx) == Mimic)
        self.assertIsInstance(self.mc_cpx, DataFrame)
        self.assertEqual(len(self.mc_cpx), 0)
        self.mc_cpx.test = None
        self.assertTrue(hasattr(self.cpx, "test"))
        del self.mc_cpx.test
        self.assertFalse(hasattr(self.cpx, "test"))
