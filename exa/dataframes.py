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
    column and index requirements and keeps track of relations to other
    DataFrames.
    '''
    __pk__ = []    # Must have these index names
    __fk__ = []    # Must have these column names (which are index names of corresponding DataFrames)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        name = self.__class__.__name__
        missing_pk = set(self.__pk__).difference(self.index.names)
        missing_fk = set(self.__fk__).difference(self.columns)
        if missing_pk:                                      # If missing the index name,
            if list(missing_pk) == [None]:                  # see if it can be attached,
                self.index.names = [self.__class__.__name__.lower()]
            else:                                           # otherwise throw error.
                raise RequiredIndexError(missing_pk, name)
        if missing_fk:
            raise RequiredColumnError(missing_fk, name)

    def __repr__(self):
        return '{0}'.format(self.__class__.__name__)

    def __str__(self):                   # Prevents the awkard string print
        return self.__class__.__name__   # of the dataframe html.


class Updater(pd.SparseDataFrame):
    '''
    Sparse dataframe used to update a full :class:`~exa.dataframes.DataFrame`.
    '''
    __key__ = []   # This is both the index and the foreign DataFrame designation.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        name = self.__class__.__name__
        missing = set(self.__key__).difference(self.index.names)
        if missing:
            if list(missing) == [None]:
                self.index.names = [self.__class__.__name__.lower()]
            else:
                raise RequiredIndexError(missing_pk, name)

    def __repr__(self):
        return '{0}'.format(self.__class__.__name__)

    def __str__(self):
        return self.__class__.__name__


class ManyToManyRelation(DataFrame):
    '''
    A full DataFrame, but with only two columns which provide the many-to-many
    relationship information.
    '''
    __items__ = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.__items__) != 2 or self.columns != self.__items__:
            raise RequiredColumnError(self.__items__, self.__class__.__name__)
