# -*- coding: utf-8 -*-
'''
Base Tests
##################################
Tests for :mod:`~exa._setup`, :mod:`~exa.log`, and the suite of modules in the
test subpackage, :mod:`~exa.test.tester`, etc.
'''
from configparser import ConfigParser
from exa._setup import config
from exa.test import UnitTester


class TestSetup(UnitTester):
    '''
    Tests for :mod:`~exa._setup`
    '''
    def test_type(self):
        '''
        Check that the config is a :class:`~configparser.ConfigParser` object.
        '''
        self.assertIsInstance(config, ConfigParser)
