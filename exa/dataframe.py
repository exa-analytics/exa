# -*- coding: utf-8 -*-
'''
Custom DataFrame for exa Analytics
====================================
'''
from exa import _pd as pd
from exa.errors import DimensionError, ColumnError


class DataFrame(pd.DataFrame):
    '''
    Should behave just like a :py:class:`~pandas.DataFrame`.
    '''
    __dimensions__ = []
    __columns__ = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self) > 0:                 # Check index and column requirements
            extra = list(set(self.__dimensions__).difference(self.index.names))
            missing = list(set(self.index.names).difference(self.__dimensions__))
            if extra:
                raise DimensionError(extra=extra)
            if missing:
                raise DimensionError(missing=missing)
            missing_required_columns = list(set(self.__columns__).difference(self.columns))
            if missing_required_columns:
                raise ColumnError(missing_required_columns)
