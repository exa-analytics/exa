# -*- coding: utf-8 -*-
'''
Job
===============================================
'''
from sqlalchemy import String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from exa.utils import gen_uid
from exa.relational.base import dbsession, datetime, Base, Column, Integer


JobContainer = Table(
    'jobcontainer',
    Base.metadata,
    Column('job_pkid', Integer, ForeignKey('job.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('container_pkid', Integer, ForeignKey('container.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


JobFile = Table(
    'jobfile',
    Base.metadata,
    Column('job_pkid', Integer, ForeignKey('job.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


class Job(Base):
    '''
    Specific task in a :class:`~exa.relational.Program` or
    :class:`~exa.relational.Project`.
    '''
    name = Column(String)
    description = Column(String)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)
    size = Column(Integer)
    file_count = Column(Integer)
    containers = relationship('Container', secondary=JobContainer, backref='jobs', cascade='all, delete')
    files = relationship('File', secondary=JobFile, backref='jobs', cascade='all, delete')
