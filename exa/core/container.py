# -*- coding: utf-8 -*-
# Copyright (c) 2015-2017, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Containers
########################
This module provides the generic :class:`~exa.container.Container` object.
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
from uuid import uuid4
from sys import getsizeof
from exa.typed import TypedClass, Typed
from .data import _spec_name, _forbidden
if not hasattr(pd.Series, "items"):
    pd.Series.items = pd.Series.iteritems


class Container(TypedClass):
    """
    A storage object for data such as scalars (ints, floats, strs), arrays
    (lists, numpy objects), and structured data (pandas series and dataframe
    objects).

    TODO
    """
    default_prefix = Typed(str, doc="Default prefix for container args.")
    meta = Typed(dict, doc="Document metadata")

    def info(self):
        """
        Display information about the data objects.
        """
        df = []
        for name, item in self._items():
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
        for name, data in self._items():
            if isinstance(data, np.ndarray):
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
        """
        kwargs = {}
        # First load pandas-like and special objects
        store = pd.HDFStore(path, mode="r", complib=complib,
                            complevel=complevel, fletcher32=fletcher32)
        if _spec_name in store:
            for name, data in vars(store.get_storer(_spec_name).attrs).items():
                if name in _forbidden:
                    continue
                kwargs[name] = data
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
        return cls(**kwargs)

    def _network(self):
        """Helper function to generate the nodes and edges of the network."""
        nodes = {}
        edges = []
        for name, item in self._items():
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

    def _items(self, dct=None, include_keys=False):
        """
        Iterator for looping over data objects in the current container.
        """
        if dct is None:
            dct = vars(self)
        for key, data in dct.items():
            # Determine the correct name to use
            if (key.startswith("_") and hasattr(self.__class__, key[1:]) and
                isinstance(getattr(self.__class__, key[1:]), property)):
                name = key[1:]
            else:
                name = key
            if include_keys == True:
                yield key, name, data
            else:
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
        self.default_prefix = kwargs.pop("default_prefix", "obj_")
        self.meta = kwargs.pop("meta", None)
        for arg in args:
            do = True
            # The while check is used to make sure names do not overlap...
            # ... chances of that are incredibly small so I am not sure it
            # is necessary but it doesn't really affect performance???
            while do:
                name = self.default_prefix + uuid4().hex
                if not hasattr(self, name):
                    setattr(self, name, arg)
                    do = False
        for name, data in kwargs.items():
            setattr(self, name, data)

    def __repr__(self):
        n = self.__class__.__name__
        size = np.round(self.memory_usage(), 3)
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


##    def network(self, figsize=(14, 9), fig=True):
##        """
##        Display information about the container's object relationships.
##
##        Nodes correspond to data objects. The size of the node corresponds
##        to the size of the table in memory. The color of the node corresponds
##        to its fundamental data type. Nodes are labeled by their container
##        name; class information is listed below. The color of the connections
##        correspond to the type of relationship; either an index of one table
##        corresponds to a column in another table or the two tables share an
##        index.
##
##        Args:
##            figsize (tuple): Tuple containing figure dimensions
##            fig (bool): Generate the figure (default true)
##
##        Returns:
##            graph: Network graph object containing data relationships
##        """
##        conn_types = ['index-index', 'index-column']
##        conn_colors = mpl.color_palette(n=len(conn_types))
##        conn = dict(zip(conn_types, conn_colors))
##
##        def get_node_type_color(obj):
##            """Gets the color of a node based on the node's (sub)type."""
##            typs = [Field, SparseSeries, DataFrame, SparseDataFrame, Series, pd.DataFrame, pd.Series]
##            cols = mpl.color_palette(n=len(typs))
##            for typ, col in zip(typs, cols):
##                if isinstance(obj, typ):
##                    return '.'.join((typ.__module__, typ.__name__)), col
##            return 'other', 'gray'
##
##        def legend(items, name, loc, ax):
##            """Legend creation helper function."""
##            proxies = []
##            descriptions = []
##            for label, color in items:
##                if label == 'column-index':
##                    continue
##                if name == 'Data Type':
##                    line = mpl.sns.mpl.lines.Line2D([], [], linestyle='none', color=color, marker='o')
##                else:
##                    line = mpl.sns.mpl.lines.Line2D([], [], linestyle='-', color=color)
##                proxies.append(line)
##                descriptions.append(label)
##            lgnd = ax.legend(proxies, descriptions, title=name, loc=loc, frameon=True)
##            lgnd_frame = lgnd.get_frame()
##            lgnd_frame.set_facecolor('white')
##            lgnd_frame.set_edgecolor('black')
##            return lgnd, ax
##
##        info = self.info()
##        info = info[info['type'] != '-']
##        info['size'] *= 15000/info['size'].max()
##        info['size'] += 5000
##        node_size_dict = info['size'].to_dict()      # Can pull all nodes from keys
##        node_class_name_dict = info['type'].to_dict()
##        node_type_dict = {}    # Values are tuple of "underlying" type and color
##        node_conn_dict = {}    # Values are tuple of connection type and color
##        items = self._data().items()
##        for k0, v0 in items:
##            n0 = k0[1:] if k0.startswith('_') else k0
##            node_type_dict[n0] = get_node_type_color(v0)
##            for k1, v1 in items:
##                if v0 is v1:
##                    continue
##                n1 = k1[1:] if k1.startswith('_') else k1
##                for name in v0.index.names:    # Check the index of data object 0 against the index
##                    if name is None:           # and columns of data object 1
##                        continue
##                    if name in v1.index.names:
##                        contyp = 'index-index'
##                        node_conn_dict[(n0, n1)] = (contyp, conn[contyp])
##                        node_conn_dict[(n1, n0)] = (contyp, conn[contyp])
##                    for col in v1.columns:
##                        # Catches index "atom", column "atom1"; does not catch atom10
##                        isrelated = False
##                        if name == col:
##                            isrelated = True
##                        elif isinstance(col, str) and (name == col[:-1] and col[-1].isdigit()):
##                            isrelated = True
##                        if isrelated == True:
##                            contyp = 'index-column'
##                            node_conn_dict[(n0, n1)] = (contyp, conn[contyp])
##                            node_conn_dict[(n1, n0)] = ('column-index', conn[contyp])
##        g = nx.Graph()
##        g.add_nodes_from(node_size_dict.keys())
##        g.add_edges_from(node_conn_dict.keys())
##        node_sizes = [node_size_dict[node] for node in g.nodes()]
##        node_labels = {node: ' {}\n({})'.format(node, node_class_name_dict[node]) for node in g.nodes()}
##        node_colors = [node_type_dict[node][1] for node in g.nodes()]
##        edge_colors = [node_conn_dict[edge][1] for edge in g.edges()]
##        # Build the figure and legends
##        if fig:
##            fig, ax = mpl.sns.plt.subplots(1, figsize=figsize)
##            ax.axis('off')
##            pos = nx.spring_layout(g)
##            f0 = nx.draw_networkx_nodes(g, pos=pos, ax=ax, alpha=0.7, node_size=node_sizes,
##                                        node_color=node_colors)
##            f1 = nx.draw_networkx_labels(g, pos=pos, labels=node_labels, font_size=16,
##                                         font_weight='bold', ax=ax)
##            f2 = nx.draw_networkx_edges(g, pos=pos, edge_color=edge_colors, width=2, ax=ax)
##            l1, ax = legend(set(node_conn_dict.values()), 'Connection', (1, 0), ax)
##            l2, ax = legend(set(node_type_dict.values()), 'Data Type', (1, 0.3), ax)
##            del f0, f1, f2, l2
##            fig.gca().add_artist(l1)
##        g.edge_types = {node: value[0] for node, value in node_conn_dict.items()}  # Attached connection information to network graph
##        return g
