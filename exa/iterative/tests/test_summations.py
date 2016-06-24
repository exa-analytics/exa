# -*- coding: utf-8 -*-
'''
Tests for summations
############################
Provides tests for :mod:`~exa.distributed.iterative.summations`
'''
import numpy as np
from exa.test import UnitTester
from exa.iterative.summations import (_product_sum_2f_py, product_sum_2f)


np.random.seed(1)


class TestProductSum(UnitTester):
    '''
    Tests for all "product_sum_*" functions in
    :mod:`~exa.distributed.iterative.summations`.
    '''
    expected = np.array([0.71935458, 0.5637779, 0.5093606, 1.02265707, 0.86708038,
                         0.81266309, 0.30244695, 0.14687027, 0.09245297])
    a = np.random.rand(3)
    b = np.random.rand(3)

    def test_product_sum_2f_py(self):
        '''
        Test the python version of
        :func:`~exa.distributed.iterative.summations.product_sum_2f`.
        '''
        self.assertTrue(np.allclose(self.expected, _product_sum_2f_py(self.a, self.b)))

    def test_product_sum_2f(self):
        '''
        Test of :func:`~exa.distributed.iterative.summations.product_sum`.
        '''
        self.assertTrue(np.allclose(self.expected, product_sum_2f(self.a, self.b)))
