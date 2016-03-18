# -*- coding: utf-8 -*-
'''
The Container Module
===============================================
This module provides the relational container object and a relationship table
that connects containers to recrods representing files on disk.
'''
from sys import getsizeof
from sqlalchemy import Column, String, ForeignKey, Table, Integer, event
from sqlalchemy.orm import relationship, mapper
from exa.relational.base import Base, Name, HexUID, Time, Disk
from exa.container import BaseContainer


ContainerFile = Table(
    'containerfile',
    Base.metadata,
    Column('container_pkid', Integer, ForeignKey('container.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


class Container(BaseContainer, Name, HexUID, Time, Disk, Base):
    '''
    The relational store and file controller that is inherited by data specific
    containers to facilitate data processing, analysis, and visualization.
    '''
    files = relationship('File', secondary=ContainerFile, backref='containers', cascade='all, delete')
    _ctype = Column(String(32), nullable=False)    # Container type == class name
    __mapper_args__ = {'polymorphic_on': _ctype,
                       'polymorphic_identity': 'container',
                       'with_polymorphic': '*'}

    def __repr__(self):
        c = self.__class__.__name__
        p = self.pkid
        n = self.name
        u = self.hexuid
        return '{0}({1}: {2}[{3}])'.format(c, p, n, u)


@event.listens_for(Container, 'before_insert')
def _before_insert(mapper, connection, target):
    '''
    Before insertion update the time stamp and size.
    '''
    target._update_size()
    target._update_accessed()


#    def _update_traits(self):
#        '''
#        Overwritten when records require complexe trait updating logic.
#        '''
#        self._update_df_traits()
#        self._traits_need_update = False
#
#    def _add_unicode_traits(self, **values):
#        '''
#        Add custom traits from DataFrame json strings.
#
#        Warning:
#            Only supports Unicode!
#        '''
#        for name, value in values.items():
#            obj = traitlets.Unicode().tag(sync=True)
#            obj.class_init(self.__class__, name)
#            setattr(self.__class__, name, obj)
#            obj.instance_init(self)
#            self[name] = value
#            self.send_state(name)
#
#    def _update_df_traits(self):
#        '''
#        '''
#        for name in self.__dfclasses__.keys():
#            value = self[name]
#            if isinstance(value, DataFrame):
#                values = self[name].get_trait_values()
#                self._add_unicode_traits(**values)
#
#    def _get_by_index(self, index):
#        '''
#        Positional getter.
#        '''
#        cp = self.copy()
#        for name, df in cp.get_dataframes().items():
#            if isinstance(df, DataFrame):
#                cp[name] = df._get_by_index(index)
#        #cp._update_traits()
#        return cp
#
#    def _get_by_indices(self, indices):
#        '''
#        '''
#        cp = self.copy()
#        for name, df in cp.get_dataframes().items():
#            if isinstance(df, DataFrame):
#                cp[name] = df._get_by_indices(indices)
#        #cp._update_traits()
#        return cp
#
#    def _get_by_slice(self, key):
#        '''
#        '''
#        cp = self.copy()
#        for name, df in cp.get_dataframes().items():
#            if isinstance(df, DataFrame):
#                cp[name] = df._get_by_slice(key)
#        #cp._update_traits()
#        return cp
#
#    def __iter__(self):
#        raise NotImplementedError()
#
#    def __len__(self):
#        raise NotImplementedError()
#
#    def __getitem__(self, key):
#        '''
#        Integers, slices, and lists are assumed to be values in the index (
#        for multi-indexed dataframes, corresponding to level 0).
#        '''
#        if isinstance(key, int):
#            return self._get_by_index(key)
#        elif isinstance(key, list):
#            return self._get_by_indices(key)
#        elif isinstance(key, slice):
#            return self._get_by_slice(key)
#        elif isinstance(key, str):
#            return getattr(self, key)
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
#        if isinstance(value, pd.DataFrame) and not isinstance(value, DataFrame):
#            for name, cls in self.__dfclasses__.items():
#                if key == name:
#                    super().__setattr__(key, cls(value))
#                    return
#            super().__setattr__(key, DataFrame(value))
#            return
#        super().__setattr__(key, value)
#
#    def __init__(self, meta=None, dfs=None, **kwargs):
#        super().__init__(**kwargs)
#        if dfs:                               # DataFrame attributes
#            if isinstance(dfs, dict):
#                for name, df in dfs.items():
#                    setattr(self, name, df)
#                    self.__dfclasses__[name] = df.__class__
#            else:
#                raise TypeError('Argument "dfs" must be of type dict.')
#        self.meta = meta
#        self._traits_need_update = True
#
#
#    def __str__(self):
#        return repr(self)
#
#
