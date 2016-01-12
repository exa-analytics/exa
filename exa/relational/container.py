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
