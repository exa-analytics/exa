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

Another feature of these dataframes is that the _groupbys parameter provides a
convenient algorithm for container slicing and concatenation/joining/merging.
These types of operations are non-trivial when dealing with dataframes whose
contents may be related (i.e. relational dataframes) so care must be taken to
ensure no mangling of indices is performed. See the container module for more
info.

See Also:
    Modules :mod:`~exa.container` and :mod:`~exa.widget` may provide context
    and usage examples for these classes.

.. _categories: http://pandas-docs.github.io/pandas-docs-travis/categorical.html
'''
import numpy as np
import pandas as pd
from traitlets import Unicode, Integer, Float
from exa.error import RequiredIndexError, RequiredColumnError


class NDBase:
    '''
    Base class for custom dataframe and series objects that have traits.
    '''
    _precision = 3      # Default number of decimal places passed by traits
    _traits = []        # Traits present as dataframe columns (or series values)

    def _get_traits(self):
        return {}

    def __repr__(self):
        name = self.__class__.__name__
        n = len(self)
        return '{0}(len: {1})'.format(name, n)

    def __str__(self):
        return self.__repr__()


class Series(NDBase, pd.Series):
    '''
    Trait supporting analogue of :class:`~pandas.Series`.
    '''
    _copy = pd.Series.copy

    def copy(self, *args, **kwargs):
        '''
        Custom copy function returns same type
        '''
        return self.__class__(self._copy(*args, **kwargs))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DataFrame(NDBase, pd.DataFrame):
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
    _categories = {}    # Column name, original type pairs ('label', int) that can be compressed to a category

    @property
    def _fi(self):
        return self.index[0]

    @property
    def _li(self):
        return self.index[-1]

    def copy(self, *args, **kwargs):
        '''
        Custom copy function returns same type
        '''
        return self.__class__(self._copy(*args, **kwargs))

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

    def _get_custom_traits(self):
        '''
        Placeholder function to be overwritten when custom trait creation is
        required
        Returns:
            traits (dict): Dictionary of traits to be added
        '''
        return {}

    def _get_traits(self):
        '''
        Generate trait objects from column data.

        This function will group columns by the :class:`~exa.numerical.DataFrame`'s
        **_groupbys** attribute, select the column (or columns) that specify a
        single trait, and package that up as a trait to be used by the frontend.

        Note:
            This function decides what `trait type`_ to use. Typically, a
            column (or columns) containing unique data is sent as a (grouped)
            json string. If the column contains non-unique data, this function
            will send a single value of the appropriate type (e.g. `Float`_) so
            as to duplicate the least amount of data possible (and have the least
            communication overhead possible).

        See Also:
            The collecting function of the JavaScript side of things is the
            **get_trait** method in **container.js**.

        Tip:
            The algorithm's performance could be improved: in the case where
            each group has *N* values that are the same to each other but
            unique with respect to other groups' values all values are sent to
            the frontend!

        .. _trait type: http://traitlets.readthedocs.org/en/stable/trait_types.html
        .. _Float: http://traitlets.readthedocs.org/en/stable/trait_types.html#traitlets.Float
        '''
        traits = self._get_custom_traits()
        groups = None
        prefix = self.__class__.__name__.lower()
        self._revert_categories()
        if self._groupbys:
            groups = self.groupby(self._groupbys)
        for name in self._traits:
            if name in self.columns:
                trait_name = '_'.join((prefix, name))    # Name mangle to ensure uniqueness
                if np.all(np.isclose(self[name], self.ix[self._fi, name])):
                    value = self.ix[self._fi, name]
                    dtype = type(value)
                    if dtype is np.int64 or dtype is np.int32 or dtype is int:
                        trait = Integer(int(value))
                    elif dtype is np.float64 or dtype is np.float32 or dtype is float:
                        trait = Float(float(value))
                    else:
                        raise TypeError('Unknown type for {0} with type {1}'.format(name, dtype))
                elif groups:                              # Else send grouped traits
                    trait = Unicode(groups.apply(lambda g: g[name].values).to_json(orient='values', double_precision=self._precision))
                else:                                     # Else send flat values
                    trait = self[name].to_json(orient='values', double_precision=self._precision)
                traits[trait_name] = trait.tag(sync=True)
            elif name == self.index.names[0]:             # Otherwise, if index, send flat values
                trait_name = '_'.join((prefix, name))
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
    A discrete field is described by its spatial discritization (field data)
    where each discrete point has any number of attributes (field values). This
    is a special type of dataframe because the dimensionality of the field
    values may be different for different fields. This class, therefore, stores
    the field dimensionality in one dataframe and field values in other data
    frames.
    '''
    _precision = 4
    _indices = ['field']
    _df_get_traits = DataFrame._get_traits

    def copy(self, *args, **kwargs):
        '''
        Copy the field dataframe, including the field values
        '''
        df = self._copy(*args, **kwargs)
        field_values = [field.copy() for field in self.field_values]
        return self.__class__(field_values, df)

    def _get_traits(self):
        '''
        Because the :class:`~exa.numerical.Field` object has attached vector
        and scalar field values, trait creation is handled slightly differently.
        '''
        traits = self._df_get_traits()
        self._revert_categories()
        if self._groupbys:
            grps = self.groupby(self._groupbys)
            string = grps.apply(lambda g: g.index).to_json(orient='values')
            traits['field_indices'] = Unicode(string).tag(sync=True)
            #string = grps.apply(lambda g: g['label'].values).to_json(orient='values')
            #traits['field_labels'] = Unicode(string).tag(sync=True)
            #string = grps.apply(lambda g: g['field_type'].values).to_json(orient='values')
            #traits['field_types'] = Unicode(string).tag(sync=True)
        else:
            string = Series(self.index).to_json(orient='values')
            traits['field_indices'] = Unicode(string).tag(sync=True)
            #string = self['label'].to_json(orient='values')
            #traits['field_labels'] = Unicode(string).tag(sync=True)
            #string = self['field_types'].to_json(orient='values')
            #traits['field_types'] = Unicode(strign).tag(sync=True)
        s = pd.Series({i: field.values for i, field in enumerate(self.field_values)})
        traits['field_values'] = Unicode(s.to_json(orient='values', double_precision=self._precision)).tag(sync=True)
        self._set_categories()
        return traits

    def __init__(self, field_values, *args, **kwargs):
        '''
        Args:
            field_values (list): List of Series or DataFrame objects containing field values with indices corresponding to field data index
        '''
        super().__init__(*args, **kwargs)
        self.field_values = field_values


class Field3D(Field):
    '''
    Dataframe for storing dimensions of a scalar or vector field of 3D space.
    The row index present in this dataframe should correspond to a
    A dataframe for storing field (meta)data along with the actual field values.
    The storage of field values may be in the form of a scalar field (via
    :class:`~exa.numerical.Series`) or vector field (via
    :class:`~exa.numerical.DataFrame`). The field index (of this dataframe)
    corresponds to the index in the list of field value data.

    +-------------------+----------+-------------------------------------------+
    | Column            | Type     | Description                               |
    +===================+==========+===========================================+
    | nx                | int      | number of dimensionsin x                  |
    +-------------------+----------+-------------------------------------------+
    | ny                | int      | number of dimensionsin y                  |
    +-------------------+----------+-------------------------------------------+
    | nz                | int      | number of dimensionsin z                  |
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
    '''
    _columns = ['nx', 'ny', 'nz', 'ox', 'oy', 'oz', 'xi', 'xj', 'xk',
                'yi', 'yj', 'yk', 'zi', 'zj', 'zk']
    _traits = ['nx', 'ny', 'nz', 'ox', 'oy', 'oz', 'xi', 'xj', 'xk',
               'yi', 'yj', 'yk', 'zi', 'zj', 'zk']


class SparseDataFrame(NDBase, pd.SparseDataFrame):
    '''
    Trait supporting sparse dataframe, typically used to update values in a
    related dataframe.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self) > 0:
            name = self.__class__.__name__
            if self._indices:
                missing = set(self._indices).difference(self.index.names)
                if missing and len(self.index.names) != len(self._indices):
                    raise RequiredIndexError(missing, name)
                else:
                    self.index.names = self._indices
