# -*- coding: utf-8 -*-
'''
Tests for :mod:`~exa.relational.unit`
========================================
Test availablility of unit conversions.
'''
import numpy as np
import pandas as pd
from exa.test import UnitTester
from exa.relational import Acceleration, Length


class TestUnit(UnitTester):
    '''
    Check unit conversion tables.
    '''
    def test_table(self):
        '''
        Check that the table can be converted to a :class:`~pandas.DataFrame`.
        '''
        tbl = Acceleration.table()
        self.assertIsInstance(tbl, pd.DataFrame)

    def test_getitem(self):
        '''
        Ensure that conversion factors can be selected from the tables.
        '''
        self.assertTrue(np.isclose(Length['au', 'A'], 0.529, atol=10**-3))
