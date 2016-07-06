# -*- coding: utf-8 -*-
'''
File Table
###################
This table keeps track of all files managed by exa. This includes containers
(which are HDF5 files on disk) as well as raw data files of any type.
'''
from datetime import datetime
from sqlalchemy import String, Column
from exa.relational.base import Base, generate_hexuid, Name, HexUID, Time


class File(Name, HexUID, Time, Base):
    '''Representation of a file on disk.'''
    extension = Column(String, nullable=False)    # File extension
    container = Column(String)                    # If a container, string class name
    size = Column(Integer)
