# -*- coding: utf-8 -*-
'''
Container
===============================================
'''
from exa.relational.base import session, datetime, relationship, event
from exa.relational.base import Column, Integer, String, DateTime
from exa.relational.base import ForeignKey, Table, Base, Meta
from exa.utils import gen_uid

ContainerFile = Table(
    'containerfile',
    Base.metadata,
    Column('container_pkid', Integer, ForeignKey('container.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


class Container(Base):
    '''
    Database representation of the 'session' concept.

    See Also:
        :class:`~exa.session.Session`
    '''
    name = Column(String)
    description = Column(String)
    uid = Column(String(32), default=gen_uid)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)
    files = relationship('File', secondary=ContainerFile, backref='containers', cascade='all, delete')


    @classmethod
    def load(cls, key):
        obj = cls._getitem(key)   # This function is in class Meta
        # TODO: attach all of the df data from files
        return obj

    def __getitem__(self, key):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __init__(self, name=None, description=None, **kwargs):
        super().__init__(name=name, description=description)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        if self.name is None:
            return 'Container({0})'.format(self.uid)
        else:
            return 'Container({0})'.format(self.name)


@event.listens_for(Container, 'after_insert')
def _update_files(self, *args):
    '''
    Write/create files on disk (represented by entries in the File
    table/instances of the File class) that are associated with the
    current Container.
    '''
    print('now we rewrite any hdf5 and other files on disk')
    print(self)
    print(args)

@event.listens_for(Container, 'after_delete')
def _remove_files(self, *args):
    '''
    Delete files on disk (represented by entries in the File
    table/instances of the File class) that are associated with the
    recently deleted Container.
    '''
    print('now we delete any hdf5 and other files on disk')
    print(self)
    print(args)
