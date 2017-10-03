# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Data Objects
########################
Exa provides a `pandas`_ like Series and DataFrame object which support saving
and loading metadata when using the HDF format.
"""
import six
import warnings
import numpy as np
import pandas as pd
from pandas.io import pytables
from pandas.core.dtypes.dtypes import CategoricalDtypeType
from exa.typed import Typed, TypedMeta, yield_typed, TypedClass


#4 Default values used for pandas compatibility
_npmap = {int: (np.int, np.int_, np.int0, np.int8, np.int16, np.int32,
                np.int64),
          float: (np.float, np.float_, np.float16, np.float32, np.float64),
          str: (np.object, np.object_, np.object0),
          complex: (np.complex, np.complex_, np.complex64, np.complex128)}
_spec_name = "__exa_storer__"
_forbidden = ("CLASS", "TITLE", "VERSION", "pandas_type", "pandas_version",
              "encoding", "index_variety", "name")


class _Param(TypedClass):
    """
    Args:
        typ: Type or iterable of acceptable types
        required (bool): Mandatory name/value (default True)
        auto (bool): Attempt automatic conversion (default True)
    """
    dtype = Typed(type)
    dtypes = Typed(dict)
    index = Typed((bool, pd.Index))
    value = Typed(str)

    def check(self, data):
        """Perform internal checks then default checks."""
        self._check(data)
        if len(data) > 0 and len(self.typ) > 0 and self.typ[0] is not None:
            self.check_type(data)

    def check_type(self, data):
        """Overwritten below."""
        raise NotImplementedError()

    def __call__(self, name):
        self.name = name
        return self

    def __init__(self, typ=None, required=False, auto=True, verbose=True):
        self.typ = typ if isinstance(typ, (list, tuple)) else (typ, )
        self.required = required
        self.auto = auto
        self.verbose = verbose


class Index(_Param):
    """
    A required index.

    .. code-block:: python

        class Foo(DataFrame):
            idx0 = Index(int, level=0)
            idx1 = Index(int, level=1)

    Args:
        typ: Type or iterable of acceptable types
        required (bool): Mandatory name/value (default True)
        level (int): If multiindex, index level (default None)
        auto (bool): Automatic type conversion
        verbose (bool): Report warnings

    Note:
        Numeric types must used must be numpy types.
    """
    def _check(self, data):
        """Assert data object validity."""
        if self.name not in data.index.names and self.auto:
            data.index.set_names(self.name, level=self.level, inplace=True)
        if self.required and self.name not in data.index.names:
            raise NameError("No index with name {}".format(self.name))

    def check_type(self, data):
        """Type check."""
        lvl = 0 if self.level is None else self.level
        ty = data.index.get_level_values(lvl).dtype.type
        for t in self.typ:
            if t is ty or t in _npmap and ty in _npmap[t]:
                return
        # If not already the correct type and conversion is set to occur
        if self.auto:
            if hasattr(data.index, "levels"):
                for t in self.typ:
                    t = 'category' if t is CategoricalDtypeType else t
                    try:
                        setter = []
                        for i, l in enumerate(data.index.levels):
                            if i == lvl:
                                setter.append(l.astype(t))
                            else:
                                setter.append(l)
                        data.index = data.index.set_levels(setter)
                        if self.verbose:
                            warnings.warn("Index {} type converted to {}".format(lvl, t.__name__))
                        return
                    except (TypeError, ):
                        pass
            else:
                for t in self.typ:
                    t = 'category' if t is CategoricalDtypeType else t
                    try:
                        data.index = data.index.astype(t)
                        if self.verbose:
                            warnings.warn("Index type converted to {}".format(t.__name__))
                        return
                    except (TypeError, ):
                        pass
        raise TypeError("Wrong type for index '{}' with type {} (expected {})".format(self.name, ty, self.typ))

    def __init__(self, *args, **kwargs):
        level = kwargs.pop("level", None)
        kwargs['required'] = kwargs.pop("required", True)
        super(Index, self).__init__(*args, **kwargs)
        self.level = level


class Column(_Param):
    """
    A required column.

    .. code-block:: python

        class Foo(DataFrame):
            reqcol = Column(int, required=True)

    Args:
        typ: Type or iterable of acceptable types
        required (bool): Mandatory name/value (default True)
        auto (bool): Automatic type conversion
        verbose (bool): Report warnings

    Note:
        Numeric types must used must be numpy types.
    """
    def _check(self, data):
        """Custom checks specific to columns."""
        if self.required and self.name not in data.columns:
            raise NameError("No column with name {}".format(self.name))

    def check_type(self, data):
        """Check type."""
        if self.name in data.columns:
            ty = data[self.name].dtype.type
            for t in self.typ:
                if t is ty or t in _npmap and ty in _npmap[t]:
                    return
            if self.auto:
                for t in self.typ:
                    t = 'category' if t is CategoricalDtypeType else t
                    try:
                        data[self.name] = data[self.name].astype(t)
                        if self.verbose:
                            warnings.warn("Column '{}' type converted to {}".format(self.name, t.__name__))
                        return
                    except Exception:
                        pass
            raise TypeError("Wrong type for column '{}' with type {} (expected {})".format(self.name, ty, self.typ))


class _BaseMeta(TypedMeta):
    """
    This metaclass inspects data class objects and modifies their
    required data parameters upon instantiation.
    """
    def __new__(mcs, name, bases, clsdict):
        kwargs = {}
        params = []
        for key, item in clsdict.items():
            if isinstance(item, _Param):
                params.append(item(key))
            else:
                kwargs[key] = item
        kwargs['_params'] = params
        return super(_BaseMeta, mcs).__new__(mcs, name, bases, kwargs)


class _Base(six.with_metaclass(_BaseMeta)):
    """
    A base class for structured data objects. Structured data objects may
    have requirements on their indices/features. These features are handled
    by the :class:`~exa.core.data._BaseMeta` metaclass and
    :class:`~exa.core.data._Param` objects (e.g. :class:`~exa.core.data.Column`).
    """
    _metadata = ['name', 'meta']
    _params = Typed(tuple, doc="Column/index requirements of the data object.")
    meta = Typed(dict, doc="Persistent metadata.")

    def to_hdf(self, store, name, mode=None, complevel=None,
               complib=None, fletcher32=False, append=False, **kwargs):
        """
        Write data to an HDF file.

        Args:
            store (str, HDFStore): Path to HDF file or HDF file buffer
            name (str): Data object name
            mode (str): R/W mode for HDF file object
            complevel (int): Compression level
            complib (str): Compression library
            fletcher32 (bool): Checksum
            append (bool): Data for future appending
            kwargs: Passed to HDFStore.put/HDFStore.append
        """
        close = kwargs.pop("close", True)
        if not isinstance(store, pd.HDFStore):
            store = pd.HDFStore(store, mode=mode, complevel=complevel,
                                complib=complib, fletcher32=fletcher32)
        # Save the data
        if append:
            store.append(name, self, **kwargs)
        else:
            store.put(name, self, **kwargs)
        # Save the additional attributes (e.g. metadata)
        storer = store.get_storer(name)
        for key in yield_typed(self):
            storer.attrs[key] = getattr(self, key)
        if close == True:
            store.close()

    @classmethod
    def from_hdf(cls, store, name):
        """
        Read a data object (including attrs, e.g. metadata) from an HDF file.

        Args:
            store (str, HDFStore): Full file path to HDF or HDF buffer
            name (str): Name of data object to load
        """
        if not isinstance(store, pd.HDFStore):
            store = pd.HDFStore(store, mode="r")
        # Load data
        data = store.get(name)
        # Load metadata
        kwargs = {}
        storer = store.get_storer(name)
        for key in yield_typed(cls):
            if key in storer.attrs:
                kwargs[key] = storer.attrs[key]
        store.close()
        return cls(data, **kwargs)

    def _enforce(self):
        """Enforce format of columns and indices."""
        for param in self._params:
            param.check(self)

    def __setitem__(self, *args, **kwargs):
        """Setitem is called on column manipulations so we recheck columns."""
        super(_Base, self).__setitem__(*args, **kwargs)
        self._enforce()

    def __init__(self, *args, **kwargs):
        meta = kwargs.pop("meta", None)
        super(_Base, self).__init__(*args, **kwargs)
        self.meta = meta
        self._enforce()


class DataSeries(_Base, pd.Series):
    """
    Labeled, structured, n-dimensional, singly featured array.
    """
    _constructor_pandas = pd.Series

    @property
    def _constructor(self):
        return DataSeries

    @property
    def _constructor_expanddim(self):
        return DataFrame


class DataFrame(_Base, pd.DataFrame):
    """
    Labeled, structured, n-dimensional, multiply featured array.
    """
    _constructor_pandas = pd.DataFrame

    @property
    def _constructor(self):
        return DataFrame

    @property
    def _constructor_sliced(self):
        return DataSeries


class SparseDataSeries(_Base, pd.SparseSeries):
    """
    Sparse, labeled, structured, n-dimensional, singly featured array.
    """
    _constructor_pandas = pd.SparseSeries

    @property
    def _constructor(self):
        return SparseDataSeries

    @property
    def _constructor_expanddim(self):
        return SparseDataFrame


class SparseDataFrame(_Base, pd.SparseDataFrame):
    """
    Sparse, labeled, structured, n-dimensional, multiply featured array.
    """
    _constructor_pandas = pd.SparseDataFrame
    _constructor_sliced = SparseDataSeries

    @property
    def _constructor(self):
        return SparseDataFrame


def concat(*data, **kwargs):
    raise NotImplementedError()


# Required exa data objects' HDF compatibility
for cls in (DataFrame, DataSeries, SparseDataFrame, SparseDataSeries):
    pytables._TYPE_MAP[cls] = pytables._TYPE_MAP[cls._constructor_pandas]
    if cls._constructor_pandas in pytables._AXES_MAP:
        pytables._AXES_MAP[cls] = pytables._AXES_MAP[cls._constructor_pandas]


#import six
#import pandas as pd
#from .base import Base
#from exa.functions import LazyFunction
#from exa.typed import TypedMeta, TypedProperty
#
#
#class Feature(LazyFunction):
#    """
#    A description of a column in a :class:`~exa.core.dataframe.DataFrame`.
#    """
#    def to_dict(self, *args, **kwargs):
#        """Returns a dictionary of kwargs."""
#        return self.kwargs
#
#    def __init__(self, dtypes, required=False, findex=None):
#        """
#        Args:
#            dtypes (iterable, type): Dtype or iterable of dtypes of the feature (column)
#            required (bool): Required column for dataframe creation
#            findex (iterable): Foreign index names (on which groupby occurs)
#            func (function):
#        """
#        if not isinstance(dtypes, (list, tuple)):
#            dtypes = (dtypes, )
#        super(Feature, self).__init__(fn=self.to_dict, required=required,
#                                      findex=findex, dtypes=dtypes)
#
#
#class BaseMeta(TypedMeta):
#    """A typed metaclass for dataframes."""
#    def __new__(mcs, name, bases, namespace):
#        reqcols = []
#        coltypes = {}
#        # Make a copy of the namespace and modify the original
#        for attr_name, attr in dict(namespace).items():
#            if isinstance(attr, Feature):
#                # Remove the attr from the name space
#                kwargs = attr()
#                coltypes[attr_name] = kwargs['dtypes']
#                if kwargs['required']:
#                    reqcols.append(attr_name)
#        namespace['reqcols'] = reqcols
#        namespace['coltypes'] = coltypes
#        return super(BaseMeta, mcs).__new__(mcs, name, bases, namespace)
#
#
#class DataFrame(six.with_metaclass(BaseMeta, pd.DataFrame, Base)):
#    """
#    A `pandas`_ like `dataframe`_ with support for required columns, required
#    column dtypes, and convenience method creation.
#
#    A special syntax is used to create required columns or statically (d)typed
#    columns. An illustration follows with descriptions in the comments.
#
#    .. code-block:: python
#
#        class MyDataFrame(DataFrame):
#            col0 = float        # Opt. col; enforced dtype float
#            col1 = (int, True)  # Req. col; enforced dtype int
#            col2 = (None, True) # Req. col; any dtype allowed
#            col3 = (int, float) # Opt. col; enforced int, then float
#            col4 = ((int, float), True)  # Req., multiple types
#
#    In the last example ``col3`` (an optional column) is preferred to be of dtype
#    ``int`` with a fallback to ``float``; the column must be coerced to one of
#    these types otherwise a TypeError is raised.
#
#    .. _pandas: http://pandas.pydata.org/
#    .. _dataframe: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
#    """
#    # Note that the ``Base`` class, which requires the creation of an ``info``
#    # method is satisfied by the pandas DataFrame which provides that method.
#    _metadata = ["reqcols", "coltypes", "meta"]
#    reqcols = TypedProperty(list, "Required columns")
#    coltypes = TypedProperty(dict, "Column types")
#    aliases = TypedProperty(dict, docs="Column name aliases for automatic renaming")
#
#    def info(self, verbose=True, *args, **kwargs):
#        """Call the pandas DataFrame info method."""
#        kwargs['verbose'] = verbose
#        return super(DataFrame, self).info(*args, **kwargs)
#
#    @property
#    def _constructor(self):
#        return DataFrame
#
#    def _enforce_aliases(self):
#        """Automatic column naming using aliases."""
#        if isinstance(self.aliases, dict):
#            self.rename(columns=self.aliases, inplace=True)
#
#    def _enforce_columns(self):
#        """
#        Enforce required columns and dtypes using the ``coltypes`` and ``reqcols`` class
#        attribute (i.e. shared between all instances of this class); updated when
#        ``DataFrame.__new__`` is called.
#        """
#        # First check required columns.
#        if self.reqcols is not None:
#            missing = set(self.reqcols).difference(self.columns)
#            if len(missing) > 0:
#                raise NameError("Missing column(s) {}".format(missing))
#            # Second convert types.
#            dtypes = self.dtypes
#            for name, types in self.coltypes.items():
#                if name in dtypes and types is not None and types[0] != dtypes[name]:
#                    for typ in types:
#                        try:
#                            super(DataFrame, self).__setitem__(name, self[name].astype(typ))
#                            break    # Stop on successful convert
#                        except TypeError:
#                            pass
#                    else:
#                        raise TypeError("Unable to enforce column types for {} as types {}".format(name, types))
#
#    def _enforce_index(self):
#        """
#        Ensure that we have a unique index to use with the same name as the
#        class name (lowercase).
#        """
#        if isinstance(self.index, pd.MultiIndex):
#            self.reset_index(inplace=True)
#        self.index.name = self.__class__.__name__.lower()
#
#    def _enforce(self):
#        """Enforce format of columns and indices."""
#        self._enforce_aliases()
#        self._enforce_index()
#        self._enforce_columns()
#
#    def __setitem__(self, *args, **kwargs):
#        """Setitem is called on column manipulations so we recheck columns."""
#        super(DataFrame, self).__setitem__(*args, **kwargs)
#        self._enforce()
#
#    def __init__(self, *args, **kwargs):
#        meta = kwargs.pop("meta", None)
#        super(DataFrame, self).__init__(*args, **kwargs)
#        self._enforce()
#        self.meta = meta
#
#
#class SectionDataFrame(DataFrame):
#    """
#    A dataframe that describes :class:`~exa.core.parser.Sections` object sections.
#
#    Instances of this dataframe describe the starting and ending points of
#    regions of a text file to be parsed. Upon creation of instances of this
#    object, the 'attribute' column is added which suggests the name of the
#    attribute (on the instance of :class:`~exa.core.parser.Sections`) to which
#    a given text region belongs.
#    """
#    _section_name_prefix = "section"
#    parser = Feature(object, True)
#    start = Feature(int, True)
#    end = Feature(int, True)
#
#    def __init__(self, *args, **kwargs):
#        super(SectionDataFrame, self).__init__(*args, **kwargs)
#        self['attribute'] = [self._section_name_prefix+str(i).zfill(len(str(len(self)))) for i in self.index]
#
#
#class Composition(DataFrame):
#    """
#    A dataframe that describes the structure of :class:`~exa.core.composer.Composer`.
#
#    Instances of this dataframe contain information used to dynamically
#    construct a compsed editor using data stored in Python objects and a string
#    template.
#    """
#    length = Feature(None, True)
#    joiner = Feature(str, True)
#    name = Feature(str, True)
