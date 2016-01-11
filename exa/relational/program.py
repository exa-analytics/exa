# -*- coding: utf-8 -*-
'''
Program
===============================================
'''
from exa.relational.base import session, datetime, relationship
from exa.relational.base import Column, Integer, String, DateTime
from exa.relational.base import ForeignKey, Table, Base, Meta
from exa.utils import gen_uid


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
    projects = relationship('Project', secondary=ProgramProject, backref='programs', cascade='all, delete')
    jobs = relationship('Job', secondary=ProgramJob, backref='programs', cascade='all, delete')
    containers = relationship('Container', secondary=ProgramContainer, backref='programs', cascade='all, delete')
    files = relationship('File', secondary=ProgramFile, backref='programs', cascade='all, delete')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
#        Dashboard._add_to_session(self)
