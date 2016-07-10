# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016, Exa Analytics Development Team
# Distributed under the terms of the Apache License 2.0
'''
File Tables
###################
There are two types of file tables, one for "raw" data files (those coming from
third party software for example) and container objects on disk (stored as HDF5
files). Because a container is typically comprised of multiple raw data files,
there is a many to many relationship between raw data files and container files.
'''
from sqlalchemy import String, Column, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from exa.relational.base import Base, Name, HexUID, Time


containerfiledatafile = Table(    # Many to many relationship; ContainerFile - DataFile
    'containerfiledatafile',
    Base.metadata,
    Column('containerfile_pkid', Integer, ForeignKey('containerfile.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('datafile_pkid', Integer, ForeignKey('datafile.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


class DataFile(Name, HexUID, Time, Base):
    '''
    Representation of a non exa container file on disk. Provides content
    management for "raw" data files.
    '''
    extension = Column(String, nullable=False)    # File extension
    size = Column(Integer)


class ContainerFile(Name, HexUID, Time, Base):
    '''
    Representation of an exa container object on disk. Containers are often
    composed from multiple raw data files.
    '''
    size = Column(Integer)
    datafiles = relationship('DataFile', secondary=containerfiledatafile,
                             backref='containerfiles', cascade='all, delete')
