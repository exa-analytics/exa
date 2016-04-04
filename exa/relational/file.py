# -*- coding: utf-8 -*-
'''
File
===============================================
This module provides relational information about tracking files; it doesn't
itself manipulate files on disk, rather tracks metadata about manipulations
performed.

See Also:
    :class:`~exa.container.BaseContainer`
'''
from datetime import datetime
from sqlalchemy import String, DateTime, Column, Integer
from exa.utility import uid
from exa.relational.base import Base


class File(Base):
    '''
    Represents a pointer to a file on disk.

    Contains information about file size and date modified/created/accessed.
    '''
    name = Column(String)
    description = Column(String)
    uid = Column(String(32), default=uid)
    extension = Column(String, nullable=False)    # This keeps track of file type
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)
    size = Column(Integer)
