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
from sys import getsizeof
from traitlets import Bool
from sqlalchemy.orm.attributes import InstrumentedAttribute
from exa import _conf
from exa.widget import ContainerWidget
from exa.numerical import NDBase
from exa.utility import del_keys


class BaseContainer:
    '''
    Foundational class for creating data containers. Inherited by
    :class:`~exa.relational.container.Container`. This class should not be
    inherited directly; rather :class:`~exa.relational.container.Container`
    should be inherited.
    '''
    _widget_class = ContainerWidget

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

    def info(self):
        '''
        Print human readable information about the container.
        '''
        n = getsizeof(self)
        sizes = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'too high..']
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
                    kwargs = store.get_storer(key).attrs.metadata
                else:
                    kwargs[key[1:]] = store[key]
        c = cls(**kwargs)
        c._update_accessed()
        return c

    @classmethod
    def load(cls, pkid=None, path=None):
        '''
        '''
        if pkid:
            raise NotImplementedError()
        return cls.from_hdf(path)

    def _save_data(self, path=None):
        '''
        Save the dataframe (and related series) data to an `HDF5`_ file. This
        file contains all of the dataframe data as well as the descriptive
        relational data attached to the current container.
        '''
        # Check the path
        if path is None:
            path = self.hexuid + '.hdf5'
        elif os.path.isdir(path):
            path += os.sep + self.hexuid + '.hdf5'
        elif not (path.endswith('.hdf5') or path.endswith('.hdf')):
            raise ValueError('File path must have a ".hdf5" or ".hdf" extension.')
        # Get the container "kwargs" - relational values and metadata
        kwargs = self._kw_dict()
        kwargs['meta'] = str(self.meta) if self.meta else None
        kwargs = del_keys(kwargs)
        with pd.HDFStore(path) as store:
            store['kwargs'] = pd.Series()
            store.get_storer('kwargs').attrs.metadata = kwargs
            for name, df in self._numerical_dict().items():
                if isinstance(df, DataFrame):
                    df._revert_categories()
                    store[name] = df.copy()
                    df._set_categories()
                else:
                    store[name] = df

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

    def _df_bytes(self):
        '''
        Compute the size (in bytes) of all of the attached dataframes.
        '''
        total_bytes = 0
        for df in self._numerical_dict().values():
            total_bytes += df.values.nbytes
            total_bytes += df.index.nbytes
            total_bytes += df.columns.nbytes
        return total_bytes

    def _trait_names(self):
        '''
        Poll each of the attached :class:`~exa.ndframe.DataFrame` for their
        trait names.
        '''
        names = []
        has_traits = self._numerical_dict()
        for name, obj in has_traits.items():
            obj._update_traits()
            names += obj._traits
        self._widget._names = names

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
        traits = {}
        if self._test:
            traits['test'] = Bool(True).tag(sync=True)
        else:
            traits = self._custom_container_traits()
            has_traits = self._numerical_dict(cls_criteria=[NDBase])
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

    def _slice_with_int_or_string(self, key):
        '''
        Slices the current container selecting data that matches the key (either on _groupbys or
        by row index).
        '''
        cls = self.__class__
        kws = del_keys(self._kw_dict(copy=True))
        for name, df in self._numerical_dict(copy=True).items():
            dfcls = df.__class__
            if not hasattr(df, '_groupbys') and key not in df.index:
                kws[name] = df
            elif hasattr(df, '_groupbys'):
                if np.any([key in df[col] for col in df._groupbys]):
                    kws[name] = dfcls(df.groupby(df._groupbys).get_group(key))
                elif key in df.index:
                    kws[name] = dfcls(df.ix[key:key, :])
                else:
                    kws[name] = df
            else:
                kws[name] = dfcls(df.ix[key:key, :])
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
                if np.all([np.any([key in df[col] for col in df._groupbys]) for key in keys]):
                    kws[name] = dfcls(pd.concat([df.groupby(df._groupbys).get_group(key) for key in keys]))
                elif np.all([key in df.index for key in keys]):
                    kws[name] = dfcls(df.ix[keys, :])
                else:
                    kws[name] = df
            elif np.all([key in df.index for key in keys]):
                kws[name] = dfcls(df.ix[keys, :])
            else:
                kws[name] = df
        return cls(**kws)

    def __getitem__(self, key):
        '''
        The key can be an integer, slice, list, tuple, or string. If integer, this function will
        attempt to build a copy of this container object with dataframes whose contents only contains
        the slice of the dataframe where the **_groupby** attribute matches the integer value. If
        slice, list, or tuple this function will do the same as for an integer but attempt to select
        all matches in the _groupby field. Note that if the _groupby attribute is empty, this will
        select by row index instead (not column index!). If string, this function will attempt to
        get the attribute matching that string.
        '''
        if isinstance(key, int):
            return self._slice_with_int_or_string(key)
        elif isinstance(key, str) and not hasattr(self, key):
            return self._slice_with_int_or_string(key)
        elif isinstance(key, list) or isinstance(key, tuple):
            return self._slice_with_list_or_tuple(key)
        elif isinstance(key, slice):
            raise NotImplementedError()
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
        jstot = 0  # Memory usage from the widget view
        dftot = self._df_bytes()
        kwtot = 0
        for key, value in self._kw_dict().items():
            kwtot += getsizeof(key)
            kwtot += getsizeof(value)
        return dftot + kwtot + jstot

    def __init__(self, meta=None, **kwargs):
        self._test = False
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.meta = meta
        self._widget = self._widget_class(self) if _conf['notebook'] else None
        if meta is None and len(kwargs) == 0:
            self._test = True
            self.name = 'TestContainer'
            self._update_traits()

    def _repr_html_(self):
        if self._widget:
            return self._widget._repr_html_()
        return None
