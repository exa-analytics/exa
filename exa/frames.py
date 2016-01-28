# -*- coding: utf-8 -*-
'''
Custom DataFrame for exa Analytics
====================================
'''
from traitlets import Unicode, Dict
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
        grps = None
        if self.__groupby__:
            grps = self.groupby(self.__groupby__)
        for trait in self.__traits__:
            name = '_'.join(('', self.__class__.__name__.lower(), trait))
            if trait in self.columns:
                if self.__groupby__:
                    traits[name] = groups_to_json(grps, trait)
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


class ManyToMany(DataFrame):
    '''
    A DataFrame with only two columns which enumerates the relationship information.
    '''
    __fks__ = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.__fks__) != 2 or self.columns != self.__fks__:
            raise RequiredColumnError(self.__fks__, self.__class__.__name__)


def groups_to_json(groups, column):
    '''
    Create a json string from a :py:class:`~pandas.core.groupby.DataFrameGroupBy`
    object.
    '''
    json_string = '{'
    for index, group in groups:
        key = '"{0}":'.format(index)
        values = group[column].to_json(orient='values')
        json_string = ''.join((json_string, key, values, ','))
    json_string = ''.join((json_string[:-1], '}'))
    return json_string
