# -*- coding: utf-8 -*-
'''
Container
#######################
This module provides the front-facing Container object subclassing the
:class:`~exa.container.BaseContainer` and the static typing framework for
relational class attributes, :class:`~exa.container.TypedRelationalMeta`.

See Also:
    :mod:`~exa.container`
'''
from sys import getsizeof
from sqlalchemy import Column, String, ForeignKey, Table, Integer, event
from sqlalchemy.orm import relationship, mapper
from exa.relational.base import Base, Name, HexUID, Time, Disk, BaseMeta
from exa.container import BaseContainer, TypedMeta
from exa.widget import ContainerWidget


ContainerFile = Table(
    'containerfile',
    Base.metadata,
    Column('container_pkid', Integer, ForeignKey('container.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


class TypedRelationalMeta(TypedMeta, BaseMeta):
    '''
    A metaclass for relational objects that have typed attributes.
    '''
    pass


class Container(BaseContainer, Name, HexUID, Time, Disk, Base, metaclass=BaseMeta):
    '''
    The ("master") container class: this class combines relational and data
    management features and wraps them into a single data object.
    '''
    files = relationship('File', secondary=ContainerFile, backref='containers', cascade='all, delete')
    cname = Column(String(32), nullable=False)     # container class name
    __mapper_args__ = {'polymorphic_on': cname,
                       'polymorphic_identity': 'container',
                       'with_polymorphic': '*'}

    def __repr__(self):
        c = self.__class__.__name__
        p = self.pkid
        n = self.name
        u = self.hexuid
        return '{0}({1}: {2}[{3}])'.format(c, p, n, u)
