# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
DataFrame
########################
`Dataframes`_ are tabular data structures with columns and indices capable of
representing multi-dimensional, multi-featured data. The
:class:`~exa.core.dataframe.DataFrame` behaves identically to Pandas
`Dataframes`_ but provides support for required columns and column dtype
enforcement. Subclassing, therefore, allows for the creation of convenience
methods based on standardized column names (and types). Additionally,
creation of data processing and visualization systems is easier when data has
(at least a minimal) structure and type(s).

See Also:
    :class:`~exa.core.container.Container`

.. _DataFrames: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
"""
import six
import pandas as pd
from .base import Base
from exa.functions import LazyFunction
from exa.typed import TypedMeta, TypedProperty


class Feature(LazyFunction):
    """
    A description of a column in a :class:`~exa.core.dataframe.DataFrame`.
    """
    def to_dict(self, *args, **kwargs):
        """Returns a dictionary of kwargs."""
        return self.kwargs

    def __init__(self, dtypes, required=False, findex=None):
        """
        Args:
            dtypes (iterable, type): Dtype or iterable of dtypes of the feature (column)
            required (bool): Required column for dataframe creation
            findex (iterable): Foreign index names (on which groupby occurs)
            func (function):
        """
        if not isinstance(dtypes, (list, tuple)):
            dtypes = (dtypes, )
        super(Feature, self).__init__(fn=self.to_dict, required=required,
                                      findex=findex, dtypes=dtypes)


class BaseMeta(TypedMeta):
    """A typed metaclass for dataframes."""
    def __new__(mcs, name, bases, namespace):
        reqcols = []
        coltypes = {}
        # Make a copy of the namespace and modify the original
        for attr_name, attr in dict(namespace).items():
            if isinstance(attr, Feature):
                # Remove the attr from the name space
                kwargs = attr()
                coltypes[attr_name] = kwargs['dtypes']
                if kwargs['required']:
                    reqcols.append(attr_name)
        namespace['reqcols'] = reqcols
        namespace['coltypes'] = coltypes
        return super(BaseMeta, mcs).__new__(mcs, name, bases, namespace)


class DataFrame(six.with_metaclass(BaseMeta, pd.DataFrame, Base)):
    """
    A `pandas`_ like `dataframe`_ with support for required columns, required
    column dtypes, and convenience method creation.

    A special syntax is used to create required columns or statically (d)typed
    columns. An illustration follows with descriptions in the comments.

    .. code-block:: python

        class MyDataFrame(DataFrame):
            col0 = float        # Opt. col; enforced dtype float
            col1 = (int, True)  # Req. col; enforced dtype int
            col2 = (None, True) # Req. col; any dtype allowed
            col3 = (int, float) # Opt. col; enforced int, then float
            col4 = ((int, float), True)  # Req., multiple types

    In the last example ``col3`` (an optional column) is preferred to be of dtype
    ``int`` with a fallback to ``float``; the column must be coerced to one of
    these types otherwise a TypeError is raised.

    .. _pandas: http://pandas.pydata.org/
    .. _dataframe: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
    """
    # Note that the ``Base`` class, which requires the creation of an ``info``
    # method is satisfied by the pandas DataFrame which provides that method.
    _metadata = ["reqcols", "coltypes", "meta"]
    reqcols = TypedProperty(list, "Required columns")
    coltypes = TypedProperty(dict, "Column types")
    aliases = TypedProperty(dict, docs="Column name aliases for automatic renaming")

    def info(self, verbose=True, *args, **kwargs):
        """Call the pandas DataFrame info method."""
        kwargs['verbose'] = verbose
        return super(DataFrame, self).info(*args, **kwargs)

    @property
    def _constructor(self):
        return DataFrame

    def _enforce_aliases(self):
        """Automatic column naming using aliases."""
        if isinstance(self.aliases, dict):
            self.rename(columns=self.aliases, inplace=True)

    def _enforce_columns(self):
        """
        Enforce required columns and dtypes using the ``coltypes`` and ``reqcols`` class
        attribute (i.e. shared between all instances of this class); updated when
        ``DataFrame.__new__`` is called.
        """
        # First check required columns.
        if self.reqcols is not None:
            missing = set(self.reqcols).difference(self.columns)
            if len(missing) > 0:
                raise NameError("Missing column(s) {}".format(missing))
            # Second convert types.
            dtypes = self.dtypes
            for name, types in self.coltypes.items():
                if name in dtypes and types is not None and types[0] != dtypes[name]:
                    for typ in types:
                        try:
                            super(DataFrame, self).__setitem__(name, self[name].astype(typ))
                            break    # Stop on successful convert
                        except TypeError:
                            pass
                    else:
                        raise TypeError("Unable to enforce column types for {} as types {}".format(name, types))

    def _enforce_index(self):
        """
        Ensure that we have a unique index to use with the same name as the
        class name (lowercase).
        """
        if isinstance(self.index, pd.MultiIndex):
            self.reset_index(inplace=True)
        self.index.name = self.__class__.__name__.lower()

    def _enforce(self):
        """Enforce format of columns and indices."""
        self._enforce_aliases()
        self._enforce_index()
        self._enforce_columns()

    def __setitem__(self, *args, **kwargs):
        """Setitem is called on column manipulations so we recheck columns."""
        super(DataFrame, self).__setitem__(*args, **kwargs)
        self._enforce()

    def __init__(self, *args, **kwargs):
        meta = kwargs.pop("meta", None)
        super(DataFrame, self).__init__(*args, **kwargs)
        self._enforce()
        self.meta = meta


class SectionDataFrame(DataFrame):
    """
    A dataframe that describes :class:`~exa.core.parser.Sections` object sections.

    Instances of this dataframe describe the starting and ending points of
    regions of a text file to be parsed. Upon creation of instances of this
    object, the 'attribute' column is added which suggests the name of the
    attribute (on the instance of :class:`~exa.core.parser.Sections`) to which
    a given text region belongs.
    """
    _section_name_prefix = "section"
    parser = Feature(object, True)
    start = Feature(int, True)
    end = Feature(int, True)

    def __init__(self, *args, **kwargs):
        super(SectionDataFrame, self).__init__(*args, **kwargs)
        self['attribute'] = [self._section_name_prefix+str(i).zfill(len(str(len(self)))) for i in self.index]


class Composition(DataFrame):
    """
    A dataframe that describes the structure of :class:`~exa.core.composer.Composer`.

    Instances of this dataframe contain information used to dynamically
    construct a compsed editor using data stored in Python objects and a string
    template.
    """
    length = Feature(None, True)
    joiner = Feature(str, True)
    name = Feature(str, True)
