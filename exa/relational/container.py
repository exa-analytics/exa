# -*- coding: utf-8 -*-
'''
Container
===============================================
'''
from ipywidgets import DOMWidget
from traitlets import Unicode
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from exa import _pd as pd
from exa import _np as np
from exa.frames import DataFrame
from exa.relational.base import Column, Integer, Base, Name, HexUID, Time, Disk


ContainerFile = Table(
    'containerfile',
    Base.metadata,
    Column('container_pkid', Integer, ForeignKey('container.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


class Container(DOMWidget, Name, HexUID, Time, Disk, Base):
    '''
    Containers control data manipulation, processing, and provide convenient
    visualizations.
    '''
    # Relational information
    container_type = Column(String(16))
    files = relationship('File', secondary=ContainerFile, backref='containers', cascade='all, delete')
    __mapper_args__ = {
        'polymorphic_identity': 'container',   # This allows the container to
        'polymorphic_on': container_type,      # be inherited.
        'with_polymorphic': '*'
    }
    __dfclasses__ = {}

    # Widget information
    _ipy_disp = DOMWidget._ipython_display_
    _view_module = Unicode('nbextensions/exa/container').tag(sync=True)
    _view_name = Unicode('HelloView').tag(sync=True)

    def to_archive(self, path):
        '''
        Export this container to an archive that can be imported in another
        session (on any machine).
        '''
        raise NotImplementedError()

    def copy(self):
        '''
        Create a copy of the current object
        '''
        cls = self.__class__
        kwargs = {'name': self.name, 'description': self.description}
        kwargs['dfs'] = self.get_dataframes()
        print(kwargs)
        obj = cls(**kwargs)
        return obj

    def get_dataframes(self):
        '''
        Get a dictionary of dataframes. Keys are the dataframe variable name
        and values are the dataframe itself.
        '''
        return {name: df for name, df in vars(self).items() if isinstance(df, DataFrame)}

    @classmethod
    def from_archive(cls, path):
        '''
        Import a container from an archive into the current session.

        Note:
            This function will also create file entries and objects
            corresponding to the data provided in the archive.
        '''
        raise NotImplementedError()

    def _ipython_display_(self):
        '''
        Custom HTML representation
        '''
        self._ipy_disp()
        print(repr(self))

    def _repr_html_(self):
        return self._ipython_display_()

    def __setitem__(self, key, value):
        '''
        Custom set calls __setattr__ to enforce certain types.
        '''
        setattr(self, key, value)

    def __setattr__(self, key, value):
        '''
        Custom attribute setting to enforce custom dataframe types.
        '''
        if isinstance(value, pd.DataFrame):
            for name, cls in self.__dfclasses__.items():
                if key == name:
                    super().__setattr__(key, cls(value))
                    #setattr(self, key, cls(value))
                    return
            super().__setattr__(key, DataFrame(value))
            #setattr(self, key, DataFrame(value))
            return
        super().__setattr__(key, value)
        #setattr(self, key, value)

    def __init__(self, name=None, description=None, meta=None, dfs=None):
        super().__init__()
        self.name = name
        self.description = description
        self.meta = meta
        if dfs:
            if isinstance(dfs, dict):
                for name, df in dfs.items():
                    self[name] = df
            else:
                raise TypeError('Argument "dfs" must be of type dict.')

    def __repr__(self):
        c = self.__class__.__name__
        p = self.pkid
        n = self.name
        u = self.uid
        return '{0}({1}: {2}[{3}])'.format(c, p, n, u)

    def __str__(self):
        return repr(self)


def concat(containers, axis=0, join='inner'):
    '''
    Concatenate a collection of containers.
    '''
    raise NotImplementedError()


#    def _get_by_index(self, index):
#        '''
#        '''
#        obj = self.copy()
#        for name, df in obj.dataframes.items():
#            if len(df) > 0:
#                index_name = df.index.names[0]
#                obj[name] = df.ix[df.index.isin([index], index_name), :]
#        return obj
#
#    def _get_by_indices(self, indices):
#        '''
#        '''
#        obj = self.copy()
#        for name, df in obj.dataframes.items():
#            if len(df) > 0:
#                index_name = df.index.names[0]
#                obj[name] = df.ix[df.index.isin(indices, index_name), :]
#        return obj
#
#    def _get_by_slice(self, key):
#        '''
#        '''
#        obj = self.copy()
#        for name, df in obj.dataframes.items():
#            if len(df) > 0:
#                index_name = df.index.names[0]
#                index_values = df.index.get_level_values(index_name).unique()
#                start = index_values[0] if key.start is None else key.start
#                stop = index_values[-1] if key.stop is None else key.stop
#                step = index_values[1] - index_values[0] if key.step is None else key.step
#                stop += step            # To ensure we get the endpoint
#                indices = np.arange(start, stop, step, dtype=np.int64)
#                obj[name] = df.ix[df.index.isin(indices, index_name), :]
#        return obj
#
#    def __getitem__(self, key):
#        '''
#        Integers, slices, and lists are assumed to be values in the index (
#        for multi-indexed dataframes, corresponding to level 0).
#        '''
#        if isinstance(key, int):
#            return self._get_single(key)
#        elif isinstance(key, list):
#            return self._get_by_indices(key)
#        elif isinstance(key, slice):
#            return self._get_by_slice(key)
#        else:
#            raise NotImplementedError()
#
#    def __setitem__(self, key, value):
#        '''
#        Custom set calls __setattr__ to enforce certain types.
#        '''
#        setattr(self, key, value)
#
#    def __setattr__(self, key, value):
#        '''
#        Custom attribute setting to enforce custom dataframe types.
#        '''
#        if isinstance(value, pd.DataFrame):
#            for name, cls in self.__dfclasses__.items():
#                if key == name:
#                    self.__dict__[key] = cls(value)
#                    return
#            self.__dict__[key] = DataFrame(value)
#            return
#        self.__dict__[key] = value
#
#    def __iter__(self):
#        raise NotImplementedError()
#
#    def __len__(self):
#        raise NotImplementedError()
#
