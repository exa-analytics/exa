# -*- coding: utf-8 -*-
'''
Container
===============================================
'''
from sys import getsizeof
from sqlalchemy import Column, String, ForeignKey, Table, Integer, event
from sqlalchemy.orm import relationship, mapper
from exa.relational.base import Base, Name, HexUID, Time, Disk, BaseMeta
from exa.container import BaseContainer
from exa.widget import ContainerWidget


ContainerFile = Table(
    'containerfile',
    Base.metadata,
    Column('container_pkid', Integer, ForeignKey('container.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


class Meta(BaseMeta):
    '''
    Metaclass for :class:`~exa.container.BaseContainer` responsible for
    automatically creating properties for statically typed container class
    attributes.

    .. code-block:: Python

        class TestContainerMeta(BaseContainerMeta):
            attr1 = int
            attr2 = DataFrame


        class TestContainer(metaclass=TestContainerMeta):
            def __init__(self, attr1, attr2):
                self.attr1 = attr1
                self.attr2 = attr2
    '''
    @staticmethod
    def create_property(name, ptype):
        '''
        Helper function to create a type-enforcing property.
        '''
        pname = '_' + name    # See the second code block in the docstring
        def getter(self):
            if not hasattr(self, pname) and hasattr(self, 'compute{}'.format(pname)):
                self['compute{}'.format(pname)]()
            if not hasattr(self, pname):
                raise AttributeError('Please compute or set {} first.'.format(name))
            return getattr(self, pname)
        def setter(self, obj):
            if not isinstance(obj, ptype):
                try:
                    obj = ptype(obj)
                except:
                    raise TypeError('Object {0} must instance of {1}'.format(name, ptype))
            setattr(self, pname, obj)
        def deleter(self):
            del self[pname]
        return property(getter, setter, deleter)

    def __new__(metacls, name, bases, clsdict):
        '''
        Here we control the creation of the class definition. For every statically
        typed attributed (see source code or docstring)
        '''
        for k, v in metacls.__dict__.items():
            if isinstance(v, type) and k[0] != '_':
                clsdict[k] = Meta.create_property(k, v)
        return super().__new__(metacls, name, bases, clsdict)


class Container(BaseContainer, Name, HexUID, Time, Disk, Base, metaclass=Meta):
    '''
    The container class: this class combines relational and data management
    features and wraps them into a single data object.
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
