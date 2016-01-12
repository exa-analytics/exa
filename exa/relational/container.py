# -*- coding: utf-8 -*-
'''
Container
===============================================
'''
from exa.relational.base import session, datetime, relationship, event
from exa.relational.base import Column, Integer, String, DateTime
from exa.relational.base import ForeignKey, Table, Base
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
    size = Column(Integer)
    file_count = Column(Integer)
    files = relationship('File', secondary=ContainerFile, backref='containers', cascade='all, delete')

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


@event.listens_for(Container, 'before_insert')
def before_insert(mapper, connection, container):
    '''
    '''
    print('before insert')

@event.listens_for(Container, 'before_update')
def _before_update(mapper, connection, container):
    '''
    Actions to perform just before commiting Containers
    '''
    print('just before update')

@event.listens_for(Container, 'after_insert')
def _create_files(mapper, connection, container):
    '''
    Write/create files on disk (represented by entries in the File
    table/instances of the File class) that are associated with the
    current Container.
    '''
    print('now we rewrite any hdf5 and other files on disk')

@event.listens_for(Container, 'after_update')
def _update_files(mapper, connection, container):
    '''
    '''
    print('update!')

@event.listens_for(Container, 'after_delete')
def _delete_files(mapper, connection, container):
    '''
    Delete files on disk (represented by entries in the File
    table/instances of the File class) that are associated with the
    recently deleted Container.
    '''
    print('now we delete any hdf5 and other files on disk')
