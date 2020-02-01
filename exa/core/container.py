# Copyright (c) 2015-2020, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
"""
Container
########################
The :class:`~exa.core.container.Container` class is the primary object for
data processing, analysis, and visualization. In brief, containers are composed
of data objects whose contents are used for 2D and 3D visualization. Containers
also provide some content management and data relationship features.

See Also:
    For a description of data objects see :mod:`~exa.core.numerical`.
"""
import os
import logging
import numpy as np
import pandas as pd
import networkx as nx
from sys import getsizeof
from copy import deepcopy
from collections import defaultdict
from .numerical import check_key, Field, Series, DataFrame, SparseDataFrame
from exa.util.utility import convert_bytes


class Container(object):
    """
    Container class responsible for all features related to data management.
    """
    _getter_prefix = 'compute'
    _cardinal = None    # Name of the cardinal data table

    @property
    def log(self):
        name = '.'.join([self.__module__,
                         self.__class__.__name__])
        return logging.getLogger(name)

    def copy(self, name=None, description=None, meta=None):
        """
        Create a copy of the current object (may alter the container's name,
        description, and update the metadata if needed).
        """
        cls = self.__class__
        kwargs = self._rel(copy=True)
        kwargs.update(self._data(copy=True))
        if name is not None:
            kwargs['name'] = name
        if description is not None:
            kwargs['description'] = description
        if meta is not None:
            kwargs['meta'] = meta
        return cls(**kwargs)

    def concat(self, *args, **kwargs):
        """
        Concatenate any number of container objects with the current object into
        a single container object.

        See Also:
            For argument description, see :func:`~exa.core.container.concat`.
        """
        raise NotImplementedError()

    def slice_naive(self, key):
        """
        Naively slice each data object in the container by the object's index.

        Args:
            key: Int, slice, or list by which to extra "sub"-container

        Returns:
            sub: Sub container of the same format with a view of the data

        Warning:
            To ensure that a new container is created, use the copy method.

            .. code-block:: Python

                mycontainer[slice].copy()
        """
        kwargs = {'name': self.name, 'description': self.description, 'meta': self.meta}
        for name, data in self._data().items():
            k = name[1:] if name.startswith('_') else name
            kwargs[k] = data.slice_naive(key)
        return self.__class__(**kwargs)

    def slice_cardinal(self, key):
        """
        Slice the container according to its (primary) cardinal axis.

        The "cardinal" axis can have any name so long as the name matches a
        data object attached to the container. The index name for this object
        should also match the value of the cardinal axis.

        The algorithm builds a network graph representing the data relationships
        (including information about the type of relationship) and then traverses
        the edge tree (starting from the cardinal table). Each subsequent child
        object in the tree is sliced based on its relationship with its parent.

        Note:
            Breadth first traversal is performed.

        Warning:
            This function does not make a copy (if possible): to ensure a new
            object is created (a copy) use :func:`~exa.core.container.Container.copy`
            after slicing.

            .. code-block:: Python

                myslice = mycontainer[::2].copy()

        See Also:
            For data network generation, see :func:`~exa.core.container.Container.network`.
            For information about relationships between data objects see
            :mod:`~exa.core.numerical`.
        """
        if self._cardinal:
            cls = self.__class__
            key = check_key(self[self._cardinal], key, cardinal=True)
            g = self.network()
            kwargs = {self._cardinal: self[self._cardinal].loc[key], 'name': self.name,
                      'description': self.description, 'meta': self.meta}
            # Next traverse, breadth first, all data objects
            for parent, child in nx.bfs_edges(g, self._cardinal):
                if child in kwargs:
                    continue
                typ = g.edge_types[(parent, child)]
                if self._cardinal in self[child].columns and hasattr(self[child], 'slice_cardinal'):
                    kwargs[child] = self[child].slice_cardinal(key)
                elif typ == 'index-index':
                    # Select from the child on the parent's index (the parent is
                    # in the kwargs already).
                    kwargs[child] = self[child].loc[kwargs[parent].index.values]
                elif typ == 'index-column':
                    # Select from the child where the column (of the same name as
                    # the parent) is in the parent's index values
                    cdf = self[child]
                    kwargs[child] = cdf[cdf[parent].isin(kwargs[parent].index.values)]
                elif typ == 'column-index':
                    # Select from the child where the child's index is in the
                    # column of the parent. Note that this relationship
                    cdf = self[child]
                    cin = cdf.index.name
                    cols = [col for col in kwargs[parent] if cin == col or (cin == col[:-1] and col[-1].isdigit())]
                    index = kwargs[parent][cols].stack().astype(np.int64).values
                    kwargs[child] = cdf[cdf.index.isin(index)]
            return cls(**kwargs)

    def cardinal_groupby(self):
        """
        Create an instance of this class for every step in the cardinal dimension.
        """
        if self._cardinal:
            g = self.network()
            cardinal_indexes = self[self._cardinal].index.values
            selfs = {}
            cls = self.__class__
            for cardinal_index in cardinal_indexes:
                kwargs = {self._cardinal: self[self._cardinal].loc[[cardinal_index]]}
                for parent, child in nx.bfs_edges(g, source=self._cardinal):
                    if child in kwargs:
                        continue
                    typ = g.edge_types[(parent, child)]
                    if (self._cardinal in self[child].columns and 
                        hasattr(self[child], 'slice_cardinal')):
                        kwargs[child] = self[child].slice_cardinal(key)
                    elif typ == 'index-index':
                        # Select from the child on the parent's index
                        # (the parent is in the kwargs already).
                        print("child: ", child)
                        print("parent: ", parent)
                        print("kwargs: ", kwargs)
                        print(self[child].index)
                        print(self[child].values)
                        print(kwargs[parent].index.values)
                        kwargs[child] = self[child].loc[kwargs[parent].index.values]
                    elif typ == 'index-column':
                        # Select from the child where the column (of the same name as
                        # the parent) is in the parent's index values
                        cdf = self[child]
                        kwargs[child] = cdf[cdf[parent].isin(kwargs[parent].index.values)]
                    elif typ == 'column-index':
                        # Select from the child where the child's index is in the
                        # column of the parent. Note that this relationship
                        cdf = self[child]
                        cin = cdf.index.name
                        cols = [col for col in kwargs[parent] if cin == col or (cin == col[:-1] and col[-1].isdigit())]
                        index = kwargs[parent][cols].stack().astype(np.int64).values
                        kwargs[child] = cdf[cdf.index.isin(index)]
                selfs[cardinal_index] = cls(**kwargs)
        return selfs

    def info(self):
        """
        Display information about the container's data objects (note that info
        on metadata and visualization objects is also provided).

        Note:
            Sizes are reported in bytes.
        """
        names = []
        types = []
        sizes = []
        names.append('WIDGET')
        types.append('-')
        s = 0
        sizes.append(s)
        names.append('METADATA')
        types.append('-')
        s = 0
        for obj in self._rel().values():
            s += getsizeof(obj)
        sizes.append(s)
        for name, obj in self._data().items():
            names.append(name[1:] if name.startswith('_') else name)
            types.append('.'.join((obj.__module__, obj.__class__.__name__)))
            if isinstance(obj, pd.Series):
                sizes.append(obj.memory_usage())
            else:
                sizes.append(obj.memory_usage().sum())
        inf = pd.DataFrame.from_dict({'object': names, 'type': types, 'size': sizes})
        inf.set_index('object', inplace=True)
        return inf.sort_index()

    def memory_usage(self, string=False):
        """
        Get the memory usage estimate of the container.

        Args:
            string (bool): Human readable string (default false)

        See Also:
            :func:`~exa.core.container.Container.info`
        """
        if string:
            n = getsizeof(self)
            return ' '.join((str(s) for s in convert_bytes(n)))
        return self.info()['size']

    def network(self):
        """
        Generate a network of relationships between the data inside the
        container.

        Returns:
            graph: Network graph object containing data relationships
        """
        n = len(self._data())
        conn_types = ['index-index', 'index-column']
        conn_colors = ([(0.275191,0.194905,0.496005),
                       (0.212395,0.359683,0.55171),
                       (0.153364,0.497,0.557724),
                       (0.122312,0.633153,0.530398),
                       (0.288921,0.758394,0.428426),
                       (0.626579,0.854645,0.223353)]*n)[:n]
        conn = dict(zip(conn_types, conn_colors))

        def get_node_type_color(obj):
            """Gets the color of a node based on the node's (sub)type."""
            for col in conn_colors:
                if isinstance(obj, (pd.DataFrame, pd.Series, pd.SparseSeries,
                                    pd.SparseDataFrame)):
                    typ = type(obj)
                    return '.'.join((typ.__module__, typ.__name__)), col
            return 'other', 'gray'

        info = self.info()
        info = info[info['type'] != '-']
        info['size'] *= 13000/info['size'].max()
        info['size'] += 2000
        node_size_dict = info['size'].to_dict()    # Pull all nodes from keys
        node_class_name_dict = info['type'].to_dict()
        node_type_dict = {}    # Values are tup of "underlying" type and color
        node_conn_dict = {}    # Values are tup of connection type and color
        items = self._data().items()
        for k0, v0 in items:
            n0 = k0[1:] if k0.startswith('_') else k0
            node_type_dict[n0] = get_node_type_color(v0)
            for k1, v1 in items:
                if v0 is v1:
                    continue
                n1 = k1[1:] if k1.startswith('_') else k1
                # Check the index of data object 0 against the index
                for name in v0.index.names:
                    if name is None:           # and columns of data object 1
                        continue
                    if name in v1.index.names:
                        contyp = 'index-index'
                        node_conn_dict[(n0, n1)] = (contyp, conn[contyp])
                        node_conn_dict[(n1, n0)] = (contyp, conn[contyp])
                    for col in v1.columns:
                        # Catches index "atom", column "atom1";
                        # does not catch atom10
                        if name == col or (name == col[:-1] and
                                           col[-1].isdigit()):
                            contyp = 'index-column'
                            node_conn_dict[(n0, n1)] = (contyp, conn[contyp])
                            node_conn_dict[(n1, n0)] = ('column-index',
                                                        conn[contyp])
        g = nx.Graph()
        g.add_nodes_from(node_size_dict.keys())
        g.add_edges_from(node_conn_dict.keys())
        node_sizes = [node_size_dict[node] for node in g.nodes()]
        node_labels = {n: ' {}\n({})'.format(n, node_class_name_dict[n])
                       for n in g.nodes()}
        node_colors = [node_type_dict[n][1] for n in g.nodes()]
        edge_colors = [node_conn_dict[e][1] for e in g.edges()]
        # Attached connection information to network graph
        g.edge_types = {n: v[0] for n, v in node_conn_dict.items()}
        return g

    def save(self, path=None, complevel=1, complib='zlib'):
        """
        Save the container as an HDF5 archive.

        Args:
            path (str): Path where to save the container
        """
        if path is None:
            path = self.hexuid + '.hdf5'
        elif os.path.isdir(path):
            path += os.sep + self.hexuid + '.hdf5'
        elif not (path.endswith('.hdf5') or path.endswith('.hdf')):
            raise ValueError('File path must have a ".hdf5" or ".hdf" extension.')
        with pd.HDFStore(path, 'w', complevel=complevel, complib=complib) as store:
            store['kwargs'] = pd.Series()
            store.get_storer('kwargs').attrs.metadata = self._rel()
            fc = 0    # Field counter (see special handling of fields below)
            for name, data in self._data().items():
                if hasattr(data, '_revert_categories'):
                    data._revert_categories()
                name = name[1:] if name.startswith('_') else name
                if isinstance(data, Field):    # Fields are handled separately
                    fname = 'FIELD{}_'.format(fc) + name + '/'
                    store[fname + 'data'] = pd.DataFrame(data)
                    for i, field in enumerate(data.field_values):
                        ffname = fname + 'values' + str(i)
                        if isinstance(field, pd.Series):
                            store[ffname] = pd.Series(field)
                        else:
                            store[ffname] = pd.DataFrame(field)
                    fc += 1
                elif isinstance(data, Series):
                    s = pd.Series(data)
                    if isinstance(data.dtype, pd.types.dtypes.CategoricalDtype):
                        s = s.astype('O')
                    store[name] = s
                elif isinstance(data, DataFrame):
                    store[name] = pd.DataFrame(data)
                elif isinstance(data, pd.SparseSeries):
                    s = pd.SparseSeries(data)
                    if isinstance(data.dtype, pd.types.dtypes.CategoricalDtype):
                        s = s.astype('O')
                    store[name] = s
                elif isinstance(data, SparseDataFrame):
                    store[name] = pd.SparseDataFrame(data)
                else:
                    if hasattr(data, 'dtype') and isinstance(data.dtype, pd.types.dtypes.CategoricalDtype):
                        data = data.astype('O')
                    else:
                        for col in data:
                            if isinstance(data[col].dtype, pd.types.dtypes.CategoricalDtype):
                                data[col] = data[col].astype('O')
                    store[name] = data
                if hasattr(data, '_set_categories'):
                    data._set_categories()

    def to_hdf(self, *args, **kwargs):
        """Alias of :func:`~exa.core.container.Container`."""
        self.save(*args, **kwargs)

    @classmethod
    def load(cls, pkid_or_path=None):
        """
        Load a container object from a persistent location or file path.

        Args:
            pkid_or_path: Integer pkid corresponding to the container table or file path

        Returns:
            container: The saved container object
        """
        path = pkid_or_path
        if isinstance(path, (int, np.int32, np.int64)):
            raise NotImplementedError('Lookup via CMS not implemented.')
        elif not os.path.isfile(path):
            raise FileNotFoundError('File {} not found.'.format(path))
        kwargs = {}
        fields = defaultdict(dict)
        with pd.HDFStore(path) as store:
            for key in store.keys():
                if 'kwargs' in key:
                    kwargs.update(store.get_storer(key).attrs.metadata)
                elif "FIELD" in key:
                    name, dname = "_".join(key.split("_")[1:]).split("/")
                    dname = dname.replace('values', '')
                    fields[name][dname] = store[key]
                else:
                    name = str(key[1:])
                    kwargs[name] = store[key]
        for name, field_data in fields.items():
            fps = field_data.pop('data')
            kwargs[name] = Field(fps, field_values=[field_data[str(arr)] for arr in
                                                    sorted(map(int, field_data.keys()))])
        return cls(**kwargs)

    @classmethod
    def from_hdf(cls, *args, **kwargs):
        """Alias for :func:`~exa.core.container.Container`."""
        return cls.load(*args, **kwargs)

    def _rel(self, copy=False):
        """
        Get descriptive kwargs of the container (e.g. name, description, meta).
        """
        rel = {}
        for key, obj in vars(self).items():
            if (not isinstance(obj, (pd.Series, pd.DataFrame,
                                     pd.SparseSeries, SparseDataFrame))
                and not key.startswith('_')):
                if copy and 'id' not in key:
                    rel[key] = deepcopy(obj)
                else:
                    rel[key] = obj
        return rel

    def _data(self, copy=False):
        """
        Get data kwargs of the container (i.e. dataframe and series objects).
        """
        data = {}
        for key, obj in vars(self).items():
            if isinstance(obj, (pd.Series, pd.DataFrame,
                          pd.SparseSeries, SparseDataFrame)):
                if copy:
                    data[key] = obj.copy(deep=True)
                else:
                    data[key] = obj
        return data

    def __delitem__(self, key):
        if key in vars(self):
            del self.__dict__[key]

    def __sizeof__(self):
        """Note that this function must return a Python integer."""
        return int(self.info()['size'].sum())

    def __getitem__(self, key):
        if isinstance(key, str):
            return getattr(self, key)
        elif isinstance(key, (int, slice, list)) and self._cardinal is None:
            return self.slice_naive(key)
        elif isinstance(key, (int, slice, list)) and self._cardinal is not None:
            return self.slice_cardinal(key)
        raise KeyError()

    def __init__(self, name=None, description=None, meta=None, **kwargs):
        self.log.info('adding {} attrs'.format(len(kwargs)))
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.name = name
        self.description = description
        self.meta = meta
