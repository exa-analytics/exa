# -*- coding: utf-8 -*-
'''
Custom DataFrame (and Related) Classes
=========================================
The :class:`~exa.dataframe.DataFrame` inherits :class:`~pandas.DataFrame` and
behaves just like it, but it provides special methods for extracting trait
data from the frame. The trait data is used by :class:`~exa.widget.ContainerWidget`
(and its subclasses) and the web gui to generate interactive data visualizations.
Because these dataframes have context about their data, they also provide
convience methods for in memory data compression (using `categories`_).

See Also:
    Modules :mod:`~exa.container` and :mod:`~exa.widget` may provide context.

.. _categories: http://pandas-docs.github.io/pandas-docs-travis/categorical.html
'''
import numpy as np
import pandas as pd
from traitlets import Unicode, Dict
from exa.error import RequiredIndexError, RequiredColumnError


class _TraitsDF:
    '''
    Base dataframe class providing trait support for :class:`~pandas.DataFrame`
    like objects.
    '''
    _precision = 4      # Default number of decimal places passed by traits
    _indices = []       # Required index names (typically single valued list)
    _columns = []       # Required column entries
    _traits = []        # Columns that are usable traits
    _groupbys = []      # Column names by which to group the data
    _categories = {}    # Column name, original type pairs ('label', int) that can be compressed to a category

    def _revert_categories(self):
        '''
        Change all columns of type category to their native type.
        '''
        for column, dtype in self._categories.items():
            self[column] = self[column].astype(dtype)

    def _set_categories(self):
        '''
        Change all category like columns from their native type to category type.
        '''
        for column, dtype in self._categories.items():
            self[column] = self[column].astype('category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self) > 0:
            name = self.__class__.__name__
            if self._columns:
                missing = set(self._columns).difference(self.columns)
                if missing:
                    raise RequiredColumnError(missing, name)
            if self._indices:
                missing = set(self._indices).difference(self.index.names)
                if missing:
                    raise RequiredIndexError(missing, name)

    def __repr__(self):
        name = self.__class__.__name__
        n = len(self)
        m = len(self.columns)
        return '{0}(rows: {1} columns: {2})'.format(name, n, m)

    def __str__(self):
        return self.__repr__()

class DataFrame(_TraitsDF, pd.DataFrame):
    '''
    Trait supporting analogue of :class:`~pandas.DataFrame`.

    Note:
        Columns, indices, etc. are only enforced if the dataframe has non-zero
        length.
    '''
    pass


class SparseFrame(_TraitsDF, pd.SparseDataFrame):
    '''
    A sparse dataframe used to update it's corresponding
    :class:`~exa.ndframe.DataFrame` or a truly sparse data store.
    '''
    pass


#    _key = []   # This is both the index and the foreign DataFrame designation.
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        if len(self) > 0:
#            name = self.__class__.__name__
#            missing = set(self._key).difference(self.index.names)
#            if missing:
#                raise RequiredIndexError(missing, name)
#
#    def __repr__(self):
#        return '{0}'.format(self.__class__.__name__)
#
#    def __str__(self):
#        return self.__class__.__name__



#    def _as_raw(self, which=[]):
#        '''
#        Internal conversion from categories to raw types.
#
#        If no argument is provided, will convert all categories.
#
#        Args:
#            which: String or list of strings of column names to convert
#        '''
#        for name, dtype in self.__categories:
#            if which == [] or name in which or name == which:
#                self[col] = self[col].astype(dtype)
#
#    def _as_cat(self, which=[]):
#        '''
#        Internal conversion to categories from raw types.
#
#        If no argument is provided, will convert all categories.
#
#        Args:
#            which: String or list of strings of column names to convert
#        '''
#        for name, dtype in self._categories:
#            if which == [] or name in which or name == which:
#                self[col] = self[col].astype('category')
#
#    def get_trait_values(self):
#        '''
#        Returns:
#            traits (dict): Traits to be added to the DOMWidget (:class:`~exa.relational.container.Container`)
#        '''
#        traits = {}
#        if len(self) > 0:
#            self._prep_trait_values()
#            groups = None
#            if self._groupbys:
#                groups = self.groupby(self._groupbys)
#            for trait in self._traits:
#                name = '_'.join(('', self.__class__.__name__.lower(), trait))
#                if trait in self.columns:
#                    if self._groupbys:
#                        traits[name] = groups.apply(lambda group: group[trait].astype('O').values).to_json()
#                    else:
#                        traits[name] = self[trait].to_json(orient='values')
#                else:
#                    traits[name] = ''
#            self._post_trait_values()
#        return traits
#
#    def _get_column_values(self, *columns, dtype='f8'):
#        '''
#        '''
#        data = np.empty((len(columns), ), dtype='O')
#        for i, column in enumerate(columns):
#            data[i] = self[column]
#        return np.vstack(data).T.astype(dtype)
#
#    def _get_max_values(self, *columns, dtype='f8'):
#        '''
#        '''
#        data = np.empty((len(columns), ), dtype=dtype)
#        for i, column in enumerate(columns):
#            data[i] = self[column].max()
#        return data
#
#    def _get_min_values(self, *columns, dtype='f8'):
#        '''
#        '''
#        data = np.empty((len(columns), ), dtype=dtype)
#        for i, column in enumerate(columns):
#            data[i] = self[column].min()
#        return data
#
#    def _prep_trait_values(self):
#        '''
#        '''
#        pass
#
#    def _post_trait_values(self):
#        '''
#        '''
#        pass
#
#    def _get_by_index(self, index):
#        '''
#        '''
#        if len(self) > 0:
#            cls = self.__class__
#            if self._groupbys:
#                getter = self[self._groupbys].unique()[index]
#                return cls(self.groupby(self._groupbys).get_group(getter))
#            else:
#                return cls(self.ix[index:index, :])
#        else:
#            return self
#
#    def _get_by_indices(self, indices):
#        '''
#        '''
#        if len(self) > 0:
#            cls = self.__class__
#            if self._groupbys:
#                getters = self[self._groupbys].unique()[indices]
#                return cls(self[self[self._groupbys].isin(getters)])
#            else:
#                return cls(self.ix[indices, :])
#        else:
#            return self
#
#    def _get_by_slice(self, s):
#        '''
#        '''
#        if len(self) > 0:
#            cls = self.__class__
#            indices = self.index
#            if self._groupbys:
#                indices = self[self._groupbys].unique()
#            start = indices[0] if s.start is None else indices[s.start]
#            stop = indices[-1] if s.stop is None else indices[s.stop]
#            step = s.step
#            indices = indices[start:stop:step]
#            if self._groupbys:
#                return cls(self.ix[self[self._groupbys].isin(indices)])
#            return cls(self.ix[indices, :])
#        else:
#            return self
#
#class Updater(pd.SparseDataFrame):
#    '''
#    Sparse dataframe used to update a full :class:`~exa.dataframes.DataFrame`.
#    '''
#    _key = []   # This is both the index and the foreign DataFrame designation.
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        if len(self) > 0:
#            name = self.__class__.__name__
#            missing = set(self._key).difference(self.index.names)
#            if missing:
#                raise RequiredIndexError(missing, name)
#
#    def __repr__(self):
#        return '{0}'.format(self.__class__.__name__)
#
#    def __str__(self):
#        return self.__class__.__name__
#
#
#class ManyToMany(pd.DataFrame):
#    '''
#    A DataFrame with only two columns which enumerates the relationship information.
#    '''
#    _fkeys = []
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        if len(self) > 0:
#            if len(self._fkeys) != 2 or  not np.all([col in self._fkeys for col in self.columns]):
#                raise RequiredColumnError(self._fkeys, self.__class__.__name__)
#
#    def __repr__(self):
#        return '{0}'.format(self.__class__.__name__)
#
#    def __str__(self):
#        return self.__class__.__name__
#
