# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Containers
########################
This module provides the generic :class:`~exa.container.Container` object.
Containers store data objects (ints, floats, lists, `numpy` arrays, `pandas`
objects, etc.) that can be saved to `HDF` files for permanent storage.
Containers can be iterated over and support other basic collections-like
features such as length checks and element deletion. Containers can estimate
the total size (in memory) of their data objects. They do not make a copy
of their data by default.


Containers can be used to
Containers 
Developers 
Containers facilitate systematic data architecture by allowing developers to
build data specific :class:`~exa
Containers 
Containers allo

Containers are used to store a collection of data objects (such as scalars,
lists, arrays, dataframes, etc.). By default the :class:`~exa.container.Container`
enables investigation of the metadata of the data objects it holds. The object
also provides methods for saving the data to disk in common formats such as HDF.
For well structured data such as dataframes, the :class:`~exa.container.Container`
can identify relationships (i.e. relationships between index names and column
names of different dataframes). The :class:`~exa.container.Container` is
extensible and can be used to construct a unified API for a data specific task.
"""
import tables
import warnings
import numpy as np
import pandas as pd
from copy import deepcopy
from sys import getsizeof
from collections import defaultdict
from exa.typed import TypedClass, Typed
from .data import _spec_name, _forbidden, Field
if not hasattr(pd.Series, "items"):
    pd.Series.items = pd.Series.iteritems


class Container(TypedClass):
    """
    Wrapper for data processing, analysis, and storage.

    Containers accept most data formats, scalars (ints, floats, etc.), arrays (lists,
    tuples, numpy arrays), and structured data (pandas series and dataframes).
    Any number of objects may be stored as part of a Container. They can all
    be saved to disk at once using the :func:`~exa.core.container.Container.to_hdf`
    method..

    .. code-block:: python

        c = Conatiner(array=np.random.rand(10), a=[1, 2, 3])
        c.to_hdf("my.hdf")
        d = Container.from_hdf("my.hdf")

    Containers support type enforcement for their attributes.

    .. code-block:: python

    A storage object for data such as scalars (ints, floats, strs), arrays
    (lists, numpy objects), and structured data (pandas series and dataframe
    objects).

    TODO
    """
    meta = Typed(dict, doc="Document metadata")

    def info(self):
        """Displays metadata on the Container's data objects."""
        df = []
        for name, item in self.items():
            typ = item.__class__.__name__
            size = float(getsizeof(item))/(1024.0**2)
            if hasattr(item, "shape"):
                shape = str(item.shape)
            elif hasattr(item, "size"):
                if callable(item.size):
                    shape = str(item.size().to_dict())
            else:
                try:
                    shape = str(len(item))
                except (TypeError, AttributeError):
                    shape = "nan"
            df.append([name, typ, size, shape])
        columns = ("attribute", "type", "size (MiB)", "shape")
        return pd.DataFrame(df, columns=columns).set_index("attribute").sort_index()

    def network(self):
        """
        Display information about relationships between data objects.

        Dataframes with unique indices are like database tables where the index
        is a primary key. If, in another dataframe, a column with the same name
        as that index exists, it is akin to a database table's foreign key.
        Foreign keys define relationships between dataframes.
        """
        # Pick a default plotting system (bokeh, mpl, seaborn, etc.)
        raise NotImplementedError()

    def memory_usage(self):
        """
        Return total (estimated) memory usage (in MiB).
        """
        return self.info()['size (MiB)'].sum()

    def to_hdf(self, path, mode='a', append=None, sparse=0.95,
               complevel=0, complib=None, fletcher32=False, **kwargs):
        """
        Save the container's data to an HDF file.

        Exa specific data objects save their data as well as any additional
        (typed) attributes (e.g. dictionary of metadata). This method addtionally
        handles Python built-in types and numpy objects. Built-in types are
        saved as attributes of the special storer (default '__exa_storer__').
        Numpy arrays are saved using `pytables`_ machinery.

        Args:
            path (str): File path
            mode (str): Writing mode
            append (list): List of object names which are appendable
            sparse (float): Minimum density for sparse data structure
            complevel (int): Compression level
            complib (str): Compression library
            fletcher32 (bool): Checksum
            kwargs: Additional keyword arguments to be passed to put/append

        Warning:
            Existing data objects with the same name in the current HDF file
            (if applicable) will be overwritten unless the correct mode and append
            arguments are used. Scalar variables will always be overwritten (if
            they exist) or added to the collection of existing scalars (if they
            don't). Numpy and Python objects do not support append operations.

        See Also:
            Additional arguments can be found in `pandas`_ documentation.

        Note:
            Passing the keyword argument warn = False will prevent warnings from
            being shown.

        .. _pytables: http://www.pytables.org
        .. _pandas: https://pandas.pydata.org
        """
        warn = kwargs.pop("warn", True)
        # On first pass, identify which data objects we can save
        # and what method (pandas/pytables) must be used.
        numpy_save = {}
        pandas_save = {}
        special_save = {}
        for name, data in self.items():
            if isinstance(data, (np.ndarray, Field)):
                numpy_save[name] = data
            elif isinstance(data, (pd.Series, pd.DataFrame, pd.SparseSeries,
                                   pd.SparseDataFrame)):
                pandas_save[name] = data
            elif isinstance(data, (str, int, float, complex, dict, list, tuple)):
                special_save[name] = data
            elif data is not None and warn == True:
                warnings.warn("Data object '{}' ({}) not saved (unsupported).".format(name, type(data)))
        # First save numpy objects
        if len(numpy_save) > 0:
            filters = tables.Filters(complib=complib, complevel=complevel)
            store = tables.open_file(path, mode=mode, filters=filters)
            for name, data in numpy_save.items():
                if isinstance(data, Field):
                    store.create_carray("/", name+"__VALUES__", obj=data.values)
                    store.create_carray("/", name+"__DIMENSIONS__", obj=data.grid)
                else:
                    store.create_carray("/", name, obj=data)
            store.close()
        # Save remaining objects
        store = pd.HDFStore(path, mode=mode, complevel=complevel,
                            complib=complib, fletcher32=fletcher32)
        if _spec_name not in store:
            store.put(_spec_name, pd.Series())
        special = store.get_storer(_spec_name).attrs
        for name, data in special_save.items():
            special[name] = data
        for name, data in pandas_save.items():
            if ((isinstance(append, (list, tuple)) and name in append) or
                append == True or name == append):
                data.to_hdf(store, name, append=True, close=False, **kwargs)
            else:
                data.to_hdf(store, name, close=False)
        store.close()

    @classmethod
    def from_hdf(cls, path, complib=None, complevel=0, fletcher32=False):
        """
        Load a container from an HDF file.

        Args:
            path (str): Path to HDF file

        Returns:
            container: Container object with data attributes

        Warning:
            Any saved :class:`~exa.core.data.Field` objects will be returned
            as the default (aforementioned) type (instead of a possibly derived
            type).
        """
        kwargs = {}
        # First load pandas-like and special objects
        store = pd.HDFStore(path, mode="r", complib=complib,
                            complevel=complevel, fletcher32=fletcher32)
        fields = defaultdict(dict)
        if _spec_name in store:
            for name, data in vars(store.get_storer(_spec_name).attrs).items():
                if "__VALUES__" in name:
                    n = name.replace("__VALUES__", "")
                    fields[n]['values'] = data
                elif "__DIMENSIONS__" in name:
                    n = name.replace("__DIMENSIONS__")
                    fields[n]['dimensions'] = data
                elif name not in _forbidden:
                    kwargs[name] = data
        kwargs.update({name: Field(**fields[name]) for name in fields})
        for name, data in store.items():
            kwargs[name] = data
        store.close()
        # Second load numpy-like objects
        filters = tables.Filters(complib=complib, complevel=complevel)
        store = tables.open_file(path, mode="r", filters=filters)
        for data in store.walk_nodes():
            if hasattr(data, "name") and data.name not in kwargs:
                kwargs[data.name] = data.read()
        store.close()
        # Finally combine Field objects (values and dimensions)
        return cls(**kwargs)

    def _network(self):
        """Helper function to generate the nodes and edges of the network."""
        nodes = {}
        edges = []
        for name, item in self.items():
            if isinstance(item, pd.DataFrame):
                nodes[name] = (item.index.name, item.columns.values)
        for key0, (index_name0, column_names0) in nodes.items():
            for key1, (index_name1, column_names1) in nodes.items():
                if key0 == key1:
                    continue
                if ((index_name0 is not None and any(col == index_name0 for col in column_names1)) or
                    (index_name1 is not None and any(col == index_name1 for col in column_names0))):
                    pair = sorted((key0, key1))
                    if pair not in edges:
                        edges.append(pair)
        return sorted(nodes.keys()), sorted(edges)

    def items(self):
        """Generator of data object name, data object pairs for iteration over."""
        for name, data in vars(self).items():
            # For properties, yield modified name without leading underscore
            if hasattr(self.__class__, name) and isinstance(getattr(self.__class__, name), property) and name.startswith("_"):
                yield name[1:], data
            yield name, data 

    def __contains__(self, key):
        if hasattr(self, key):
            return True

    def __eq__(self, other):
        for name, data in self._items():
            if name in other and not np.all(getattr(other, name) == data):
                return False
        return True

    def __len__(self):
        return len(vars(self).keys())

    def __delitem__(self, key):
        if key in vars(self):
            delattr(self, key)

    def __sizeof__(self):
        """Note that this function must return a Python integer."""
        return int(np.ceil(self.memory_usage()*1024**2))

    def __init__(self, *args, **kwargs):
        """
        Create a new container.

        Args:
            meta (dict): Dictionary of metadata about the container (default none)
            copy (bool): Make a (deep) copy of the data (default false)
            kwargs: Named data objects (str, int, list, tuple, numpy, pandas, etc.)
        """
        cp = kwargs.pop("copy", False)
        self.meta = kwargs.pop("meta", None)
        for name, data in kwargs.items():
            if cp:
                setattr(self, name, deepcopy(data))
            else:
                setattr(self, name, data)

    def __repr__(self):
        n = self.__class__.__name__
        size = getsizeof(self)
        return "{}(data={}, size (MiB)={})".format(n, len(self), size)


def concatenate(*containers, **kwargs):
    """
    Concatenate containers' data and create a new container object.

    Args:
        containers (iterable): Collection of container objects to concatenate
        axis (int, dict): Axis along which to concatenate (dictionary with data object name, int pairs)
        join (str): How to join indices of other axis (default, 'outer')
        ignore_index (bool): Reset concatenation index values (default False)
    """
    raise NotImplementedError()
