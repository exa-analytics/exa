# -*- coding: utf-8 -*-
'''
Exceptions, Errors, and Warnings
==================================
All base level exceptions are defined here.
'''
import re

class ExaException(Exception):
    '''
    Exception with support for logging.
    '''
    def __init__(self, msg=None, log=True):
        spacer = '\n' + ' ' * len(self.__class__.__name__) + '  '    # Align the message
        if msg is None:
            msg = self.msg
        else:
            msg = re.sub(r'\s*\n\s*', spacer, msg)
        super().__init__(msg)
        if log:
            pass


class RequiredIndexError(ExaException):
    '''
    :class:`~exa.dataframe.DataFrame` index name error.
    '''
    _msg = 'Missing required index(ices), {0}, for creation of class {1} object.'

    def __init__(self, missing, clsname):
        self.msg = self._msg.format(missing, clsname)
        super().__init__()


class RequiredColumnError(ExaException):
    '''
    :class:`~exa.dataframe.DataFrame` column error.
    '''
    _msg = 'Missing required column(s), {0}, for creation of class {1} object.'

    def __init__(self, missing, clsname):
        self.msg = self._msg.format(missing, clsname)
        super().__init__()
