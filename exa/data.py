# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Data Objects
########################
Exa provides a `pandas`_ like Series and DataFrame object which support saving
and loading metadata when using the HDF format.
"""
import pandas as pd
from .typed import Typed, TypedClass, yield_typed
from .util.hdf import _spec_name


class Feature(object):
    """
    """
    pass


class _Base(TypedClass):
    """
    """
    _metadata = ['name', 'metadata']
    metadata = Typed(dict, doc="Persistent metadata")

    def to_hdf(self, path_or_buf, key, mode=None, complevel=None,
               complib=None, fletcher32=False, append=False, **kwargs):
        """
        Write the dataframe to and HDF.

        Args:
            path_or_buf (str, HDFStore): Path to HDF file or HDF file buffer
            key (str): Data object name
            mode (str): R/W mode for HDF file object
            complevel (str): Compression level
            complib (str): Compression library
            fletcher32 (bool): Checksum
            append (bool): Data for future appending
            kwargs: Passed to HDFStore.put/HDFStore.append
        """
        spec_name = kwargs.pop("spec_name", _spec_name)
        store = path_or_buf
        if not isinstance(store, pd.HDFStore):
            store = pd.HDFStore(path_or_buf, mode, complevel, complib, fletcher32)
        cls = self.__class__
        if spec_name not in store:
            store.put(spec_name, pd.Series())
        storer = store.get_storer(spec_name).attrs
        for suffix in yield_typed(cls):
            name = key + "_" + suffix
            storer[name] = getattr(self, suffix)
        self.__class__ = self._constructor_pandas
        if append:
            store.append(key, self, **kwargs)
        else:
            store.put(key, self, **kwargs)
        self.__class__ = cls
        store.close()


class DataSeries(pd.Series, _Base):
    """
    """
    @property
    def _constructor(self):
        return DataSeries

    @property
    def _constructor_pandas(self):
        return pd.Series

    @property
    def _constructor_expanddim(self):
        return DataFrame

    def __init__(self, *args, **kwargs):
        metadata = kwargs.pop("metadata", None)
        super(DataSeries, self).__init__(*args, **kwargs)
        self.metadata = metadata    # Prevents recursion error


class DataFrame(pd.DataFrame, _Base):
    """
    """

    @property
    def _constructor(self):
        return DataFrame

    @property
    def _constructor_pandas(self):
        return pd.DataFrame

    @property
    def _constructor_sliced(self):
        return DataSeries

    def __init__(self, *args, **kwargs):
        metadata = kwargs.pop("metadata", None)
        super(DataFrame, self).__init__(*args, **kwargs)
        self.metadata = metadata     # Prevents recursion error



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
