# -*- coding: utf-8 -*-
'''
Exceptions, Errors, and Warnings for Relational Objects
=========================================================
'''
from exa.errors import ExaException


class PrimaryKeyError(ExaException):
    '''
    '''
    _msg = 'Primary key id (pkid) {0} not found in table {1}!'

    def __init__(self, pkid, table):
        self.msg = self._msg.format(pkid, table)
        super().__init__()


class MultipleObjectsError(ExaException):
    '''
    '''
    _msg = 'Multiple objects found with key {0} in table {1}.'

    def __init__(self, key, table):
        self.msg = self._msg.format(key, table)
        super().__init__()


class NameKeyError(ExaException):
    '''
    '''
    _msg = 'Table {0} does not have the "name" attribute'

    def __init__(self, table):
        self.msg = self._msg.format(table)
        super().__init__()


class FactorNotFound(ExaException):
    '''
    '''
    _msg = 'Conversion factor from {0} to {1} not found: check unit names!'

    def __init__(self, f, t):
        self.msg = self._msg.format(f, t)
        super().__init__()
