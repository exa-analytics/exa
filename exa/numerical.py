# -*- coding: utf-8 -*-
'''
Trait Supporting Data Objects
###################################
The :class:`~exa.numerical.DataFrame` is an extension of the
:class:`~pandas.DataFrame` object. It provides additional methods for creating
traits.

Note:
    For further information on traits, see :mod:`~exa.widget`.

Additionally, :class:`~exa.numerical.DataFrame` and related objects (e.g
:class:`~exa.numerical.Field`) provide attributes for defining their index and
column names. This has the effect of creating relationships between different
dataframes. They can be grouped into three types:

1. index name (df1) matches index name (df2)
2. index name (df1) matches column name (df2)
3. column name (df1) matches column name (df2)

Note:
    These types correspond to one to one, one to many, and many to many relational
    types, respectively.

Finally, the objects contained in this module provide convenience methods for
handling `categorical data`_.

See Also:
    :mod:`~exa.container`, :mod:`~exa.widget`

.. _categorical data: http://pandas-docs.github.io/pandas-docs-travis/categorical.html
'''
import numpy as np
import pandas as pd
from numbers import Integral, Real
from traitlets import Unicode, Integer, Float
from exa.error import RequiredIndexError, RequiredColumnError


class Numerical:
    '''
    Base class for :class:`~exa.numerical.Series`, :class:`~exa.numerical.DataFrame`,
    and :class:`~exa.numerical.Field` objects, providing default trait
    functionality, shortened string representation, and in memory copying support.
    '''
    def copy(self, *args, **kwargs):
        '''
        Create a copy without mangling the (class) type.
        '''
        return self.__class__(self._copy(*args, **kwargs))

    def _update_custom_traits(self):
        return {}    # Placeholder for custom traits: by default return empty dict

    def _update_traits(self):
        traits = self._update_custom_traits()    # See comment above
        return traits

    def __repr__(self):
        name = self.__class__.__name__
        return '{0}{1}'.format(name, self.shape)

    def __str__(self):
        return self.__repr__()


class Series(Numerical, pd.Series):
    '''
    Trait supporting analogue of :class:`~pandas.Series`.
    '''
    _copy = pd.Series.copy


class DataFrame(Numerical, pd.DataFrame):
    '''
    Trait supporting analogue of :class:`~pandas.DataFrame`.

    Note:
        Columns, indices, etc. are only enforced if the dataframe has non-zero
        length.
    '''
    _copy = pd.DataFrame.copy
    _groupbys = []      # Column names by which to group the data
    _indices = []       # Required index names (typically single valued list)
    _columns = []       # Required column entries
    _traits = []        # Traits present as dataframe columns (or series values)
    _categories = {}    # Column name, original type pairs ('label', int) that can be compressed to a category
    _precision = {}     # Traits precision for JSON

    def _revert_categories(self):
        '''
        Change all columns of type category to their native type.
        '''
        for column, dtype in self._categories.items():
            if column in self.columns:
                self[column] = self[column].astype(dtype)

    def _set_categories(self):
        '''
        Change all category like columns from their native type to category type.
        '''
        for column, dtype in self._categories.items():
            if column in self.columns:
                self[column] = self[column].astype('category')

    def _update_traits(self):
        '''
        Generate trait objects from column data.

        This function will group columns (if applicable) and form JSON object strings
        from columns which have been declared as traits (using the _traits attribute).

        Note:
            This function decides what `trait type`_ to use. This will almost always
            be a JSON (unicode) string formatted to be parsed into an array like
            structure in Javascript.

        .. _trait type: http://traitlets.readthedocs.org/en/stable/trait_types.html
        '''
        traits = self._update_custom_traits()
        groups = None
        prefix = self.__class__.__name__.lower()
        self._revert_categories()
        self._fi = self.index[0]
        if self._groupbys:
            groups = self.groupby(self._groupbys)
        for name in self._traits:
            trait_name = '_'.join((prefix, str(name)))    # Name mangle to ensure uniqueness
            if name in self.columns:
                if np.all(np.isclose(self[name], self.ix[self._fi, name])):    # Don't bother sending all elements if same
                    value = self.ix[self._fi, name]
                    if isinstance(value, Integral):
                        trait = Integer(int(value))
                    elif isinstance(value, Real):
                        trait = Float(float(value))
                    else:
                        raise TypeError('Unknown type for {0} with type {1}'.format(name, dtype))
                elif groups:                              # Else send grouped traits
                    trait = Unicode(groups.apply(lambda g: g[name].values).to_json(orient='values', double_precision=self._precision))
                else:                                     # Else send flat values
                    trait = self[name].to_json(orient='values', double_precision=self._precision)
                traits[trait_name] = trait.tag(sync=True)
            elif name == self.index.names[0]:             # Otherwise, if index, send flat values
                trait_name = '_'.join((prefix, str(name)))
                traits[trait_name] = Unicode(pd.Series(self.index).to_json(orient='values', double_precision=self._precision)).tag(sync=True)
        self._set_categories()
        return traits

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
                if missing and len(self.index.names) != len(self._indices):
                    raise RequiredIndexError(missing, name)
                else:
                    self.index.names = self._indices


class Field(DataFrame):
    '''
    Fields are a special dataframe that always have a **field_values**
    attribute which is a list container series/dataframe objects that contain
    the discrete field values - the :class:`~exa.numerical.Field` dataframe
    itself contains the description of the field (e.g. number of grid points,
    size).
    '''
    _precision = 4
    _indices = ['field']
    _memory_usage = DataFrame.memory_usage

    def copy(self, *args, **kwargs):
        '''
        Copy the field dataframe, including the field values
        '''
        df = self._copy(*args, **kwargs)
        field_values = [field.copy() for field in self.field_values]
        return self.__class__(field_values, df)

    def _update_custom_traits(self):
        '''
        Obtain field values using the custom trait getter (called automatically
        by :func:`~exa.numerical.Numerical._update_traits`).
        '''
        traits = {}
        if self._groupbys:
            grps = self.groupby(self._groupbys)
            string = str(list(grps.groups.values())).replace(' ', '')
            traits['field_indices'] = Unicode(string).tag(sync=True)
        else:
            string = pd.Series(self.index.values).to_json(orient='values')
            traits['field_indices'] = Unicode(string).tag(sync=True)
        s = pd.Series({i: field.values for i, field in enumerate(self.field_values)})
        json_string = s.to_json(orient='values', double_precision=self._precision)
        traits['field_values'] = Unicode(json_string).tag(sync=True)
        return traits

    def memory_usage(self):
        '''
        Get the combined memory usage of the field data and field values.
        '''
        data = self._memory_usage()
        values = 0
        for value in self.field_values:
            values += value.memory_usage()
        data['field_values'] = values
        return data

    def __init__(self, *args, field_values=None, **kwargs):
        if isinstance(args[0], pd.Series):
            args = (args[0].to_frame().T, )
        super().__init__(*args, **kwargs)
        if isinstance(field_values, pd.Series) and len(self) == 1:
            self.field_values
        if isinstance(field_values, list):
            self.field_values = [Series(v) for v in field_values]
        else:
            self.field_values = [Series(v) for v in field_values]
        for i in range(len(field_values)):
            self.field_values[i].name = i


class Field3D(Field):
    '''
    Dataframe for storing dimensions of a scalar or vector field of 3D space.

    +-------------------+----------+-------------------------------------------+
    | Column            | Type     | Description                               |
    +===================+==========+===========================================+
    | nx                | int      | number of grid points in x                |
    +-------------------+----------+-------------------------------------------+
    | ny                | int      | number of grid points in y                |
    +-------------------+----------+-------------------------------------------+
    | nz                | int      | number of grid points in z                |
    +-------------------+----------+-------------------------------------------+
    | ox                | float    | field origin point in x                   |
    +-------------------+----------+-------------------------------------------+
    | oy                | float    | field origin point in y                   |
    +-------------------+----------+-------------------------------------------+
    | oz                | float    | field origin point in z                   |
    +-------------------+----------+-------------------------------------------+
    | xi                | float    | First component in x                      |
    +-------------------+----------+-------------------------------------------+
    | xj                | float    | Second component in x                     |
    +-------------------+----------+-------------------------------------------+
    | xk                | float    | Third component in x                      |
    +-------------------+----------+-------------------------------------------+
    | yi                | float    | First component in y                      |
    +-------------------+----------+-------------------------------------------+
    | yj                | float    | Second component in y                     |
    +-------------------+----------+-------------------------------------------+
    | yk                | float    | Third component in y                      |
    +-------------------+----------+-------------------------------------------+
    | zi                | float    | First component in z                      |
    +-------------------+----------+-------------------------------------------+
    | zj                | float    | Second component in z                     |
    +-------------------+----------+-------------------------------------------+
    | zk                | float    | Third component in z                      |
    +-------------------+----------+-------------------------------------------+

    Note:
        Each field should be flattened into an N x 1 (scalar) or N x 3 (vector)
        series or dataframe respectively. The orientation of the flattening
        should have x as the outer loop and z values as the inner loop (for both
        cases). This is sometimes called C-major order, C-style order, and has
        the last index changing the fastest and the first index changing the
        slowest.

    See Also:
        :class:`~exa.numerical.Field`
    '''
    _columns = ['nx', 'ny', 'nz', 'ox', 'oy', 'oz', 'xi', 'xj', 'xk',
                'yi', 'yj', 'yk', 'zi', 'zj', 'zk']
    _traits = ['nx', 'ny', 'nz', 'ox', 'oy', 'oz', 'xi', 'xj', 'xk',
               'yi', 'yj', 'yk', 'zi', 'zj', 'zk']


class SparseSeries(Numerical, pd.SparseSeries):
    '''
    Trait supporting sparse series.
    '''
    _copy = pd.SparseSeries.copy


class SparseDataFrame(Numerical, pd.SparseDataFrame):
    '''
    Trait supporting sparse dataframe.
    '''
    _copy = pd.SparseDataFrame.copy

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
                if missing and len(self.index.names) != len(self._indices):
                    raise RequiredIndexError(missing, name)
                else:
                    self.index.names = self._indices
