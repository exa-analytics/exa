# -*- coding: utf-8 -*-
'''
Job Table
#############
'''
from sqlalchemy import String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from exa.relational.base import Name, Time, Size, Base


jobfile = Table(
    'jobfile',
    Base.metadata,
    Column('job_pkid', Integer, ForeignKey('job.pkid', onupdate='CASCADE', ondelete='CASCADE')),
    Column('file_pkid', Integer, ForeignKey('file.pkid', onupdate='CASCADE', ondelete='CASCADE'))
)


class Job(Name, Time, Size, Base):
    '''
    Specific task in a :class:`~exa.relational.Program` or
    :class:`~exa.relational.Project`.
    '''
    file_count = Column(Integer)
    files = relationship('File', secondary=JobFile, backref='jobs', cascade='all, delete')
