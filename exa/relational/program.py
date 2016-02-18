# -*- coding: utf-8 -*-
'''
Program
===============================================
'''
from sqlalchemy import String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from exa.utils import gen_uid
from exa.relational.base import datetime, Base, Column, Integer


ProgramProject = Table(
    'programproject',
    Base.metadata,
    Column('program_pkid', Integer, ForeignKey('program.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('project_pkid', Integer, ForeignKey('project.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


ProgramJob = Table(
    'programjob',
    Base.metadata,
    Column('program_pkid', Integer, ForeignKey('program.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('job_pkid', Integer, ForeignKey('job.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


ProgramContainer = Table(
    'programcontainer',
    Base.metadata,
    Column('program_pkid', Integer, ForeignKey('program.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('container_pkid', Integer, ForeignKey('container.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


ProgramFile = Table(
    'programfile',
    Base.metadata,
    Column('program_pkid', Integer, ForeignKey('program.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


class Program(Base):
    '''
    Long term or on-going project
    '''
    name = Column(String)
    description = Column(String)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now)
    accessed = Column(DateTime, default=datetime.now)
    size = Column(Integer)
    file_count = Column(Integer)
    projects = relationship('Project', secondary=ProgramProject, backref='programs', cascade='all, delete')
    jobs = relationship('Job', secondary=ProgramJob, backref='programs', cascade='all, delete')
    containers = relationship('Container', secondary=ProgramContainer, backref='programs', cascade='all, delete')
    files = relationship('File', secondary=ProgramFile, backref='programs', cascade='all, delete')
