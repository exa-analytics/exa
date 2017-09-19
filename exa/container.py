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
import numpy as np
import pandas as pd
from uuid import uuid4
from sys import getsizeof
from .typed import TypedClass, Typed
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
    metadata = Typed(dict, doc="Metadata dictionary.")

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
        pass

    def memory_usage(self):
        """
        Return total (estimated) memory usage (in MiB).
        """
        return self.info()['size (MiB)'].sum()

    def to_hdf(self, path, mode='a', append=None, sparse=0.95, original_types="original_types",
               spec_store_name="__SPECIAL__", **kwargs):
        """
        Save the container's data to an HDF file.

        Not all data objects are compatible with the HDF format. Scalars (such as int,
        floats, etc.) and metadata (dict, if present) are saved

        Args:
            path (str): File path
            mode (str): Writing mode
            append (list): List of data object names which should written in an appendable format
            sparse (float): Minimum density for sparse data structure
            spec_store_name (str): Name of the HDF storer where scalars and specials are stored
            kwargs: Additional keyword arguments to be passed to pandas.HDFStore

        Warning:
            Existing data objects with the same name in the current HDF file
            (if applicable) will be overwritten unless the correct mode and append
            arguments are used. Scalar variables will always be overwritten (if
            they exist) or added to the collection of existing scalars (if they don't).

        See Also:
            Additional arguments can be found in pandas.HDFStore documentation.
        """
        dct = vars(self)
        append = [] if append is None else append
        forbidden = ("CLASS", "TITLE", "VERSION", "pandas_type", "pandas_version",
                     "encoding", "index_variety", "name", original_types)
        conv = {'ss': pd.SparseSeries, 's': pd.Series,
                'sd': pd.SparseDataFrame, 'd': pd.DataFrame}
        # Since not all data can be saved, filter through and determine what can
        # be saved and raise a warning for what can't.
        to_save = {}
        for key, name, data in self._items(dct, include_keys=True):
            # Determine if storage is possible
            typ = None
            if isinstance(data, (pd.Series, pd.SparseSeries,
                                 pd.DataFrame, pd.SparseDataFrame)):
                typ = "array"
            elif (isinstance(data, (str, int, float, complex)) or
                  (name == "metadata" and isinstance(data, dict))):
                typ = "scalar"
            else:
                try:
                    rho = pd.SparseSeries(data).density
                    if rho < sparse:
                        typ = "ss"
                    else:
                        typ = "s"
                except:
                    try:
                        rho = pd.SparseDataFrame(data).density
                        if rho < sparse:
                            typ = "sd"
                        else:
                            typ = "d"
                    except:
                        pass
                    pass
            # Raise a warning if the data cannot be saved.
            if typ is None and data is not None:
                warnings.warn("Unable to store '{}', {}, in HDF format.".format(name, type(data)))
            elif data is not None:
                to_save[name] = [key, typ, type(data)]
        df = pd.DataFrame.from_dict(to_save, orient="index")
        df.columns = ["key", "stored_type", "original_type"]
        # Open the HDF file and begin saving data
        store = pd.HDFStore(path, mode=mode, **kwargs)
        if spec_store_name not in store:
            store.put(spec_store_name, pd.Series())
        attrs = store.get_storer(spec_store_name).attrs
        setattr(attrs, original_types, df['original_type'].to_dict())
        for typ, group in df.groupby("stored_type"):
            if typ == "scalar":
                for name, key in group['key'].items():
                    setattr(attrs, name, dct[key])
            elif typ in conv.keys():
                for name, key in group['key'].items():
                    if name in append:
                        store.put(name, conv[typ](dct[key]), append=True, format="table")
                    else:
                        store.put(name, conv[typ](dct[key]), format="fixed")
            else:
                for name, key in group['key'].items():
                    if name in append:
                        store.put(name, dct[key], append=True, format="table")
                    else:
                        store.put(name, dct[key], format="fixed")
        store.close()

    @classmethod
    def from_hdf(cls, path, original_types="original_types", spec_store_name="__SPECIAL__"):
        """
        Load a container from an HDF file.
        """
        forbidden = ("CLASS", "TITLE", "VERSION", "pandas_type", "pandas_version",
                     "encoding", "index_variety", "name", original_types)
        kwargs = {}
        store = pd.HDFStore(path, mode="r")
        otypes = {}
        if spec_store_name in store:
            attrs = store.get_storer(spec_store_name).attrs
            otypes = getattr(attrs, original_types)
            kwargs.update({name: item for name, item in vars(attrs).items() if not name.startswith("_") and name not in forbidden})
        for name, item in store.items():
            if name == spec_store_name:
                continue
            if name in otypes:
                kwargs[name] = otypes[name](item)
            else:
                kwargs[name] = item
        store.close()
        return cls(**kwargs)

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
        self.metadata = kwargs.pop("metadata", None)
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
