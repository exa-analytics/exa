# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Tests for :mod:`~exa.math.misc.summation`
############################################
'''
import string
import random
import numpy as np
from exa.test import UnitTester
from exa.math.misc.summation import sum_product_pair, sum_product_pair_f8


class TestSumProductPair(UnitTester):
    '''
    Tests for all functions name **sum_product_pair\***
    '''
    def setUp(self):
        '''
        Generate a couple of attributes for testing.
        '''
        self.s0 = [random.choice(string.ascii_letters) for i in range(500)]
        self.s1 = [random.choice(string.ascii_letters) for i in range(100)]
        self.n0 = np.random.randint(0, 100, size=(500, ))
        self.n1 = np.random.randint(0, 100, size=(100, ))
        self.f0 = np.random.rand(500)
        self.f1 = np.random.rand(100)

    def test_sum_product_pair(self):
        '''
        Test :func:`~exa.math.misc.summation.sum_product_pair`. This function
        should work regardless of types.
        '''
        r = sum_product_pair(self.s0, self.s0)
        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 250000)
        r = sum_product_pair(self.s0, self.s1)
        self.assertEqual(len(r), 50000)
        self.assertTrue(all(isinstance(rr, str) for rr in r))
        r = sum_product_pair(self.n0, self.n0)
        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 250000)
        r = sum_product_pair(self.n0, self.n1)
        self.assertEqual(len(r), 50000)
        self.assertTrue(all(isinstance(rr, (np.int32, np.int64)) for rr in r))
        r = sum_product_pair(self.f0, self.f0)
        self.assertEqual(len(r), 250000)
        self.assertTrue(all(isinstance(rr, (np.float32, np.float64)) for rr in r))

    def test_sum_product_pair_f8(self):
        '''
        Test :func:`~exa.math.misc.summation.sum_product_pair_f8`. This function
        only works on 64-bit floating point numbers.
        '''
        with self.assertRaises(Exception) as ex:
            sum_product_pair_f8(self.s0, self.s1)
        exnb = 'Failed at nopython'
        exnp = 'could not convert string to float'
        ex = str(ex.exception)
        self.assertTrue(exnb in ex or exnp in ex)
        r = sum_product_pair_f8(self.f0, self.f0)
        self.assertEqual(len(r), 250000)
        self.assertTrue(all(isinstance(rr, np.float64) for rr in r))
        r = sum_product_pair_f8(self.f0, self.f1)
        self.assertEqual(len(r), 50000)
        self.assertTrue(all(isinstance(rr, np.float64) for rr in r))
