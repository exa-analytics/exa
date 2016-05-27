# -*- coding: utf-8 -*-
'''
Tests for :mod:`~exa.relational.isotope`
========================================
'''
import pandas as pd
from exa.test import UnitTester
from exa.relational import Isotope


class TestIsotope(UnitTester):
    '''
    Check isotope table
    '''
    def test_table(self):
        '''
        Check that the table can be converted to a :class:`~pandas.DataFrame`.
        '''
        self.assertIsInstance(Isotope.to_frame(), pd.DataFrame)

    def test_selections(self):
        '''
        Check that isotopes can be selected in any manner.
        '''
        self.assertIsInstance(Isotope['1H'], Isotope)
        self.assertIsInstance(Isotope[175], Isotope)
        self.assertIsInstance(Isotope[0], Isotope)
        self.assertIsInstance(Isotope['H'], list)

    def test_data(self):
        '''
        Test the integrity of the database data.
        '''
        self.assertTrue(Isotope['1H'].Z == 1)
