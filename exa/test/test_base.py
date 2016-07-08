# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Basic Tests
##################################
Tests for :mod:`~exa._config`, :mod:`~exa.log`, and the suite of modules in the
test subpackage, :mod:`~exa.test.tester`, etc.
'''
from unittest import TestCase
from configparser import ConfigParser
from exa._config import config
from exa.test import UnitTester
from exa.log import loggers


class TestConfig(UnitTester):
    '''
    Tests for :mod:`~exa._config`.
    '''
    def test_type(self):
        '''
        Check that the config is a :class:`~configparser.ConfigParser` object.
        '''
        self.assertIsInstance(config, ConfigParser)


class TestLog(UnitTester):
    '''
    Tests for :mod:`~exa.log`.
    '''
    def test_logger(self):
        '''
        Check that at least dblog and syslog are present in the loggers.
        '''
        self.assertIn('dblog', loggers)
        self.assertIn('syslog', loggers)


class TestTester(UnitTester):
    '''
    Tests for :mod:`~exa.test.tester`.
    '''
    def test_type(self):
        '''
        Ensure that the tester is an instance of a test case.
        '''
        self.assertIsInstance(self, TestCase)
