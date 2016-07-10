# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Tests for :mod:`~exa.numerical`
#################################
'''
import numpy as np
from exa.test import UnitTester
from exa.numerical import Numerical, Series


#class TestSeries(Series):
#    _precision = 2
#    _sname = 's0'
#
#
#class TestSeries1(Series):
#    '''
#    Series object where the index name is always "idx".
#    '''
#    _precision = 2
#    _sname = 's1'
#    _iname = 's1idx'
#    _index_trait = True
#    _stype = str
#    _itype = np.int64
#
#
#class TestDataFrame(DataFrame):
#    '''
#    Test dataframe object tracks 3D objects of a given shape at
#    a given origin.
#    '''
#    _groupbys = ['group']
#    _indices = ['obj']
#    _columns = ['x', 'y', 'z', 'typ']
#    _traits = ['x', 'y', 'z']
#    _categories = {'group': np.int64, 'typ': str}
#    _precision = {'x': 2, 'y': 2, 'z': 2}
#
#
#class TestField(Field3D):
#    _vprecision = 6

class TestNumerical(UnitTester):
    '''Tests for the base numerical class, :class:`~exa.numerical.Numerical`.'''
    def setUp(self):
        '''Create an instance of the class.'''
        self.numerical = Numerical()

    def test_traits(self):
        '''Check calls to trait creation functions.'''
        traits = self.numerical._custom_traits()
        self.assertIsInstance(traits, dict)
        self.assertTrue(len(traits) == 0)
        traits = self.numerical._update_traits()
        self.assertIsInstance(traits, dict)
        self.assertTrue(len(traits) == 0)


class TestingSeries(Series):
    '''An example usage of the :class:`~exa.numerical.Series` object.'''
    _sname = 'testing'
    _iname = 'index'
    _stype = np.float64
    _itype = np.int64
    _precision = 2


class TestTestingSeries(UnitTester):
    '''Test the :class:`~exa.test.test_numerical.TestingSeries` object.'''
    def setUp(self):
        '''Create an instance of the object to be tested.'''
        self.s = TestingSeries(np.random.rand(10))

    def test_underattr(self):
        '''
        Test to ensure the (class level) underscore attributes (of
        :class:`~exa.test.test_numerical.TestingSeries`) are respected.
        '''
        self.assertTrue(self.s.name == TestingSeries._sname)
        self.assertTrue(self.s.index.name == TestingSeries._iname)
