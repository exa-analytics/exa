# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Exceptions
#################################
All base level exceptions are defined here.
'''
import re


class ExaException(Exception):
    '''
    Exception with support for logging.
    '''
    def __init__(self, msg):
        spacer = '\n' + ' ' * len(self.__class__.__name__) + '  '    # Align the message
        msg = re.sub(r'\s*\n\s*', spacer, msg)
        super().__init__(msg)


class RequiredIndexError(ExaException):
    '''
    :class:`~exa.dataframe.DataFrame` index name error.
    '''
    _msg = 'Missing required index(ices), {0}, for creation of class {1} object.'

    def __init__(self, missing, clsname):
        msg = self._msg.format(missing, clsname)
        super().__init__(msg)


class RequiredColumnError(ExaException):
    '''
    :class:`~exa.dataframe.DataFrame` column error.
    '''
    _msg = 'Missing required column(s), {0}, for creation of class {1} object.'

    def __init__(self, missing, clsname):
        msg = self._msg.format(missing, clsname)
        super().__init__(msg)
