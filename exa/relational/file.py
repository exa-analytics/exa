# -*- coding: utf-8 -*-
'''
File
===============================================
'''
from sqlalchemy import String, DateTime
from exa.utility import gen_uid
from exa.relational.base import datetime, Column, Integer, Base


class File(Base):
    '''
    '''
    name = Column(String)
    description = Column(String)
    uid = Column(String(32), default=gen_uid)
    extension = Column(String, nullable=False)         # Defines file's type
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)
    size = Column(Integer)
