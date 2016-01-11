# -*- coding: utf-8 -*-
'''
File
===============================================
'''
from exa.relational.base import datetime
from exa.relational.base import Column, Integer, String, DateTime, Base
from exa.utils import gen_uid


class File(Base):
    '''
    '''
    name = Column(String)
    description = Column(String)
    uid = Column(String(32), default=gen_uid)
    ext = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)
    size = Column(Integer)
