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
import pandas as pd
from sqlalchemy.orm.attributes import InstrumentedAttribute
from exa import _conf
from exa.widget import Widget


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
        self._save()    # First update the database
        # Second write the dataframes to a file

    def copy(self, **kwargs):
        '''
        Create a copy of the current object.
        '''
        cls = self.__class__
        meta = self.meta
        widget = self._widget.__class__
        kws = self._get_relational_kwargs(copy=True)
        dfs = self._get_dataframes(copy=True)
        kws.update(kwargs)
        kws.update(dfs)
        return cls(meta=meta, widget=widget, **kws)

    @classmethod
    def from_hdf(cls, path):
        '''
        '''
        raise NotImplementedError()

    @classmethod
    def load(cls, pkid=None, path=None):
        '''
        '''
        raise NotImplementedError()

    def _get_relational_kwargs(self, copy=False):
        '''
        Get the relational key word arugments except primary key ids.
        '''
        kws = {}
        for name, value in self.__class__.__dict__.items():
            if isinstance(value, InstrumentedAttribute) and 'id' not in name:
                kws[name] = self[name]
        if copy:
            return kws.copy()
        else:
            return kws

    def _get_dataframes(self, copy=False):
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
