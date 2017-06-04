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
"""
import pandas as pd
from .base import Base


class DataFrame(pd.DataFrame, Base):
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
    """
    # Note that the ``Base`` class, which requires the creation of an ``info``
    # method is satisfied by the pandas DataFrame which provides that method.
    _metadata = ["_reqcols", "_coltypes", "meta"]

    def info(self, verbose=True, *args, **kwargs):
        """Call the pandas DataFrame info method."""
        kwargs['verbose'] = verbose
        return super(DataFrame, self).info(*args, **kwargs)

    @property
    def _constructor(self):
        return DataFrame

    def _enforce_columns(self):
        """
        Enforce required columns and dtypes using the ``_coltypes`` and ``_reqcols`` class
        attribute (i.e. shared between all instances of this class); updated when
        ``DataFrame.__new__`` is called.
        """
        # First check required columns.
        missing = set(self._reqcols).difference(self.columns)
        if len(missing) > 0:
            raise NameError("Missing column(s) {}".format(missing))
        # Second convert types.
        dtypes = self.dtypes
        for name, types in self._coltypes.items():
            if name in dtypes and types is not None and types[0] != dtypes[name]:
                for typ in types:
                    try:
                        super(DataFrame, self).__setitem__(name, self[name].astype(typ))
                        break    # Stop on successful convert
                    except TypeError:
                        pass
                else:
                    raise TypeError("Unable to enforce column types for {} as types {}".format(name, types))

    def __setitem__(self, *args, **kwargs):
        """Setitem is called on column manipulations so we recheck columns."""
        super(DataFrame, self).__setitem__(*args, **kwargs)
        self._enforce_columns()

    def __new__(cls, *args, **kwargs):
        """
        Update the required columns on the fly but share the state for all
        dataframes of this type so as not to waste RAM.
        """
        _reqcols = []
        _coltypes = {}
        for name, types in vars(cls).items():
            if isinstance(types, type):
                _coltypes[name] = (types, )
            elif isinstance(types, tuple) and isinstance(types[1], bool):
                _reqcols.append(name)
                _coltypes[name] = types[0] if isinstance(types[0], tuple) else (types[0], )
            elif isinstance(types, tuple) and all(isinstance(typ, type) for typ in types):
                _coltypes[name] = types
        cls._coltypes = _coltypes
        cls._reqcols = _reqcols
        return super(DataFrame, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        meta = kwargs.pop("meta", None)
        super(DataFrame, self).__init__(*args, **kwargs)
        self._enforce_columns()
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
    parser = (object, True)
    start = (int, True)
    end = (int, True)

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
    length = (None, True)
    joiner = (str, True)
    name = (str, True)
