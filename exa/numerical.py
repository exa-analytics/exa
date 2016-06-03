# -*- coding: utf-8 -*-
'''
Trait Support for Data Structures
###################################
The :class:`~exa.numerical.DataFrame` inherits :class:`~pandas.DataFrame` and
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

Enumerated are some conventions used by trait supporting data objects:
- use **_precision** to specify precision of floats sent to JS
- use **_traits** to specify (possible) column names that are sent to JS
- use **_columns** to specify required columns
- use **_groupbys** to specify columns on which to group (typically these columns are foreign keys to another frame with an index of the same name as the column name)
- use **_categories** to specify (possible) column names that are category dtype ({name: normal_type})
- an index of -1 means not applicable (or not possible to compute)

See Also:
    Modules :mod:`~exa.container` and :mod:`~exa.widget` may provide context
    and usage examples for these classes.

.. _categories: http://pandas-docs.github.io/pandas-docs-travis/categorical.html
'''
import numpy as np
import pandas as pd
from numbers import Integral, Real
from traitlets import Unicode, Integer, Float
from exa.error import RequiredIndexError, RequiredColumnError


class NDBase:
    '''
    Base class for trait supporting dataframe/series objects.
    '''
    _precision = 3      # Default number of decimal places passed by traits

    def copy(self, *args, **kwargs):
        '''
        Custom copy function returns same type
        '''
        return self.__class__(self._copy(*args, **kwargs))

    def _update_custom_traits(self):
        '''
        Placeholder for custom trait creation (e.g. when multiple columns form a single trait).
        '''
        return {}

    def _update_traits(self):
        '''
        Empty default traits.
        '''
        traits = self._update_custom_traits()
        return traits

    def __repr__(self):
        name = self.__class__.__name__
        return '{0}{1}'.format(name, self.shape)

    def __str__(self):
        return self.__repr__()


class Series(NDBase, pd.Series):
    '''
    Trait supporting analogue of :class:`~pandas.Series`.
    '''
    _copy = pd.Series.copy


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
    _traits = []        # Traits present as dataframe columns (or series values)

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
        if self._groupbys:
            groups = self.groupby(self._groupbys)
        for name in self._traits:
            if name in self.columns:
                trait_name = '_'.join((prefix, str(name)))    # Name mangle to ensure uniqueness
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
                traits[trait_name] = trait
            elif name == self.index.names[0]:             # Otherwise, if index, send flat values
                trait_name = '_'.join((prefix, str(name)))
                traits[trait_name] = Unicode(pd.Series(self.index).to_json(orient='values', double_precision=self._precision))
            traits[trait_name].tag(sync=True)
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
        by :func:`~exa.numerical.NDBase._update_traits`).
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


class SparseSeries(NDBase, pd.SparseSeries):
    '''
    Trait supporting sparse series.
    '''
    _copy = pd.SparseSeries.copy


class SparseDataFrame(NDBase, pd.SparseDataFrame):
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
