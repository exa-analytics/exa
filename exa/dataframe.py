# -*- coding: utf-8 -*-
'''
Custom DataFrame for exa Analytics
====================================
'''
from exa import _pd as pd
from exa.errors import DimensionError, ColumnError


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
            extra = set(self.__indices__).difference(self.index.names)
            missing = set(self.index.names).difference(self.__indices__)
            if extra:                      # Check indices
                raise DimensionError(extra=extra, name=name)
            if missing:
                raise DimensionError(missing=missing, name=name)
            missing_required_columns = set(self.__columns__).difference(self.columns)
            if missing_required_columns:   # Check columns
                raise ColumnError(missing_required_columns, name=name)
