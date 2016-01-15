# -*- coding: utf-8 -*-
'''
Exceptions, Errors, and Warnings
==================================
All base level exceptions are defined here.
'''
from exa import _re as re
from exa.decorators import logger


@logger
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
            self._logger.error(msg)


class DimensionError(ExaException):
    '''
    :class:`~exa.dataframe.DataFrame` index name error.
    '''
    _extra = 'Extra dimension(s), {0}, supplied in the index of {1}.'
    _missing = 'Missing required dimension(s), {0}, in class {1}.'

    def __init__(self, extra=None, missing=None, name=None):
        if extra is None:
            self.msg = self._missing.format(missing, name)
        else:
            self.msg = self._extra.format(extra, name)
        super().__init__()


class ColumnError(ExaException):
    '''
    :class:`~exa.dataframe.DataFrame` column error.
    '''
    def __init__(self, columns, name):
        self.msg = 'Missing required column(s), {0}, in class {1}.'.format(columns, name)
        super().__init__()
