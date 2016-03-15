# -*- coding: utf-8 -*-
'''
Tests for :mod:`~exa.relational.constant`
========================================
'''
import numpy as np
import pandas as pd
from exa.test import UnitTester
from exa.relational import Constant


class TestConstant(UnitTester):
    '''
    Check the physical constants table.
    '''
    def test_table(self):
        '''
        Check that the table can be converted to a :class:`~pandas.DataFrame`.
        '''
        self.assertIsInstance(Constant.table(), pd.DataFrame)

    def test_value(self):
        '''
        Check data values.
        '''
        Eh = Constant['Eh']
        self.assertTrue(hasattr(Eh, 'value'))
        self.assertTrue(np.isclose(Eh.value, 4.35974434*10**-18))
