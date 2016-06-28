# -*- coding: utf-8 -*-
'''
Base Container
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
from collections import OrderedDict
from traitlets import Bool
from collections import defaultdict
from sqlalchemy.orm.attributes import InstrumentedAttribute
from exa import global_config, mpl
from exa.widget import ContainerWidget
from exa.numerical import NDBase, DataFrame, Field, SparseDataFrame, Series
from exa.utility import del_keys


class TypedMeta(type):
    '''
    A metaclass for automatically generating properties for statically typed
    class attributes. Useage is the following:

    .. code-block:: Python

        class TestMeta(TypedMeta):
            attr1 = int
            attr2 = DataFrame

        class TestClass(metaclass=TestMeta):
            def __init__(self, attr1, attr2):
                self.attr1 = attr1
                self.attr2 = attr2

    Under the covers, this class creates code that looks like the following:

    .. code-block:: Python

        class TestClass:
            @property
            def attr1(self):
                return self._attr1

            @attr1.setter
            def attr1(self, obj):
                if not isinstance(obj, int):
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
        pname = '_' + name
        def getter(self):
            if not hasattr(self, pname) and hasattr(self, '{}{}'.format(self._getter_prefix, pname)):
                self['{}{}'.format(self._getter_prefix, pname)]()
            if not hasattr(self, pname):
                raise AttributeError('Please compute or set {} first.'.format(name))
            return getattr(self, pname)
        def setter(self, obj):
            if not isinstance(obj, ptype):
                try:
                    obj = ptype(obj)
                except:
                    raise TypeError('Object {0} must instance of {1}'.format(name, ptype))
            setattr(self, pname, obj)
        def deleter(self):
            del self[pname]
        return property(getter, setter, deleter)

    def __new__(metacls, name, bases, clsdict):
        '''
        Here we control the creation of the class definition. For every statically
        typed attributed (see source code or docstring)
        '''
        for k, v in metacls.__dict__.items():
            if isinstance(v, type) and k[0] != '_':
                clsdict[k] = metacls.create_property(k, v)
        return super().__new__(metacls, name, bases, clsdict)


class BaseContainer:
    '''
    Base container class responsible for all features related to data
    management; relational features are in :class:`~exa.relational.container.Container`.

    Note:
        Due to the requirements of mixing metaclasses, a metaclass is
        created in :mod:`~exa.relational.container` and assigned to the
        "master" container object, :class:`~exa.relational.container.Container`.
    '''
    _widget_class = ContainerWidget
    _getter_prefix = 'compute'

    def add_data(self, data):
        pass

    def append_field(self, data, values=None):
        pass

    def save(self, path=None):
        '''
        Save the current working container to an HDF5 file.

        .. code-block:: Python

            container.save()  # Save to default location
            container.save('my/location/file.name')  # Save HDF5 file at given path
        '''
        self._save_record()
        self._save_data(path)

    def copy(self, **kwargs):
        '''
        Create a copy of the current object.
        '''
        cls = self.__class__
        kws = del_keys(self._kw_dict(copy=True))
        dfs = self._data(copy=True)
        kws.update(kwargs)
        kws.update(dfs)
        return cls(**kws)

    def concat(self, *args, **kwargs):
        '''
        Concatenate any number of container objects with the current object into
        a single container object.

        See Also:
            For argument description, see :func:`~exa.container.concat`.
        '''
        raise NotImplementedError()

    def info(self):
        '''
        Print human readable information about the container.
        '''
        sizes = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB']
        mem_usage = self.memory_usage().sum()
        n = np.rint(len(str(mem_usage))/4).astype(int)
        print('size ({0}):'.format(sizes[n]),  mem_usage/(1024**n))
        print('object count:', len(self._data().keys()))

    def memory_usage(self):
        '''
        Get the memory usage (in bytes) of the container object.
        '''
        data_mem = 0      # Memory due to data objects
        rel_mem = 0       # Memory due to metadata/relational attributes
        widget_mem = 0    # Memory due to widget data
        for obj in self._data().values():
            data_mem += getsizeof(obj)
        for obj in self._rel().values():
            rel_mem += getsizeof(obj)
        if self._widget is not None:
            for obj in self._widget._trait_values.values():
                widget_mem += getsizeof(obj)
        mem = pd.Series({'data': data_mem, 'base': rel_mem, 'widget': widget_mem})
        mem.name = 'bytes'
        return mem



#    def data_network(self):
#        '''
#        Visualize the dataframe/series relationships and relative sizes.
#
#        A network graph representation of the current container is drawn. Nodes
#        are data objects (dataframes or series) attached to the current
#        container. Their relative size is proportional to the amount of data
#        they contain. The node color corresponds to the number of relationships
#        a given node has with other nodes. The edge color correspond to the
#        type of connection a given node has with another node (index to index,
#        index to column, or index to other).
#
#        If performed on an empty or test container, this function will display
#        the enforced data objects and their connectivity. No information about
#        the type of connectivity
#        '''
#        edges = []
#        nodes = []
#        node_sizes = {}
#        edge_colors = {}
#        edge_color_map = sns.color_palette('viridis', 4)
#        data = self._df_types.items()
#        if not self._test:
#            data = self._numerical_dict().items()
#        for i, (name0, df0) in enumerate(data):
#            n0 = name0[1:] if name0.startswith('_') else name0
#            indices0, columns0 = get_indices_columns(df0)
#            for name1, df1 in data:
#                if df0 is df1:
#                    continue
#                n1 = name1[1:] if name1.startswith('_') else name1
#                indices1, columns1 = get_indices_columns(df1)
#                key = (n0, n1)
#                if any([index in indices1 for index in indices0]):
#                    edges.append(key)
#                    edge_colors[key] = edge_color_map[0]
#                elif any([index in columns1 for index in indices0]):
#                    edges.append(key)
#                    edge_colors[key] = edge_color_map[1]
#                elif any([index in columns0 for index in indices1]):
#                    edges.append(key)
#                    edge_colors[key] = edge_color_map[1]
#                #elif (hasattr(df0, '_categories') and hasattr(df1, '_categories')):
#                #    if (np.any([index in  for index in df0._groupbys]) or
#                #        np.any([index in columns0 for index in df1._groupbys])):
#                #        edges.append(key)
#                #        edge_colors[key] = edge_color_map[2]
#            nodes.append(n0)
#            node_sizes[n0] = df0.size if isinstance(df0.size, np.int64) or isinstance(df0.size, int) else 0
#            if hasattr(df0, 'field_values'):
#                for i, field in enumerate(df0.field_values):
#                    key = (n0, 'field_values[*]'.format(i))
#                    if key[1] not in nodes:
#                        nodes.append(key[1])
#                        node_sizes[key[1]] = field.size if isinstance(field.size, np.int64) or isinstance(field.size, int) else 0
#                    else:
#                        node_sizes[key[1]] += field.size if isinstance(field.size, np.int64) or isinstance(field.size, int) else 0
#                    edges.append(key)
#                    edge_colors[key] = edge_color_map[3]
#                    key = (key[1], key[0])
#                    edges.append(key)
#                    edge_colors[key] = edge_color_map[2]
#        g = nx.Graph()
#        g.add_nodes_from(nodes)
#        g.add_edges_from(edges)
#        fig, ax = sns.plt.subplots(1, figsize=(13, 8), dpi=600)
#        ax.axis('off')
#        degree_values = np.unique(list(g.degree().values()))
#        enum_map = {v: k for k, v in enumerate(degree_values)}
#        node_colors = sns.color_palette('viridis', len(degree_values))
#        node_color = [node_colors[enum_map[g.degree()[node]]] for node in g.nodes()]
#        edge_color = [edge_colors[edge] for edge in g.edges()]
#        node_size = 3000
#        if not self._test:
#            node_size = np.log(np.array([node_sizes[node] for node in g.nodes()]))
#            node_size *= 13000 / node_size.max()
#            node_size += 2000
#        pos = nx.spring_layout(g)
#        f0 = nx.draw_networkx_nodes(g, pos=pos, node_size=node_size,
#                                    node_color=node_color, alpha=0.8, ax=ax)
#        f1 = nx.draw_networkx_labels(g, pos=pos, labels={k: k for k in g.nodes()},
#                                     font_size=15, font_weight='bold', ax=ax)
#        f2 = nx.draw_networkx_edges(g, pos=pos, edge_color=edge_color, width=2, ax=ax)
#        axbox = ax.get_position()
#        # Node color legend
#        degree_map = {v: k for k, v in enum_map.items()}
#        proxies = []
#        descriptions = []
#        for i, v in enumerate(degree_values):
#            line = sns.mpl.lines.Line2D([], [], linestyle='none', color=node_colors[enum_map[v]], marker='o')
#            proxies.append(line)
#            descriptions.append(degree_map[i])
#        r_legend = ax.legend(proxies, descriptions, title='Connections', loc=(1, 0), frameon=True)
#        r_frame = r_legend.get_frame()
#        r_frame.set_facecolor('white')
#        r_frame.set_edgecolor('black')
#        # Edge color legend
#        rel_types = {0: 'index - index', 1: 'index - column', 2: 'column - column',
#                     3: 'index - other'}
#        proxies = []
#        descriptions = []
#        for i, c in enumerate(edge_color_map):
#            line = sns.mpl.lines.Line2D([], [], linestyle='-', color=c)
#            proxies.append(line)
#            descriptions.append(rel_types[i])
#        e_legend = ax.legend(proxies, descriptions, title='Relationship Type', loc=(1, 0.7), frameon=True)
#        e_frame = r_legend.get_frame()
#        e_frame.set_facecolor('white')
#        e_frame.set_edgecolor('black')
#        fig.gca().add_artist(r_legend)
#        return g

    @classmethod
    def from_hdf(cls, path):
        '''
        Load a container object from an HDF5 file.

        Args:
            path (str): Full file path to the container hdf5 file.
        '''
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

    @classmethod
    def load(cls, pkid_or_path=None):
        '''
        Load a container object from a persistent location or file path.

        Args:
            pkid_or_path: Integer pkid corresponding to the container table or file path

        Returns:
            container: The saved container object
        '''
        if isinstance(pkid_or_path, int):
            raise NotImplementedError('Support for persistent storage coming soon...')
        elif isinstance(pkid_or_path, str):
            return cls.from_hdf(pkid_or_path)
        else:
            raise TypeError('The argument should be int or str, not {}.'.format(type(pkid_or_path)))

    def _save_data(self, path=None, how='hdf'):
        '''
        Save the dataframe (and related series) data to an `HDF5`_ file. This
        file contains all of the dataframe data as well as the descriptive
        relational data attached to the current container.
        '''
        kwargs = self._kw_dict()
        kwargs['meta'] = str(self.meta) if self.meta else None
        kwargs = del_keys(kwargs)
        if how == 'hdf':
            self._save_hdf(path, kwargs)
        else:
            raise NotImplementedError('Currently only hdf5 is supported')

    def _save_hdf(self, path, kwargs):
        '''
        Save the container to an HDF5 file. Returns the saved file path upon
        completion.
        '''
        # Check the path
        if path is None:
            path = self.hexuid + '.hdf5'
        elif os.path.isdir(path):
            path += os.sep + self.hexuid + '.hdf5'
        elif not (path.endswith('.hdf5') or path.endswith('.hdf')):
            raise ValueError('File path must have a ".hdf5" or ".hdf" extension.')
        with pd.HDFStore(path) as store:
            store['kwargs'] = pd.Series()
            store.get_storer('kwargs').attrs.metadata = kwargs
            fc = 0
            for name, df in self._data().items():
                name = name[1:] if name.startswith('_') else name
                if isinstance(df, Field):
                    df._revert_categories()
                    fname = 'FIELD{}_'.format(fc) + name + '/'
                    store[fname + 'data'] = pd.DataFrame(df)
                    for i, field in enumerate(df.field_values):
                        ffname = fname + 'values' + str(i)
                        if isinstance(field, pd.Series):
                            store[ffname] = pd.Series(field)
                        else:
                            store[ffname] = pd.DataFrame(field)
                    df._set_categories()
                    fc += 1
                elif isinstance(df, Series):
                    store[name] = pd.Series(df)
                elif isinstance(df, SparseDataFrame):
                    store[name] = pd.SparseDataFrame(df)
                elif isinstance(df, DataFrame):
                    df._revert_categories()
                    store[name] = pd.DataFrame(df)
                    df._set_categories()
                else:
                    store[name] = df
        return path

    def _rel(self, copy=False):
        '''
        Get all relational and metadata data of the container.
        '''
        rel = {}
        for key, obj in self.__dict__.items():
            if not isinstance(obj, (pd.Series, pd.DataFrame)):
                if copy:
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
            if isinstance(obj, (pd.Series, pd.DataFrame)):
                if copy:
                    data[key] = obj.copy()
                else:
                    data[key] = obj
        return data

    def _trait_data(self):
        '''
        Get all data that contains traits.
        '''
        active = {}
        for key, obj in self._data().items():
            if hasattr(obj, '_traits'):
                if len(obj._traits) > 0 and len(obj) > 0:
                    active[key] = obj
        return active

    def _update_custom_traits(self):
        '''
        For generating custom traits dependent on multiple data objects.

        See Also:
            :func:`~exa.numerical.NDBase._update_custom_traits`
        '''
        return {}

    def _update_traits(self):
        '''
        Main entry point for updating all traits of the current container. This
        function will make calls to every data object that contains traits.

        See Also:
            :func:`~exa.numerical.NDBase._update_traits`
        '''
        if self._widget is not None:
            traits = {}
            if self._test:
                traits['test'] = Bool(True).tag(sync=True)
            else:
                traits['test'] = Bool(False).tag(sync=True)
                traits.update(self._custom_container_traits())
                has_traits = self._trait_data()
                for obj in has_traits.values():
                    traits.update(obj._update_traits())
            self._widget.add_traits(**traits)
            self._traits_need_update = False

    def _slice_with_int_or_string(self, key):
        '''
        Slices the current container selecting data that matches the key (either on _groupbys or
        by row index).
        '''
        cls = self.__class__
        kws = del_keys(self._kw_dict(copy=True))
        for name, df in self._data(copy=True).items():
            dfcls = df.__class__
            if hasattr(df, '_groupbys'):
                if len(df._groupbys) > 0:
                    grps = df.groupby(df._groupbys)
                    selector = sorted(grps.groups.keys())[key]
                    kws[name] = dfcls(grps.get_group(selector))
            if name not in kws:
                selector = None
                if isinstance(df, pd.SparseDataFrame) or isinstance(df, pd.SparseSeries):
                    kws[name] = df
                elif key > len(df.index):
                    kws[name] = df
                else:
                    selector = df.index[key]
                    kws[name] = dfcls(df.ix[[selector], :])
        return cls(**kws)

    def _slice_with_list_or_tuple(self, keys):
        '''
        Slices the current container selecting data that matches the keys (either on _groupbys or
        by row index).
        '''
        cls = self.__class__
        kws = del_keys(self._kw_dict(copy=True))
        for name, df in self._data(copy=True).items():
            dfcls = df.__class__
            if hasattr(df, '_groupbys'):
                if len(df._groupbys) > 0:
                    grps = df.groupby(df._groupbys)
                    srtd = sorted(grps.groups.keys())
                    selector = [srtd[key] for key in keys]
                    kws[name] = dfcls(pd.concat([grps.get_group(key) for key in selector]))
            if name not in kws:
                if isinstance(df, pd.SparseDataFrame) or isinstance(df, pd.SparseSeries):
                    kws[name] = df
                elif max(keys) > len(df.index):
                    kws[name] = df
                else:
                    selector = [df.index[key] for key in keys]
                    kws[name] = dfcls(df.ix[selector, :])
        return cls(**kws)

    def _reconstruct_field(self, name, data, values):
        '''
        Enforces the field dataframe type.
        '''
        if data is None and values is None:
            return None
        elif hasattr(data, 'field_values'):
            if hasattr(data, '_set_categories'):
                data._set_categories()
            return data
        elif len(data) != len(values):
            raise TypeError('Length of Field ({}) data and values don\'t match.'.format(name))
        else:
            cls = self._df_types[name]
            for i in range(len(values)):
                if not isinstance(values[i], DataFrame) and isinstance(values[i], pd.DataFrame):
                    values[i] = DataFrame(values[i])
                else:
                    values[i] = Series(values[i])
            df = cls(values, data)
            if hasattr(df, '_set_categories'):
                df._set_categories()
            return df

    def _slice_with_slice(self, slce):
        '''
        Slices the current container selecting data that matches the range given
        by the slice object.
        '''
        cls = self.__class__
        kws = del_keys(self._kw_dict(copy=True))
        for name, df in self._data(copy=True).items():
            dfcls = df.__class__
            if hasattr(df, '_groupbys'):
                if len(df._groupbys) > 0:
                    grps = df.groupby(df._groupbys)
                    srtd = sorted(grps.groups.keys())
                    kws[name] = dfcls(pd.concat([grps.get_group(key) for key in srtd[slce]]))
            if name not in kws:
                if isinstance(df, pd.SparseDataFrame) or isinstance(df, pd.SparseSeries):
                    kws[name] = df
                elif slce == slice(None):
                    kws[name] = df
                else:
                    keys = df.index.values[slce]
                    kws[name] = dfcls(df.iloc[keys, :])
        return cls(**kws)

    def __getitem__(self, key):
        '''
        Containers can be sliced in a number of different ways and the slicing
        of the data values depends on the characteristics of the individual
        data objects (i.e. presence of _groupbys).
        '''
        if isinstance(key, int):
            return self._slice_with_int_or_string(key)
        elif isinstance(key, str) and not hasattr(self, key):
            return self._slice_with_int_or_string(key)
        elif isinstance(key, list) or isinstance(key, tuple):
            return self._slice_with_list_or_tuple(key)
        elif isinstance(key, slice):
            return self._slice_with_slice(key)
        elif hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError('No selection method for key {} of type {}'.format(key, type(key)))

    def __delitem__(self, key):
        del self[key]

    def __init__(self, name=None, description=None, meta=None, **kwargs):
        self.name = name
        self.description = description
        self.meta = meta
        #print(kwargs)
        #self._df_types = {}
        #for key, value in kwargs.items():
        #    print(self)
        #    print(key)
        #    print(value)
        #    setattr(self, key, value)
        #    self._df_types[key] = value
        self._test = False
        self._traits_need_update = True
        self._widget = self._widget_class(self) if global_config['notebook'] else None
        if meta is None and len(kwargs) == 0 and len(self._data()) == 0:
            self._test = True
            self.name = 'TestContainer'
            self._update_traits()

    def _repr_html_(self):
        if self._widget:
            if self._traits_need_update:
                self._update_traits()
            return self._widget._repr_html_()
        return None


def slice_by_int():
    pass

#def concat(*containers, axis=0, join='outer', ingore_index=False):
#    '''
#    Concatenate any number of container objects into a single container object.
#
#    Args:
#        containers: A sequence of container or container like objects
#        axis (int): Axis along which to concatenate (0: "hstack", 1: "vstack")
#        join (str): How to handle indices on other axis (full outer join: "outer", inner join: "inner")
#        ignore_index (bool): See warning below!
#
#    Returns:
#        container: Concatenated container object
#
#    Note:
#        The concatenated object will have a new unique id, primary, key, and
#        its metadata will contain references to the original conatiners.
#
#    Warning:
#        The ignore_index option is primarily for internal use. If set to true,
#        may cause the resulting concatenated container object to not have
#        meaningful indices or columns. Use with care.
#    '''
#    # In the simplest case, all of the containers have unique indices and should
#    # simply be sorted and then their dataframe data appended
#    cls = containers[0].__class__
#    if not np.all([cls == container.__class__ for container in containers]):
#        raise TypeError('Can only concatenate containers of the same type!')
#    # Get the master list of dataframes and record pkids
#    df_classes = {}
#    meta = {'concat_pkid': []}
#    for container in containers:
#        meta['concat_pkid'].append(container.pkid)
#        for key, value in container._numerical_dict().items():
#            name = key[1:] if key.startswith('_') else key
#            df_classes[name] = value.__class__
#    # For each dataframe, concatentate first by groupbys then by index
#    new_dfs = {}
#    for name, cls in df_classes.items():
#        dflist = [container[name] for container in containers]
#        dftypes = [type(df) for df in dflist]
#        df_type = dftypes[0]
#        df0 = dflist[0]
#        if np.any([dftype is not df_type for dftype in dftypes]):
#            raise TypeError('Cannot concantenate dataframes ({}) with different types!'.format(name))
#        if isinstance(df0, exa.numerical.Field):
#            print('FIELD')
#            news_dfs[name] = _concat_fields(dflist, cls, axis=axis, join=join)
#        elif isinstance(df0, exa.numerical.Series):
#            print('SERIES')
#            new_dfs[name] = _concat_series(dflist, cls)
#        elif isinstance(df0, exa.numerical.SparseDataFrame):
#
#            pass
#        elif isinstance(df0, exa.numerical.DataFrame):
#            pass
#        else:
#            pass
#            #new_dfs[name] = _concat_reindex(dflist, cls)
#    print(new_dfs.keys())
#    kwargs.update(new_dfs)
#    if 'meta' in kwargs:
#        kwargs['meta'].update(meta)
#    else:
#        kwargs['meta'] = meta
#    return kwargs
#
#def _concat_series(series, cls):
#    '''
#    '''
#    return cls(pd.concat(series))
#
#def _concat_dataframes(dataframes, cls):
#    '''
#    '''
#    grps = dataframes
#
#def _concat_fields(fields, cls, axis, join):
#    '''
#    '''
#    grps = fields[0]._groupbys
#    new_groupbys = {}
#    for name in grps:
#        if axis == 0:
#            new_groupbys[name] = pd.Series([i for i in range(len(fields)) for j in range(len(fields[i]))], dtype='category')
#        else:
#            new_groupbys[name] = pd.Series([i for i in range(len(fields[0]))], dtype='category')
#    field_values = [values for field in fields for values in field.field_values]
#    field_data = pd.concat([pd.DataFrame(field) for field in fields], axis=axis, join=join)
#    field_data.reset_index(inplace=True, drop=True)
#    for name in grps:
#        field_data[name] = new_groupbys[name]
#    return cls(field_values, field_data)
