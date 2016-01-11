# -*- coding: utf-8 -*-
'''
File
===============================================
'''
from exa.relational.base import session, datetime, relationship
from exa.relational.base import Column, Integer, String, DateTime
from exa.relational.base import ForeignKey, Table, Base, Meta
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Dashboard._add_to_session(self)
        Dashboard._add_to_program(self)
        Dashboard._add_to_project(self)
        Dashboard._add_to_job(self)
