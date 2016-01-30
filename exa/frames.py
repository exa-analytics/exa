# -*- coding: utf-8 -*-
'''
Custom DataFrame for exa Analytics
====================================
'''
from traitlets import Unicode, Dict
from exa import _np as np
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
    __traits__ = []
    __groupby__ = None   # Defines the index levels (in some cases the attributes can be used to form a multiindex)

    def _get_column_values(self, *columns, dtype='f8'):
        '''
        '''
        data = np.empty((len(columns), ), dtype='O')
        for i, column in enumerate(columns):
            data[i] = self[column]
        return np.vstack(data).T.astype(dtype)

    def _get_max_values(self, *columns, dtype='f8'):
        '''
        '''
        data = np.empty((len(columns), ), dtype=dtype)
        for i, column in enumerate(columns):
            data[i] = self[column].max()
        return data

    def _get_min_values(self, *columns, dtype='f8'):
        '''
        '''
        data = np.empty((len(columns), ), dtype=dtype)
        for i, column in enumerate(columns):
            data[i] = self[column].min()
        return data

    def _prep_trait_values(self):
        '''
        Placeholder or subclasses to use when logic is required before getting
        traits.
        '''
        pass

    def _post_trait_values(self):
        '''
        '''
        pass

    def get_trait_values(self):
        '''
        Returns:
            traits (dict): Traits to be added to the DOMWidget (:class:`~exa.relational.container.Container`)
        '''
        self._prep_trait_values()
        traits = {}
        groups = None
        if self.__groupby__:
            groups = self.groupby(self.__groupby__)
        for trait in self.__traits__:
            name = '_'.join(('', self.__class__.__name__.lower(), trait))
            if trait in self.columns:
                if self.__groupby__:
                    traits[name] = groups.apply(lambda group: group[trait].values).to_json()
                else:
                    traits[name] = self[trait].to_json(orient='values')
            else:
                traits[name] = ''
        self._post_trait_values()
        return traits

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self) > 0:
            name = self.__class__.__name__
            missing_pk = set(self.__pk__).difference(self.index.names)
            missing_fk = set(self.__fk__).difference(self.columns)
            if missing_pk:                                      # If missing the index name,
                if list(missing_pk) == self.__pk__:             # see if it can be attached,
                    self.index.names = self.__pk__
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
        if len(self) > 0:
            name = self.__class__.__name__
            missing = set(self.__key__).difference(self.index.names)
            if missing:
                raise RequiredIndexError(missing, name)

    def __repr__(self):
        return '{0}'.format(self.__class__.__name__)

    def __str__(self):
        return self.__class__.__name__


class ManyToMany(pd.DataFrame):
    '''
    A DataFrame with only two columns which enumerates the relationship information.
    '''
    __fks__ = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self) > 0:
            if len(self.__fks__) != 2 or  not np.all([col in self.__fks__ for col in self.columns]):
                raise RequiredColumnError(self.__fks__, self.__class__.__name__)
