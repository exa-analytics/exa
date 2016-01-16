# -*- coding: utf-8 -*-
'''
Custom DataFrame for exa Analytics
====================================
'''
from exa import _pd as pd
from exa.errors import RequiredIndexError, RequiredColumnError


class DataFrame(pd.DataFrame):
    '''
    Behaves just like a :py:class:`~pandas.DataFrame`, but enforces minimum
    column and index requirements.

    '''
    __indices__ = []
    __columns__ = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self) > 0:
            name = self.__class__.__name__
            missing_req_indices = set(self.__indices__).difference(self.index.names)
            missing_req_columns = set(self.__columns__).difference(self.columns)
            if missing_req_indices:
                raise RequiredIndexError(missing_req_indices, name)
            if missing_req_columns:
                raise RequiredColumnError(missing_req_columns, name)

    def __repr__(self):
        return '{0}'.format(self.__class__.__name__)

    def __str__(self):
        return self.__class__.__name__
