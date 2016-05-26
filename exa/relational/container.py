# -*- coding: utf-8 -*-
'''
Container
===============================================
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
