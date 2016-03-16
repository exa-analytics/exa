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
import pandas as pd
from sqlalchemy.orm.attributes import InstrumentedAttribute
from exa import _conf
from exa.widget import Widget


_rm_keys = ('id', 'accessed', 'modified', 'files', 'created', 'size')
_widget_default = Widget if _conf['notebook'] else None


class BaseContainer:
    '''
    Foundational class for creating data containers. Inherited by
    :class:`~exa.relational.container.Container`. This class should not be
    inherited directly; rather :class:`~exa.relational.container.Container`
    should be inherited.
    '''
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
        meta = self.meta
        widget = self._widget.__class__
        kws = self._kw_dict(copy=True)
        kws = _prune_kws(kws, _rm_keys)
        dfs = self._dataframe_dict(copy=True)
        kws.update(kwargs)
        kws.update(dfs)
        return cls(meta=meta, widget=widget, **kws)

    def info(self):
        '''
        Print human readable information about the container.
        '''
        df_total_bytes = self._df_bytes()
        n = df_total_bytes
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
            if '/_relational' in store.keys():
                kwargs = store['/_relational'].to_dict()
            for key in store.keys():
                kwargs[key[1:]] = store[key]
        return cls(**kwargs)

    @classmethod
    def load(cls, pkid=None, path=None):
        '''
        '''
        if pkid:
            raise NotImplementedError()
        else:
            return cls.from_hdf(path)

    def _save_data(self, path=None):
        '''
        Save the dataframe (and related series) data to an `HDF5`_ file. This
        file contains all of the
        '''
        if path is None:
            path = self.hexuid + '.hdf5'
        elif os.path.isdir(path):
            path += os.sep + self.hexuid + '.hdf5'
        elif not (path.endswith('.hdf5') or path.endswith('.hdf')):
            raise ValueError('File path must have a ".hdf5" or ".hdf" extension.')
        series = pd.Series(_prune_kws(self._kw_dict(copy=True), _rm_keys))
        series['meta'] = str(self.meta) if self.meta else None
        with pd.HDFStore(path) as store:
            store['_relational'] = series
            for name, df in self._dataframe_dict().items():
                store[name] = df

    def _df_bytes(self):
        '''
        Compute the size of all of the attached dataframes
        '''
        total_bytes = 0
        for df in self._dataframe_dict().values():
            total_bytes += df.values.nbytes
            total_bytes += df.index.nbytes
            total_bytes += df.columns.nbytes
        return total_bytes

    def _kw_dict(self, copy=False):
        '''
        '''
        kws = {}
        for name, value in self.__class__.__dict__.items():
            if isinstance(value, InstrumentedAttribute):
                kws[name] = self[name]
        if copy:
            return kws.copy()
        else:
            return kws

    def _dataframe_dict(self, copy=False):
        '''
        Get the attached dataframe objects.
        '''
        dfs = {}
        for name, value in self.__dict__.items():
            if isinstance(value, pd.DataFrame):
                if copy:
                    dfs[name] = value.copy()
                else:
                    dfs[name] = value
        return dfs

    def _kw_frame(self):
        '''
        Create a dataframe from the kwargs used to generate this container
        in order to save them to HDF5.
        '''
        kwargs = _prune_kws(self._kw_dict(), _rm_keys)
        df = pd.Series(kwargs).to_frame().T
        for column in df.columns:
            df[column] = df[column].astype(type(kwargs[column]))
        return df

    def __sizeof__(self):
        '''
        Sum of the dataframe sizes, trait values, and relational data.
        '''
        pass

    def __getitem__(self, key):
        if isinstance(key, int):
            pass
        elif hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError()

    def __init__(self, meta=None, widget=_widget_default, **kwargs):
        '''
        Args:
            meta: Dictionary of metadata key, value pairs
            widget: Class instance (of Jupyter notebook widget) or None
        '''
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.meta = meta
        self._widget = widget(self) if widget else None

    def _repr_html_(self):
        if self._widget:
            return self._widget._ipython_display_()
        return None


def _prune_kws(kws, to_prune, how='contains'):
    '''
    '''
    rkws = kws.copy()
    for key in kws.keys():
        if any((prune in key for prune in to_prune)):
            del rkws[key]
    return rkws
