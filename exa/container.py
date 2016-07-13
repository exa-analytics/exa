# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
Container
########################
The :class:`~exa.container.BaseContainer` class is the primary object for
data processing, analysis, and visualization. Containers are composed of
n-dimensional spreadsheet-like (see :mod:`~exa.numerical`) objects whose
columns contain data for 2D and 3D visualization.

The :class:`~exa.container.BaseContainer` is akin to a :class:`~pandas.HDFStore`
in that it is a container for dataframes (and saves to an HDF5 file). It is
different in that it provides visualization tools access to the data contained
via automated JSON strings, transferrable between languages.

See Also:
    :mod:`~exa.relational.container` and :mod:`~exa.widget`
'''
import os
import numpy as np
import pandas as pd
import networkx as nx
from sys import getsizeof
from copy import deepcopy
from traitlets import Bool
from exa import mpl
from exa._config import config
from exa.widget import ContainerWidget
from exa.numerical import Series, DataFrame, SparseSeries, SparseDataFrame, Field
from exa.relational import ContainerFile, scoped_session
from exa.utility import convert_bytes


# These constants are used for data network visualization
edge_colors = mpl.sns.color_palette('viridis', 2)
edge_types = ['index-index', 'index-column']
edge_color_map = dict(zip(edge_types, edge_colors))
r_edge_color_map = {v: k for k, v in edge_color_map.items()}
node_colors = mpl.sns.color_palette('viridis', 7)
node_types = [Field, SparseSeries, DataFrame, SparseDataFrame, Series, pd.DataFrame, pd.Series]
node_color_map = list(zip(node_types, node_colors))
r_node_color_map = {v: '.'.join((k.__module__, k.__name__)) for k, v in node_color_map}


class Container:
    '''
    Container class responsible for all features related to data management.
    '''
    _widget_class = ContainerWidget
    _getter_prefix = 'compute'
    _cardinal_axis = None

    def copy(self, **kwargs):
        '''
        Create a copy of the current object.
        '''
        cls = self.__class__
        kws = self._rel(copy=True)
        dfs = self._data(copy=True)
        kws.update(dfs)             # We updates kws in this order because we
        kws.update(kwargs)          # want to respect the user's kwargs.
        return cls(**kws)

    def concat(self, *args, **kwargs):
        '''
        Concatenate any number of container objects with the current object into
        a single container object.

        See Also:
            For argument description, see :func:`~exa.container.concat`.
        '''
        raise NotImplementedError()

    def slice_by_indices(self, key):
        '''
        Slice the container by series or dataframe index.

        Warning:
            Does not make a copy, must call the **.copy()** method on the
            resulting container if a copy is needed.
        '''
        if isinstance(key, (int, np.int32, np.int64)):
            key = [key]
        kwargs = {}
        for name, data in self._data().items():
            k = name[1:] if name.startswith('_') else name
            if isinstance(data, Field):
                d = data.ix[key]
                i = d.index.values
                v = data.field_values[i]
                kwargs[k] = data.__class__(d, field_values=v)
            else:
                kwargs[k] = data.ix[key]
        return self.__class__(name=self.name, description=self.description,
                              meta=self.meta, **kwargs)

    def slice_by_cardinal_axis(self, key):
        '''
        Slice the container according to its cardinal axis.

        See Also:
            Note the warning in :func:`~exa.container.Container.slice_by_indices`.
        '''
        if isinstance(key, (int, np.int32, np.int64)):
            key = [key]
        elif isinstance(key, slice):
            key = self[self._cardinal_axis].index.values[key]
        kwargs = {}
        for name, data in self._data().items():
            k = name[1:] if name.startswith('_') else name
            if self._cardinal_axis in data.index.names:
                kwargs[k] = data.ix[key]
            elif self._cardinal_axis in data.columns:
                kwargs[k] = data[data[self._cardinal_axis].isin(key)]
            else:
                kwargs[k] = data
        return self.__class__(name=self.name, description=self.description,
                              meta=self.meta, **kwargs)

    def info(self):
        '''
        Display information about the container's objects.

        Note:
            Sizes are reported in bytes.
        '''
        names = []
        types = []
        sizes = []
        names.append('WIDGET')
        types.append('-')
        s = 0
        if self._widget is not None:
            for obj in self._widget._trait_values.values():
                s += getsizeof(obj)
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

    def memory_usage(self):
        '''
        Estimate the memory usage of the entire container.
        '''
        n = getsizeof(self)
        return ' '.join((str(s) for s in convert_bytes(n)))

    def network(self):
        '''
        Display information about the container's object relationships.

        Note:
            Due to quirks of plotting, rerunning this command until a "pleasing"
            visual is generated may be useful.
        '''
        def get_color(obj):
            '''Gets the color of a node based on the node's data type.'''
            for k, v in node_color_map:
                if isinstance(obj, k):
                    return v
            return 'gray'

        def legend(items, mapper, title, loc, ax):
            '''Legend creation helper'''
            proxies = []
            descriptions = []
            for k in set(items):
                if title == 'Data Type':
                    line = mpl.sns.mpl.lines.Line2D([], [], linestyle='none', color=k, marker='o')
                else:
                    line = mpl.sns.mpl.lines.Line2D([], [], linestyle='-', color=k)
                proxies.append(line)
                descriptions.append(mapper[k])
            leg = ax.legend(proxies, descriptions, title=title, loc=loc, frameon=True)
            leg_frame = leg.get_frame()
            leg_frame.set_facecolor('white')
            leg_frame.set_edgecolor('black')
            return leg, ax

        inf = self.info()
        inf = inf[inf['type'] != '-']
        nodes = inf.index.values
        node_sizes = inf['size']
        node_sizes *= 13000/node_sizes.max()
        node_sizes += 2000
        node_colors = {}
        node_types = {}
        edges = {}
        items = self._data().items()
        for k0, v0 in items:
            n0 = k0[1:] if k0.startswith('_') else k0
            node_colors[n0] = get_color(v0)
            node_types[n0] = '.'.join((v0.__class__.__module__, v0.__class__.__name__))
            for k1, v1 in items:
                if v0 is v1:
                    continue
                n1 = k1[1:] if k1.startswith('_') else k1
                for name in v0.index.names:
                    if name is None:
                        continue
                    if name in v1.index.names:
                        edges[(n0, n1)] = edge_color_map['index-index']
                        edges[(n1, n0)] = edge_color_map['index-index']
                    for col in v1.columns:
                        if name in col and '_' not in col:    # Catches things like index name == 'index', column name == 'index0'
                            edges[(n0, n1)] = edge_color_map['index-column']
                            edges[(n1, n0)] = edge_color_map['index-column']
        g = nx.Graph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges.keys())
        node_size = [node_sizes[k] for k in g.nodes()]
        node_color = [node_colors[k] for k in g.nodes()]
        edge_color = [edges[k] for k in g.edges()]
        labels = {k: ' {}\n({})'.format(k, node_types[k]) for k in g.nodes()}
        fig, ax = mpl.sns.plt.subplots(1, figsize=(14, 9), dpi=300)
        ax.axis('off')
        pos = nx.spring_layout(g)
        f0 = nx.draw_networkx_nodes(g, pos=pos, ax=ax, alpha=0.7, node_size=node_size,
                                    node_color=node_color)
        f1 = nx.draw_networkx_labels(g, pos=pos, labels=labels, font_size=17,
                                     font_weight='bold', ax=ax)
        f2 = nx.draw_networkx_edges(g, pos=pos, edge_color=edge_color, width=2, ax=ax)
        l1, ax = legend(edge_color, r_edge_color_map, 'Connection', (1, 0), ax)
        l2, ax = legend(node_color, r_node_color_map, 'Data Type', (1, 0.3), ax)
        fig.gca().add_artist(l1)

    def save(self, path):
        '''
        Save the container as an HDF5 archive.

        Args:
            path (str): Path where to save the container
        '''
        # First save the file record
        with scoped_session() as session:
            cfile = ContainerFile(name=self.name, description=self.description,
                                  size=getsizeof(self))
            session.add(cfile)
        # Second save the data
        if path is None:
            path = self.hexuid + '.hdf5'
        elif os.path.isdir(path):
            path += os.sep + self.hexuid + '.hdf5'
        elif not (path.endswith('.hdf5') or path.endswith('.hdf')):
            raise ValueError('File path must have a ".hdf5" or ".hdf" extension.')
        with pd.HDFStore(path, 'w') as store:
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
                elif isinstance(data, SparseSeries):
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

    @classmethod
    def load(cls, pkid_or_path=None):
        '''
        Load a container object from a persistent location or file path.

        Args:
            pkid_or_path: Integer pkid corresponding to the container table or file path

        Returns:
            container: The saved container object
        '''
        path = pkid_or_path
        if not os.path.isfile(pkid_or_path):
            raise NotImplementedError('Cannot lookup automatic path yet..')
        kwargs = {}
        with pd.HDFStore(path) as store:
            for key in store.keys():
                if 'kwargs' in key:
                    kwargs.update(store.get_storer(key).attrs.metadata)
                else:
                    name = str(key[1:])
                    kwargs[name] = store[key]
        # Process any fields
        n = [int(key.split('_')[0].replace('FIELD', '')) for key in kwargs.keys() if 'FIELD' in key]
        if len(n) != 0:
            n = max(n)
            to_del = []
            for i in range(n + 1):
                search = 'FIELD' + str(i)
                names = [key for key in kwargs.keys() if search in key]
                to_del += names
                arg = names[0].replace(search + '_', '').split('/')[0]
                field_values = [kwargs[key] for key in names if 'values' in key]
                dkey = None
                for name in names:
                    if 'data' in name:
                        dkey = name
                field_data = kwargs[dkey]
                kwargs[arg] = field_data
                kwargs[arg + '_values'] = field_values
            for name in to_del:
                del kwargs[name]
        return cls(**kwargs)

    def _rel(self, copy=False):
        '''
        Get all (propagatable) relational and metadata data of the container (
        primary keys are not propagatable).
        '''
        rel = {}
        for key, obj in self.__dict__.items():
            if not isinstance(obj, (pd.Series, pd.DataFrame)) and not key.startswith('_'):
                if copy and 'id' not in key:
                    rel[key] = deepcopy(obj)
                else:
                    rel[key] = obj
        return rel

    def _data(self, copy=False):
        '''
        Get all data associated with the container as key value pairs.
        '''
        data = {}
        for key, obj in self.__dict__.items():
            if isinstance(obj, (pd.Series, pd.DataFrame, pd.SparseSeries, pd.SparseDataFrame)):
                if copy:
                    data[key] = obj.copy()
                else:
                    data[key] = obj
        return data

    def _custom_traits(self):
        '''
        Placeholder for custom container traits (e.g. traits that are comprised
        of data present in multiple data objects).
        '''
        return {}

    def _update_traits(self):
        '''
        Jupyter notebook widgets require data to be available within a
        :class:`~exa.widget.Widget` object. This allows notebook extensions
        (nbextensions - written in JavaScript) to access backend (Python) data
        via `ipywidgets`_.

        .. _ipywidgets: https://ipywidgets.readthedocs.io/en/latest/
        '''
        if self._widget is not None:    # If a corresponding widget exists, build traits
            traits = self._custom_traits()
            if len(self._data()) == 0:
                traits['test'] = Bool(True).tag(sync=True)
            else:
                traits['test'] = Bool(False).tag(sync=True)
                traits.update(self._custom_traits())
                for n, obj in self._data().items():
                    if (hasattr(obj, '_traits') or isinstance(obj, (Series, SparseSeries))) and len(obj) > 0:
                        traits.update(obj._update_traits())
            self._widget.add_traits(**traits)    # Adding traits to the widget makes
            self._traits_need_update = False     # them accesible from nbextensions (JavaScript).

    def __delitem__(self, key):
        if key in self.__dict__:
            del self.__dict__[key]

    def __sizeof__(self):
        '''Note that this function must return a Python integer.'''
        return int(self.info()['size'].sum())

    def __getitem__(self, key):
        if isinstance(key, str):
            return getattr(self, key)
        elif isinstance(key, (int, slice, list)) and self._cardinal_axis is None:
            return self.slice_by_indices(key)
        elif isinstance(key, (int, slice, list)) and self._cardinal_axis is not None:
            return self.slice_by_cardinal_axis(key)
        raise KeyError()

    def __init__(self, name=None, description=None, meta={}, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.name = name
        self.description = description
        self.meta = meta
        self._traits_need_update = True
        # This will create an instance of the widget class (if present)
        self._widget = self._widget_class(self) if config['dynamic']['notebook'] == 'true' else None

    def _repr_html_(self):
        if self._widget is not None and self._traits_need_update:
            self._update_traits()
        return self._widget._repr_html_()


class TypedMeta(type):
    '''
    This metaclass creates statically typed class attributes using the property
    framework.

    .. code-block:: Python

        class TestMeta(TypedMeta):
            attr1 = (int, float)
            attr2 = DataFrame

        class TestClass(metaclass=TestMeta):
            def __init__(self, attr1, attr2):
                self.attr1 = attr1
                self.attr2 = attr2

    The above code dynamically creates code that looks like the following:

    .. code-block:: Python

        class TestClass:
            @property
            def attr1(self):
                return self._attr1

            @attr1.setter
            def attr1(self, obj):
                if not isinstance(obj, (int, float)):
                    raise TypeError('attr1 must be int')
                self._attr1 = obj

            @attr1.deleter
            def attr1(self):
                del self._attr1

            @property
            def attr2(self):
                return self._attr2

            @attr2.setter
            def attr2(self, obj):
                if not isinstance(obj, DataFrame):
                    raise TypeError('attr2 must be DataFrame')
                self._attr2 = obj

            @attr2.deleter
            def attr2(self):
                del self._attr2

            def __init__(self, attr1, attr2):
                self.attr1 = attr1
                self.attr2 = attr2
    '''
    @staticmethod
    def create_property(name, ptype):
        '''
        Creates a custom property with a getter that performs computing
        functionality (if available) and raise a type error if setting
        with the wrong type.

        Note:
            By default, the setter attempts to convert the object to the
            correct type; a type error is raised if this fails.
        '''
        pname = '_' + name    # This will be where the data is store (e.g. self._name)
        def getter(self):
            '''
            This is the default property "getter" for container data objects.
            If the property value is None, this function will check for a
            convenience method with the signature, self.compute_name() and call
            it prior to returning the property value.
            '''
            if not hasattr(self, pname) and hasattr(self, '{}{}'.format(self._getter_prefix, pname)):
                self['{}{}'.format(self._getter_prefix, pname)]()
            if not hasattr(self, pname):
                raise AttributeError('Please compute or set {} first.'.format(name))
            return getattr(self, pname)

        def setter(self, obj):
            '''
            This is the default property "setter" for container data objects.
            Prior to setting a property value, this function checks that the
            object's type is correct.
            '''
            if not isinstance(obj, ptype):
                try:
                    obj = ptype(obj)
                except Exception:
                    raise TypeError('Must be able to convert object {0} to {1} (or must be of type {1})'.format(name, ptype))
            setattr(self, pname, obj)

        def deleter(self):
            '''Deletes the property's value.'''
            del self[pname]

        return property(getter, setter, deleter)

    def __new__(metacls, name, bases, clsdict):
        '''
        Modification of the class definition occurs here; we iterate over all
        statically typed attributes and attach their property (see
        :func:`~exa.container.TypedMeta.create_property`) definition, returning
        the new class definition.
        '''
        for k, v in metacls.__dict__.items():
            if isinstance(v, type) and k[0] != '_':
                clsdict[k] = metacls.create_property(k, v)
        return super().__new__(metacls, name, bases, clsdict)
