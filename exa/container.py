# -*- coding: utf-8 -*-
'''
Base Container Class
===============================================
The :class:`~exa.container.BaseContainer` class is the primary controller for
data acquisition, management, and visualization. Containers are an object based
storage device used to process, analyze, (visualize), and organize
raw data stored as n-dimensional array objects (dataframes). Each Container
object is aware of the dataframes attached to it and provides standard
methods for common manipulations.

Data specific containers (such as the Universe class which is provided by the
atomic package, for example) are capable of advanced, automatic data analysis
tailored to the specific data content at hand.

See Also:
    :mod:`~exa.relational.container`
'''
import os
import numpy as np
import pandas as pd
import networkx as nx
from sys import getsizeof
from collections import OrderedDict
from traitlets import Bool
from collections import defaultdict
from sqlalchemy.orm.attributes import InstrumentedAttribute
from exa import _conf
from exa.widget import ContainerWidget
from exa.numerical import NDBase, DataFrame, Field, SparseDataFrame, Series
from exa.utility import del_keys


class BaseContainer:
    '''
    Foundational class for creating data containers. Inherited by
    :class:`~exa.relational.container.Container`. This class should not be
    inherited directly; rather :class:`~exa.relational.container.Container`
    should be inherited.
    '''
    _widget_class = ContainerWidget
    _df_types = OrderedDict()

    @property
    def field_values(self):
        '''
        Retrieve values of a specific field.

        Args:
            field (int): Field index (corresponding to the fields dataframe)

        Returns:
            data: Series or dataframe object containing field values
        '''
        if self._is('_field'):
            return self._field.field_values

    def append_numerical(self, frame_or_series):
        '''
        Attach a dataframe or series object to the current container.
        '''
        raise NotImplementedError()

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
        dfs = self._numerical_dict(copy=True)
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
        #return concat(self, *args, **kwargs)

    def info(self):
        '''
        Print human readable information about the container.
        '''
        n = getsizeof(self)
        sizes = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB']
        for size in sizes:
            s = str(n).split('.')
            if len(s) > 1:
                if len(s[0]) <= 3 and len(s[1]) > 3:
                    print('size ({0}): {1}'.format(size, n))
                    break
            elif len(s[0]) <= 3:
                print('size ({0}): {1}'.format(size, n))
                break
            n /= 1024

    def network(self):
        '''
        Visualize the dataframe relationships as a directed network graph. The
        direction points toward the dataframe that contains the index and
        away from the dataframe that contains the column. If no direction is
        given the match is on column axis or if both directions are given the match
        is on index axis.
        '''
        node_scheme = ['olivedrab', 'orange', 'firebrick']
        edge_scheme = ['olive', 'gold', 'darkred']
        nodes = {name: name[1:] if name.startswith('_') else name for name in self._numerical_dict().keys()}
        edges = []
        ncolors = defaultdict(int)
        ecolors = defaultdict(int)
        n = len(nodes)
        for internal_name, pn in nodes.items():
            df0 = self[internal_name]
            if isinstance(df0, pd.Series):
                continue
            for internal_other, po in nodes.items():
                df1 = self[internal_other]
                if df0 is df1 or isinstance(df1, pd.Series):
                    continue    # Skip if same
                index0 = df0.index.names
                index1 = df1.index.names
                columns0 = df0.columns
                columns1 = df1.columns
                if np.any([idx0 in index1 for idx0 in index0]):
                    edges.append((pn, po))
                    ncolors[pn] = max([ncolors[pn], 2])
                    ncolors[po] = max([ncolors[po], 2])
                    ecolors[(pn, po)] = max([ecolors[(pn, po)], 2])
                    ecolors[(po, pn)] = max([ecolors[(po, pn)], 2])
                elif np.any([idx0 in columns1 for idx0 in index0]) or np.any([idx0 + '0' in columns1 for idx0 in index0]):
                    edges.append((pn, po))
                    ncolors[pn] = max([ncolors[pn], 2])
                    ncolors[po] = max([ncolors[po], 1])
                    ecolors[(pn, po)] = max([ecolors[(pn, po)], 1])
                    ecolors[(po, pn)] = max([ecolors[(po, pn)], 1])
                elif np.any([idx1 in columns0 for idx1 in index1]) or np.any([idx1 + '0' in columns0 for idx1 in index1]):
                    edges.append((pn, po))
                    ncolors[pn] = max([ncolors[pn], 1])
                    ncolors[po] = max([ncolors[po], 2])
                    ecolors[(pn, po)] = max([ecolors[(pn, po)], 1])
                    ecolors[(po, pn)] = max([ecolors[(po, pn)], 1])
        g = nx.Graph()
        g.add_nodes_from(nodes.values())
        g.add_edges_from(edges)
        node_colors = [node_scheme[ncolors[node]] for node in g.nodes()]
        edge_colors = [edge_scheme[ecolors[edge]] for edge in g.edges()]
        nx.draw(g, with_labels=True, node_size=11000, font_size=15, node_color=node_colors, edge_colors=edge_colors)

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
            for name, df in self._numerical_dict().items():
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

    def _kw_dict(self, copy=False):
        '''
        Create kwargs from the available (non-null valued) relational arguments.

        Args:
            copy (bool): Return a copy of the attributes (default False)

        Returns:
            d (dict): Dictionary of non-null relational attributes.
        '''
        kws = {}
        for name, value in self.__class__.__dict__.items():
            if isinstance(value, InstrumentedAttribute):
                obj = self[name]
                if obj:
                    kws[name] = obj
        if copy:
            return kws.copy()
        return kws

    def _numerical_dict(self, copy=False, cls_criteria=[pd.Series, pd.DataFrame]):
        '''
        Get the attached :class:`~exa.numerical.Series` and
        :class:`~exa.numerical.DataFrame` objects.

        Args:
            copy (bool): Return an in memory copy
            cls_criteria (class): List of class objects to identify by (default :class:`~pandas.DataFrame`)

        Returns:
            dfs (dict): Name, dataframe key-value pairs
        '''
        dfs = {}
        for name, value in self.__dict__.items():
            if any((isinstance(value, klass) for klass in cls_criteria)):
                if copy:
                    cls = value.__class__
                    dfs[name] = cls(value.copy())
                else:
                    dfs[name] = value
        return dfs

    def _active_trait_dfs(self):
        '''
        Get only dataframes that have active traits.
        '''
        active = {}
        for name, value in self._numerical_dict().items():
            if hasattr(value, '_traits'):
                if len(value._traits) > 0:
                    active[name] = value
        return active

    def _df_bytes(self):
        '''
        Compute the size (in bytes) of all of the attached dataframes.
        '''
        total_bytes = 0
        for df in self._numerical_dict().values():
            total_bytes += np.sum(df.memory_usage())
        return total_bytes

    def _widget_bytes(self):
        '''
        Compute the size (in bytes) of all of the attached traits.
        '''
        total_bytes = 0
        if self._widget:
            for value in self._widget._trait_values.values():
                total_bytes += getsizeof(value)
        return total_bytes

    def _custom_container_traits(self):
        '''
        Used when a container is required to build specific trait objects.
        '''
        return {}

    def _update_traits(self):
        '''
        Update specific traits, given in the arguments.

        Args:
            traits (list): Names of traits to update
        '''
        if self._widget is not None:
            traits = {}
            if self._test:
                traits['test'] = Bool(True).tag(sync=True)
            else:
                traits['test'] = Bool(False).tag(sync=True)
                traits.update(self._custom_container_traits())
                has_traits = self._active_trait_dfs()
                for obj in has_traits.values():
                    traits.update(obj._get_traits())
            self._widget.add_traits(**traits)


    def _is(self, name):
        '''
        Check if the dataframe or series object exists.

        Args:
            name (str): String name of the series or dataframe object

        Returns:
            exists (bool): True if it exists
        '''
        if hasattr(self[name], 'shape'):
            return True
        return False

    def _enforce_df_type(self, name, value):
        '''
        Enforces dataframe type (or NoneType).
        '''
        if value is None:
            return None
        else:
            cls = self._df_types[name]
            if not isinstance(value, cls):
                df = cls(value)
                if hasattr(df, '_set_categories'):
                    df._set_categories()
                return df
            return value

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

    def _slice_with_int_or_string(self, key):
        '''
        Slices the current container selecting data that matches the key (either on _groupbys or
        by row index).
        '''
        cls = self.__class__
        kws = del_keys(self._kw_dict(copy=True))
        for name, df in self._numerical_dict(copy=True).items():
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
        for name, df in self._numerical_dict(copy=True).items():
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

    def _slice_with_slice(self, slce):
        '''
        Slices the current container selecting data that matches the range given
        by the slice object.
        '''
        cls = self.__class__
        kws = del_keys(self._kw_dict(copy=True))
        for name, df in self._numerical_dict(copy=True).items():
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
                    keys = df.index[slce]
                    kws[name] = dfcls(df.iloc[keys, :])
        return cls(**kws)

    def _other_bytes(self):
        return 0

    def __getitem__(self, key):
        '''
        The key can be an integer, slice, list, tuple, or string. If integer,
        this function will attempt to build a copy of this container object with
        dataframes whose contents only contains the slice of the dataframe where
        the **_groupby** attribute matches the integer value. If slice, list,
        or tuple this function will do the same as for an integer but attempt
        to select all matches in the _groupby field. Note that if the _groupby
        attribute is empty, this will select by row index instead (not column
        index!). If string, this function will attempt to get the attribute
        matching that string.

        Note:
            Getting an attribute returns a reference to the attribute not a
            copy of the attribute.
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

    def __sizeof__(self):
        '''
        Sum of the dataframe sizes, trait values, and relational data.

        Warning:
            This function currently doesn't account for memory usage due to
            traits (:class:`~exa.widget.ContainerWidget`).
        '''
        jstot = self._widget_bytes()
        dftot = self._df_bytes()
        other = self._other_bytes()
        kwtot = 0
        for key, value in self._kw_dict().items():
            kwtot += getsizeof(key)
            kwtot += getsizeof(value)
        return dftot + kwtot + jstot + other

    def __init__(self, meta=None, **kwargs):
        self._test = False
        self._traits_need_update = True
        for key, value in kwargs.items():
            if key in self._df_types.keys():
                value = self._enforce_df_type(key, value)
            setattr(self, key, value)
        self.meta = meta
        self._widget = self._widget_class(self) if _conf['notebook'] else None
        if meta is None and len(kwargs) == 0 and len(self._numerical_dict()) == 0:
            self._test = True
            self.name = 'TestContainer'
            self._update_traits()
            self._traits_need_update = False

    def _repr_html_(self):
        if self._widget:
            if self._traits_need_update:
                self._update_traits()
            return self._widget._repr_html_()
        return None


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
